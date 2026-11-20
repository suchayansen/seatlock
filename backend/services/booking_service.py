
from backend.config.database import get_db
from backend.services.audit_service import write_audit

MAX_SEATS_PER_BOOKING = 4
HOLD_DURATION_MINUTES = 5


def hold_seats(student_id, event_id, seat_ids):
    """
    Atomically hold multiple seats for five minutes.
    Returns a result dictionary.
    """

    if not seat_ids:
        return {"success": False, "error": "Select at least one seat."}

    if len(seat_ids) > MAX_SEATS_PER_BOOKING:
        return {"success": False, "error": "Maximum 4 seats allowed."}

    if len(set(seat_ids)) != len(seat_ids):
        return {"success": False, "error": "Duplicate seat IDs."}

    pool = get_db()

    try:
        with pool.connection() as conn:

            # 1. Lock student row to serialize their hold requests.
            student = conn.execute(
                """
                SELECT id, role, is_active
                FROM users
                WHERE id = %s
                FOR UPDATE
                """,
                (student_id,)
            ).fetchone()

            if not student or student[1] != "student" or not student[2]:
                return {"success": False, "error": "Invalid student."}

            # 2. Validate event and booking window.
            event = conn.execute(
                """
                SELECT id
                FROM events
                WHERE id = %s
                  AND status = 'published'
                  AND event_date > NOW()
                  AND (booking_opens_at IS NULL OR booking_opens_at <= NOW())
                  AND (booking_closes_at IS NULL OR booking_closes_at > NOW())
                """,
                (event_id,)
            ).fetchone()

            if not event:
                return {"success": False, "error": "Event is unavailable for booking."}

            # 3. Find expired holds in this event, in stable order.
            expired_holds = conn.execute(
                """
                SELECT id
                FROM holds
                WHERE event_id = %s
                  AND status = 'active'
                  AND expires_at <= NOW()
                ORDER BY id
                FOR UPDATE
                """,
                (event_id,)
            ).fetchall()

            expired_ids = [row[0] for row in expired_holds]

            if expired_ids:
                # Lock affected seats in stable order.
                expired_seats = conn.execute(
                    """
                    SELECT DISTINCT s.id
                    FROM seats s
                    JOIN hold_seats hs ON hs.seat_id = s.id
                    WHERE hs.hold_id = ANY(%s)
                    ORDER BY s.id
                    FOR UPDATE OF s
                    """,
                    (expired_ids,)
                ).fetchall()

                conn.execute(
                    """
                    UPDATE holds
                    SET status = 'expired', updated_at = NOW()
                    WHERE id = ANY(%s)
                    """,
                    (expired_ids,)
                )
                write_audit(
                    conn,
                    action="booking_confirmed",
                    actor_id=student_id,
                    event_id=event_id,
                    entity_type="booking",
                    entity_id=booking_id,
                    details={
                        "booking_reference": booking_reference,
                        "seat_count": len(seats)
                    }
                )

                conn.execute(
                    """
                    UPDATE seats
                    SET status = 'available',
                        version = version + 1,
                        updated_at = NOW()
                    WHERE id = ANY(%s)
                      AND status = 'held'
                    """,
                    ([row[0] for row in expired_seats],)
                )

            # 4. Replace this student's previous active hold.
            previous = conn.execute(
                """
                SELECT id
                FROM holds
                WHERE student_id = %s
                  AND event_id = %s
                  AND status = 'active'
                FOR UPDATE
                """,
                (student_id, event_id)
            ).fetchone()

            if previous:
                old_hold_id = previous[0]

                old_seats = conn.execute(
                    """
                    SELECT s.id
                    FROM seats s
                    JOIN hold_seats hs ON hs.seat_id = s.id
                    WHERE hs.hold_id = %s
                    ORDER BY s.id
                    FOR UPDATE OF s
                    """,
                    (old_hold_id,)
                ).fetchall()

                conn.execute(
                    """
                    UPDATE holds
                    SET status = 'cancelled', updated_at = NOW()
                    WHERE id = %s
                    """,
                    (old_hold_id,)
                )

                conn.execute(
                    """
                    UPDATE seats
                    SET status = 'available',
                        version = version + 1,
                        updated_at = NOW()
                    WHERE id = ANY(%s)
                      AND status = 'held'
                    """,
                    ([row[0] for row in old_seats],)
                )

            # 5. Lock requested seats in stable order.
            seats = conn.execute(
                """
                SELECT id, status
                FROM seats
                WHERE event_id = %s
                  AND id = ANY(%s)
                ORDER BY id
                FOR UPDATE
                """,
                (event_id, seat_ids)
            ).fetchall()

            if len(seats) != len(seat_ids):
                return {"success": False, "error": "One or more seats do not exist."}

            if any(seat[1] != "available" for seat in seats):
                return {"success": False, "error": "One or more seats are unavailable."}

            # 6. Enforce maximum 4 confirmed + currently requested seats.
            booked_count = conn.execute(
                """
                SELECT COUNT(*)
                FROM bookings b
                JOIN booking_seats bs ON bs.booking_id = b.id
                WHERE b.student_id = %s
                  AND b.event_id = %s
                  AND b.status IN ('confirmed', 'checked_in')
                  AND bs.is_active = TRUE
                """,
                (student_id, event_id)
            ).fetchone()[0]

            if booked_count + len(seat_ids) > MAX_SEATS_PER_BOOKING:
                return {"success": False, "error": "Maximum 4 seats per event allowed."}

            # 7. Create five-minute hold.
            hold = conn.execute(
                """
                INSERT INTO holds (event_id, student_id, expires_at)
                VALUES (%s, %s, NOW() + INTERVAL '5 minutes')
                RETURNING id, expires_at
                """,
                (event_id, student_id)
            ).fetchone()

            hold_id, expires_at = hold

            # 8. Associate seats with hold.
            for seat_id in seat_ids:
                conn.execute(
                    """
                    INSERT INTO hold_seats (hold_id, seat_id)
                    VALUES (%s, %s)
                    """,
                    (hold_id, seat_id)
                )

            # 9. Mark seats held.
            conn.execute(
                """
                UPDATE seats
                SET status = 'held',
                    version = version + 1,
                    updated_at = NOW()
                WHERE id = ANY(%s)
                """,
                (seat_ids,)
            )

            write_audit(
                conn,
                action="seat_hold_created",
                actor_id=student_id,
                event_id=event_id,
                entity_type="hold",
                entity_id=hold_id,
                details={
                    "seat_ids": [str(seat_id) for seat_id in seat_ids],
                    "expires_at": expires_at.isoformat()
                }
            )

            return {
                "success": True,
                "hold_id": str(hold_id),
                "expires_at": expires_at.isoformat(),
                "seat_count": len(seat_ids)
            }

    except Exception:
        # The connection transaction rolls back on exceptions.
        raise


