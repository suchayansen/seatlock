
from backend.config.database import init_db, get_db, close_db
from backend.models.user import User
from backend.services.event_service import get_manageable_event


EVENT_A = "bf02b856-9122-47f2-adac-3ef927639a96"
EVENT_B = "cc3c3c29-37cb-4791-a8c2-c1b6f34e5be1"


def get_test_user(email):
    pool = get_db()

    with pool.connection() as conn:
        row = conn.execute(
            """
            SELECT id, name, email, role, is_active
            FROM users
            WHERE LOWER(email) = LOWER(%s)
            """,
            (email,)
        ).fetchone()

    if not row:
        raise RuntimeError(f"User not found: {email}")

    return User(
        id=row[0],
        name=row[1],
        email=row[2],
        role=row[3],
        is_active=row[4]
    )


if __name__ == "__main__":
    try:
        init_db()

        organizer_a = get_test_user("bahra@gmail.com")
        organizer_b = get_test_user("alpha@gmail.com")
        admin = get_test_user("admin@seatlock.test")

        print("\n--- Organizer Ownership Tests ---")

        result_1 = get_manageable_event(EVENT_A, organizer_a)
        print("Organizer A -> Event A:", "ALLOWED" if result_1 else "DENIED")

        result_2 = get_manageable_event(EVENT_B, organizer_a)
        print("Organizer A -> Event B:", "ALLOWED" if result_2 else "DENIED")

        result_3 = get_manageable_event(EVENT_B, organizer_b)
        print("Organizer B -> Event B:", "ALLOWED" if result_3 else "DENIED")

        result_4 = get_manageable_event(EVENT_A, organizer_b)
        print("Organizer B -> Event A:", "ALLOWED" if result_4 else "DENIED")

        print("\n--- Admin Access Tests ---")

        result_5 = get_manageable_event(EVENT_A, admin)
        print("Admin -> Event A:", "ALLOWED" if result_5 else "DENIED")

        result_6 = get_manageable_event(EVENT_B, admin)
        print("Admin -> Event B:", "ALLOWED" if result_6 else "DENIED")

    finally:
        close_db()
