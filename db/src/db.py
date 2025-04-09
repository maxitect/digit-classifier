import os
import logging
import psycopg

logger = logging.getLogger(__name__)

# Use DATABASE_URL env variable or fallback to a default connection string
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/mydatabase")

# Simple connection pool implementation
_connection_pool = []
_pool_size = 5
_initialized = False


def init_db():
    """
    Initialise the database and connection pool.
    """
    global _initialized, _connection_pool

    if _initialized:
        return

    try:
        # Create initial connections for the pool
        for _ in range(_pool_size):
            conn = psycopg.connect(DATABASE_URL)
            _connection_pool.append(conn)

        _initialized = True
        logger.info(
            f"Database initialised with connection pool of {_pool_size}")
    except Exception as e:
        logger.error(f"Failed to initialise database connection pool: {e}")
        raise


def get_connection():
    """
    Get a connection from the pool. If the pool is empty,
    create a new connection.
    """
    global _connection_pool

    if not _initialized:
        init_db()

    if not _connection_pool:
        try:
            # If pool is empty, create a new connection
            return psycopg.connect(DATABASE_URL)
        except Exception as e:
            logger.error(f"Error creating new database connection: {e}")
            raise

    # Take a connection from the pool
    return _connection_pool.pop()


def return_connection(conn):
    """
    Return a connection to the pool if it's still viable.
    """
    global _connection_pool

    if len(_connection_pool) < _pool_size:
        try:
            # Test if connection is still viable
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
            # If no exception occurred, return to pool
            _connection_pool.append(conn)
        except Exception:
            # If connection is broken, close it
            try:
                conn.close()
            except Exception:
                pass


def execute_query(query, params=None):
    """
    Execute a database query using a connection from the pool.
    For SELECT queries, returns fetched results.
    For other queries, commits the transaction.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)

            # If the query is a SELECT, fetch and return results
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
        return_connection(conn)


def close_all_connections():
    """
    Close all connections in the pool.
    """
    global _connection_pool, _initialized

    for conn in _connection_pool:
        try:
            conn.close()
        except Exception as e:
            logger.error(f"Error closing connection: {e}")

    _connection_pool = []
    _initialized = False
    logger.info("All database connections closed.")