import secrets
import string


def generate_booking_reference():
    return "SL-" + "".join(
        secrets.choice(string.ascii_uppercase + string.digits)
        for _ in range(10)
    )


def confirm_hold(hold_id, student_id):
    """
    Convert a valid five-minute hold into a confirmed booking.
    """

    pool = get_db()

    with pool.connection() as conn:

        # Lock the hold first.
        hold = conn.execute(
            """
            SELECT id, event_id, student_id, expires_at, status
            FROM holds
            WHERE id = %s
            FOR UPDATE
            """,
            (hold_id,)
        ).fetchone()

        if not hold:
            return {"success": False, "error": "Hold not found."}

        hold_id, event_id, owner_id, expires_at, status = hold

        if str(owner_id) != str(student_id):
            return {"success": False, "error": "You do not own this hold."}

        if status != "active":
            return {"success": False, "error": "Hold is no longer active."}

        # Check expiry using PostgreSQL's clock.
        valid = conn.execute(
            "SELECT %s > NOW()",
            (expires_at,)
        ).fetchone()[0]

        if not valid:
            conn.execute(
                """
                UPDATE holds
                SET status = 'expired', updated_at = NOW()
                WHERE id = %s
                """,
                (hold_id,)
            )

            conn.execute(
                """
                UPDATE seats s
                SET status = 'available',
                    version = version + 1,
                    updated_at = NOW()
                FROM hold_seats hs
                WHERE hs.hold_id = %s
                  AND hs.seat_id = s.id
                  AND s.status = 'held'
                """,
                (hold_id,)
            )

            return {"success": False, "error": "Hold has expired."}

        # Lock held seats in stable order.
        seats = conn.execute(
            """
            SELECT s.id, s.status
            FROM seats s
            JOIN hold_seats hs ON hs.seat_id = s.id
            WHERE hs.hold_id = %s
            ORDER BY s.id
            FOR UPDATE OF s
            """,
            (hold_id,)
        ).fetchall()

        if not seats:
            return {"success": False, "error": "No seats found for this hold."}

        if any(seat[1] != "held" for seat in seats):
            return {"success": False, "error": "Seat state conflict."}

        # Create booking.
        booking_reference = generate_booking_reference()

        booking = conn.execute(
            """
            INSERT INTO bookings (
                event_id, student_id, hold_id, booking_reference
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (event_id, student_id, hold_id, booking_reference)
        ).fetchone()

        booking_id = booking[0]

        # Create booking-seat records.
        for seat in seats:
            conn.execute(
                """
                INSERT INTO booking_seats (
                    booking_id, seat_id, price, is_active
                )
                VALUES (%s, %s, 0, TRUE)
                """,
                (booking_id, seat[0])
            )

        # Mark seats as booked.
        conn.execute(
            """
            UPDATE seats
            SET status = 'booked',
                version = version + 1,
                updated_at = NOW()
            WHERE id = ANY(%s)
            """,
            ([seat[0] for seat in seats],)
        )

        # Complete the hold.
        conn.execute(
            """
            UPDATE holds
            SET status = 'confirmed', updated_at = NOW()
            WHERE id = %s
            """,
            (hold_id,)
        )

        return {
            "success": True,
            "booking_id": str(booking_id),
            "booking_reference": booking_reference,
            "seat_count": len(seats)
        }

def get_seat_map(event_id):
    pool = get_db()

    with pool.connection() as conn:
        rows = conn.execute(
            """
            SELECT id, seat_number, section, status, version
            FROM seats
            WHERE event_id = %s
            ORDER BY section, seat_number
            """,
            (event_id,)
        ).fetchall()

    return [
        {
            "id": str(row[0]),
            "seat_number": row[1],
            "section": row[2],
            "status": row[3],
            "version": row[4]
        }
        for row in rows
    ]


def cancel_booking(booking_id, student_id):
    pool = get_db()

    with pool.connection() as conn:

        # 1. Lock and validate booking ownership
        booking = conn.execute(
            """
            SELECT id, event_id, status
            FROM bookings
            WHERE id = %s AND student_id = %s
            FOR UPDATE
            """,
            (booking_id, student_id)
        ).fetchone()

        if not booking:
            return {
                "success": False,
                "error": "Booking not found."
            }

        event_id = booking[1]
        booking_status = booking[2]

        if booking_status != "confirmed":
            return {
                "success": False,
                "error": "Booking cannot be cancelled."
            }

        # 2. Lock associated seats in stable order
        seats = conn.execute(
            """
            SELECT s.id
            FROM seats s
            JOIN booking_seats bs ON bs.seat_id = s.id
            WHERE bs.booking_id = %s
              AND bs.is_active = TRUE
            ORDER BY s.id
            FOR UPDATE OF s
            """,
            (booking_id,)
        ).fetchall()

        seat_ids = [row[0] for row in seats]

        # 3. Deactivate booking-seat records
        conn.execute(
            """
            UPDATE booking_seats
            SET is_active = FALSE
            WHERE booking_id = %s
              AND is_active = TRUE
            """,
            (booking_id,)
        )

        # 4. Release seats
        if seat_ids:
            conn.execute(
                """
                UPDATE seats
                SET status = 'available',
                    version = version + 1,
                    updated_at = NOW()
                WHERE id = ANY(%s)
                """,
                (seat_ids,)
            )

        # 5. Mark booking as cancelled
        conn.execute(
            """
            UPDATE bookings
            SET status = 'cancelled',
                cancelled_at = NOW(),
                updated_at = NOW()
            WHERE id = %s
            """,
            (booking_id,)
        )

        # 6. Write audit log in the SAME transaction
        write_audit(
            conn,
            action="booking_cancelled",
            actor_id=student_id,
            event_id=event_id,
            entity_type="booking",
            entity_id=booking_id,
            details={
                "seats_released": len(seat_ids),
                "seat_ids": [str(seat_id) for seat_id in seat_ids]
            }
        )

        return {
            "success": True,
            "message": "Booking cancelled.",
            "booking_id": str(booking_id),
            "seats_released": len(seat_ids)
        }


