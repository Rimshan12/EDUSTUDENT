from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url


def ensure_database(uri):
    url = make_url(uri)
    if not url.drivername.startswith("mysql") or not url.database:
        return
    engine = create_engine(url._replace(database=None))
    try:
        with engine.connect() as conn:
            conn.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{url.database}` "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            )
            conn.commit()
    finally:
        engine.dispose()
