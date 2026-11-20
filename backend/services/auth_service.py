from backend.config.database import get_db
from backend.auth.utils import verify_password
from backend.models.user import User


def authenticate_user(email, password):

    email = email.strip().lower()

    pool = get_db()

    with pool.connection() as conn:

        user_data = conn.execute(
            """
            SELECT
                id,
                name,
                email,
                password_hash,
                role,
                is_active
            FROM users
            WHERE LOWER(email) = %s
            LIMIT 1
            """,
            (email,)
        ).fetchone()

    if not user_data:
        return None

    user_id, name, email, password_hash, role, is_active = user_data

    if not is_active:
        return None

    if not verify_password(password, password_hash):
        return None

    return User(
        id=user_id,
        name=name,
        email=email,
        role=role,
        is_active=is_active
    )