
from backend.config.database import init_db, get_db, close_db


def create_test_event(email, title):
    pool = get_db()

    with pool.connection() as conn:
        organizer = conn.execute(
            """
            SELECT id FROM users
            WHERE LOWER(email) = LOWER(%s)
              AND role = 'organizer'
              AND is_active = TRUE
            """,
            (email,)
        ).fetchone()

        if not organizer:
            print(f"Organizer not found: {email}")
            return

        event = conn.execute(
            """
            INSERT INTO events (
                organizer_id,
                title,
                venue,
                event_date,
                status
            )
            VALUES (
                %s, %s, %s,
                NOW() + INTERVAL '30 days',
                'draft'
            )
            RETURNING id, title, organizer_id
            """,
            (organizer[0], title, "SeatLock Test Venue")
        ).fetchone()

    print("\nEvent created:")
    print("Event ID:", event[0])
    print("Title:", event[1])
    print("Organizer ID:", event[2])


if __name__ == "__main__":
    try:
        init_db()

        create_test_event(
            "bahra@gmail.com",
            "Organizer A Test Event"
        )

        create_test_event(
            "alpha@gmail.com",
            "Organizer B Test Event"
        )

    finally:
        close_db()
