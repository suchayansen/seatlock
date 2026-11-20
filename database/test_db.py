
import os
import psycopg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check environment variables
print("Checking environment variables...")

print("SUPABASE_URL:", bool(os.getenv("SUPABASE_URL")))
print("SUPABASE_PUBLISHABLE_KEY:", bool(os.getenv("SUPABASE_PUBLISHABLE_KEY")))
print("DATABASE_URL:", bool(os.getenv("DATABASE_URL")))
print("SECRET_KEY:", bool(os.getenv("SECRET_KEY")))

# Test PostgreSQL connection
print("\nTesting PostgreSQL connection...")

try:
    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        result = conn.execute("""
            SELECT
                current_database(),
                current_user,
                NOW()
        """).fetchone()

        print("\nSUCCESS! Connected to Supabase PostgreSQL.")
        print("Database:", result[0])
        print("User:", result[1])
        print("Time:", result[2])

except Exception as e:
    print("\nCONNECTION FAILED:", e)
