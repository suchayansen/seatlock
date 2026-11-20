
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from backend.config.database import init_db, get_db, close_db
from backend.services.booking_service import hold_seats


EVENT_ID = "bf02b856-9122-47f2-adac-3ef927639a96"
SEAT_NUMBER = "A3"

barrier = Barrier(2)


def attempt_hold(student_id, seat_id):
    barrier.wait()

    try:
        return hold_seats(
            student_id=student_id,
            event_id=EVENT_ID,
            seat_ids=[seat_id]
        )
    except Exception as exc:
        return {"success": False, "error": str(exc)}


if __name__ == "__main__":
    try:
        init_db()
        pool = get_db()

        with pool.connection() as conn:
            student_a = conn.execute(
                "SELECT id FROM users WHERE email = %s",
                ("abc@gmail.com",)
            ).fetchone()

            student_b = conn.execute(
                "SELECT id FROM users WHERE email = %s",
                ("studentb@test.com",)
            ).fetchone()

            seat = conn.execute(
                """
                SELECT id, status FROM seats
                WHERE event_id = %s AND seat_number = %s
                """,
                (EVENT_ID, SEAT_NUMBER)
            ).fetchone()

        if not student_a or not student_b or not seat:
            raise RuntimeError("Test users or seat not found")

        if seat[1] != "available":
            raise RuntimeError(f"A3 is not available: {seat[1]}")

        print("Starting simultaneous requests for A3...")

        with ThreadPoolExecutor(max_workers=2) as executor:
            future_a = executor.submit(
                attempt_hold, student_a[0], seat[0]
            )
            future_b = executor.submit(
                attempt_hold, student_b[0], seat[0]
            )

            result_a = future_a.result()
            result_b = future_b.result()

        print("\nStudent A:", result_a)
        print("\nStudent B:", result_b)

        successes = sum(
            result.get("success") is True
            for result in (result_a, result_b)
        )

        print("\nSuccessful holds:", successes)
        print("Expected: exactly 1")

    finally:
        close_db()
