
from backend.config.database import init_db, close_db
from backend.services.booking_service import confirm_hold

HOLD_ID = "d521e941-a8f6-4b84-8caa-bde0b114a0fe"
STUDENT_ID = "d5083dfa-fee0-409c-b2bd-488c5ac0da04"

if __name__ == "__main__":
    try:
        init_db()

        result = confirm_hold(
            hold_id=HOLD_ID,
            student_id=STUDENT_ID
        )

        print("\nConfirmation result:")
        print(result)

    finally:
        close_db()
