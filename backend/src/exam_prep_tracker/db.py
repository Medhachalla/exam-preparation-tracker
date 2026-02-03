import os
import psycopg2
import logging

logger = logging.getLogger(__name__)


def _get_env(name, default=None):
    return os.getenv(name, default)


def get_connection():
    """Return a new psycopg2 connection using DATABASE_URL or composed POSTGRES_* variables.

    This function avoids failing at import time. If a configuration is missing it raises a clear
    RuntimeError when called so calling code can handle connection failures at runtime.
    """
    database_url = _get_env("DATABASE_URL")

    if not database_url:
        # Compose from individual POSTGRES_* variables
        user = _get_env("POSTGRES_USER")
        password = _get_env("POSTGRES_PASSWORD")
        db = _get_env("POSTGRES_DB")
        host = _get_env("POSTGRES_HOST") or _get_env("POSTGRES_HOSTNAME") or _get_env("POSTGRES_SERVICE")
        port = _get_env("POSTGRES_PORT")

        if not (user and password and db and host):
            raise RuntimeError("DATABASE_URL is not set and POSTGRES_USER/POSTGRES_PASSWORD/POSTGRES_DB/POSTGRES_HOST are not fully configured")

        # Use default Postgres port if not set
        if not port:
            port = "5432"

        database_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        logger.exception("Failed to connect to Postgres: %s", e)
        # Re-raise a RuntimeError to give calling code a predictable exception type
        raise RuntimeError(f"Could not connect to the database: {e}") from e
