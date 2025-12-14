
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config import Config

# Create engine and session factory (do NOT import app.db here)
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

def wait_for_db(max_tries: int = 30, delay: float = 2.0):
    """Wait until DB is reachable to avoid startup races."""
    for attempt in range(1, max_tries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Database is reachable.")
            return
        except OperationalError as e:
            print(f"⏳ DB not ready (try {attempt}/{max_tries}): {e}")
            time.sleep(delay)
