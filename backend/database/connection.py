import logging
from contextlib import contextmanager
import mysql.connector
from mysql.connector import pooling
from mysql.connector.errors import Error

from backend.core.config import settings

logger = logging.getLogger(__name__)

# Parse database settings. Since config.py currently has a SQLAlchemy URI,
# we need to parse it or assume standard env vars. Let's assume standard
# parsing of the DATABASE_URL format or fallbacks.
# For a production setup with mysql-connector-python, we extract parameters.

def _get_db_config():
    # Attempt to parse sqlalchemy-style URL or provide defaults
    db_url = settings.database_url
    try:
        # e.g., mysql+mysqlconnector://root:root@localhost:3306/cricinsight
        if "://" in db_url:
            creds, host_db = db_url.split("://")[1].split("@")
            user, password = creds.split(":")
            host_port, database = host_db.split("/")
            if ":" in host_port:
                host, port = host_port.split(":")
            else:
                host = host_port
                port = 3306
            return {
                "host": host,
                "port": int(port),
                "user": user,
                "password": password,
                "database": database
            }
    except Exception as e:
        logger.warning(f"Failed to parse database_url. Using defaults. Error: {e}")
        
    return {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "password",
        "database": "cricinsight"
    }

try:
    db_config = _get_db_config()
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="cricinsight_pool",
        pool_size=5,
        pool_reset_session=True,
        **db_config
    )
    logger.info("MySQL connection pool created successfully.")
except Error as e:
    logger.error(f"Error while creating MySQL connection pool: {e}")
    connection_pool = None

@contextmanager
def get_db_connection():
    """
    Context manager to yield a database connection from the pool.
    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(...)
    """
    if connection_pool is None:
        raise RuntimeError("Database connection pool is not initialized.")
    
    connection = None
    try:
        connection = connection_pool.get_connection()
        yield connection
    except Error as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()
