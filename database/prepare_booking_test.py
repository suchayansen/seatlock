
from backend.config.database import init_db, get_db, close_db

EVENT_ID = "bf02b856-9122-47f2-adac-3ef927639a96"

if __name__ == "__main__":
    try:
        init_db()
        pool = get_db()

        with pool.connection() as conn:
            conn.execute(
                """
                UPDATE events
                SET status = 'published',
                    booking_opens_at = NOW() - INTERVAL '1 hour',
                    booking_closes_at = NOW() + INTERVAL '29 days'
                WHERE id = %s
                """,
                (EVENT_ID,)
            )

            for seat_number in ["A1", "A2", "A3", "A4", "A5"]:
                conn.execute(
                    """
                    INSERT INTO seats (event_id, seat_number, section)
                    VALUES (%s, %s, 'Section A')
                    ON CONFLICT (event_id, seat_number) DO NOTHING
                    """,
                    (EVENT_ID, seat_number)
                )

            seats = conn.execute(
                """
                SELECT id, seat_number, status
                FROM seats
                WHERE event_id = %s
                ORDER BY seat_number
                """,
                (EVENT_ID,)
            ).fetchall()

            print("\nTest seats:")
            for seat in seats:
                print(seat)

    finally:
        close_db()
