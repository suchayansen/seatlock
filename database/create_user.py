
import getpass

from psycopg.errors import UniqueViolation

from backend.config.database import init_db, get_db, close_db
from backend.auth.utils import hash_password


def create_user():
    print("\n=== SeatLock Account Creation ===")

    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip().lower()
    role = input("Enter role (admin/organizer/student): ").strip().lower()

    if not name or not email or "@" not in email:
        print("Invalid name or email.")
        return

    if role not in ("admin", "organizer", "student"):
        print("Invalid role.")
        return

    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    if len(password) < 12:
        print("Password must be at least 12 characters.")
        return

    password_hash = hash_password(password)

    init_db()

    try:
        pool = get_db()

        with pool.connection() as conn:
            result = conn.execute(
                """
                INSERT INTO users (name, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (name, email, password_hash, role)
            ).fetchone()

        print("\nAccount created successfully!")
        print("User ID:", result[0])
        print("Email:", email)
        print("Role:", role)

    except UniqueViolation:
        print("An account with this email already exists.")

    finally:
        close_db()


if __name__ == "__main__":
    create_user()
