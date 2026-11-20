
import os
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

pool = None


def init_db():
    global pool

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL missing")

    pool = ConnectionPool(
        conninfo=DATABASE_URL,
        min_size=1,
        max_size=5,
        open=False
    )

    pool.open()
    pool.wait()

    print("Database pool initialized!")


def get_db():
    if pool is None:
        raise RuntimeError("Database not initialized")

    return pool


def close_db():
    if pool is not None:
        pool.close()
