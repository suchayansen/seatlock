
from backend.config.database import init_db, close_db
from backend.services.booking_service import hold_seats

STUDENT_ID = "d5083dfa-fee0-409c-b2bd-488c5ac0da04"
EVENT_ID = "bf02b856-9122-47f2-adac-3ef927639a96"

SEAT_IDS = [
    "7985c687-9329-4f28-8ecf-9ec57f8d484e",
    "a3365a4f-e2e0-450b-863c-ab28346a5b39"
]

if __name__ == "__main__":
    try:
        init_db()

        result = hold_seats(
            student_id=STUDENT_ID,
            event_id=EVENT_ID,
            seat_ids=SEAT_IDS
        )

        print("\nHold result:")
        print(result)

    finally:
        close_db()
