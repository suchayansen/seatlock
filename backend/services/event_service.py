
from backend.config.database import get_db


def get_manageable_event(event_id, user):
    """
    Return an event only if:
    1. The user is an admin, OR
    2. The user is the organizer who owns the event.

    Return None if access is not permitted or event doesn't exist.
    """

    if not user.is_authenticated:
        return None

    if user.role not in ("admin", "organizer"):
        return None

    pool = get_db()

    with pool.connection() as conn:
        event = conn.execute(
            """
            SELECT id, organizer_id, title, status
            FROM events
            WHERE id = %s
              AND (
                  %s = 'admin'
                  OR organizer_id = %s
              )
            """,
            (event_id, user.role, user.id)
        ).fetchone()

    return event
