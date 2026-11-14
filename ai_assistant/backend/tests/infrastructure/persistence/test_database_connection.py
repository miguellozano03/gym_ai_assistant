from sqlalchemy import text

from app.infrastructure.persistence.database import engine


def test_database_connection():
    with engine.connect() as connection:
        assert connection.execute(text("SELECT 1")).scalar_one() == 1
