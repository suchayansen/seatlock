
import os

from flask import Flask
from dotenv import load_dotenv

from backend.extensions import login_manager
from backend.config.database import init_db, get_db, close_db
from backend.models.user import User
from backend.routes.auth_routes import auth

load_dotenv()


@login_manager.user_loader
def load_user(user_id):
    """Retrieve an authenticated user from PostgreSQL."""

    pool = get_db()

    with pool.connection() as conn:
        user_data = conn.execute(
            """
            SELECT id, name, email, role, is_active
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        ).fetchone()

    if not user_data:
        return None

    user_id, name, email, role, is_active = user_data

    if not is_active:
        return None

    return User(
        id=user_id,
        name=name,
        email=email,
        role=role,
        is_active=is_active
    )


def create_app():

    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    if not app.config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY missing")

    # Initialize Flask-Login
    login_manager.init_app(app)
    app.register_blueprint(auth)

    # Initialize PostgreSQL
    init_db()

    # Home route
    @app.route("/")
    def home():
        return """
        <h1>Welcome to SeatLock</h1>
        <p>Secure Event Seat Booking Platform</p>
        <p>Flask is running successfully!</p>
        <p>Supabase PostgreSQL is connected!</p>
        """

    return app
