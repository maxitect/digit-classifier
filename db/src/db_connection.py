import os
import logging
from psycopg_pool import ConnectionPool

logger = logging.getLogger(__name__)

# Use DATABASE_URL environment variable or fallback to a default connection string.
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost:5432/mydatabase")

pool = None

def init_pool(min_size: int = 1, max_size: int = 10):
    """
    Initialise the database connection pool.
    """
    global pool
    try:
        pool = ConnectionPool(DATABASE_URL, min_size=min_size, max_size=max_size)
        logger.info("Database connection pool created successfully.")
    except Exception as e:
        logger.error(f"Failed to create database connection pool: {e}")
        raise

def get_connection():
    """
    Get a connection from the pool. Initialise the pool if it doesn't exist.
    """
    global pool
    if pool is None:
        init_pool()
    try:
        conn = pool.getconn()
        return conn
    except Exception as e:
        logger.error(f"Error obtaining a connection from the pool: {e}")
        raise

def execute_query(query: str, params: tuple = None):
    """
    Execute a database query using a pooled connection.
    For SELECT queries, returns fetched results.
    For other queries, commits the transaction.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            # If the query is a SELECT, fetch and return results.
            if query.strip().upper().startswith("SELECT"):
                result = cur.fetchall()
            else:
                conn.commit()
                result = None
        return result
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)

def close_pool():
    """
    Close all connections in the pool.
    """
    global pool
    if pool:
        pool.closeall()
        logger.info("Database connection pool closed.")
