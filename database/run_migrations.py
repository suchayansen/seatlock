
import os
import psycopg
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

BASE_DIR = Path(__file__).parent
MIGRATIONS_DIR = BASE_DIR / "migrations"


def run_migration(file_path):

    sql = file_path.read_text(encoding="utf-8")

    with psycopg.connect(DATABASE_URL) as conn:

        conn.execute(sql)

    print(f"Migration successful: {file_path.name}")


if __name__ == "__main__":

    migration = MIGRATIONS_DIR / "012_fix_audit_shards.sql"

    run_migration(migration)
