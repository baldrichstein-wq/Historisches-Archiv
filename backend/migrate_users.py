import os
import sqlalchemy

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/historisches_archiv")
engine = sqlalchemy.create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT FALSE;"))
        conn.execute(sqlalchemy.text("ALTER TABLE users ADD COLUMN verification_token VARCHAR;"))
        conn.execute(sqlalchemy.text("UPDATE users set is_verified = TRUE;")) # Set existing users to true so they don't get locked out
        conn.commit()
    print("Database migrated successfully.")
except Exception as e:
    print(f"Error during migration: {e}")
