from db.src.db import (
    execute_query,
    get_connection,
    return_connection,
    close_all_connections
)
import db.src.db as db_module  # Import the module itself
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create mock objects to be used in tests
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value.__enter__.return_value = (
            self.mock_cursor
        )

        # Reset mock cursor between tests
        self.mock_cursor.reset_mock()

    @patch('db.src.db._connection_pool', [])
    @patch('db.src.db._initialized', True)
    @patch('db.src.db.psycopg.connect')
    def test_get_connection(self, mock_connect):
        # Mock the connection
        mock_connect.return_value = self.mock_conn

        # Test getting a new connection when the pool is empty
        conn = get_connection()
        self.assertEqual(conn, self.mock_conn)
        mock_connect.assert_called_once()

    @patch('db.src.db._connection_pool')
    @patch('db.src.db._initialized', True)
    def test_return_connection(self, mock_pool):
        # Setup the pool mock
        mock_pool.__len__.return_value = 0  # Empty pool

        # Test returning a working connection
        return_connection(self.mock_conn)

        # Verify connection test was performed
        self.mock_cursor.execute.assert_called_with("SELECT 1")

        # Verify connection was added to pool
        mock_pool.append.assert_called_once_with(self.mock_conn)

    @patch('db.src.db.get_connection')
    @patch('db.src.db.return_connection')
    def test_execute_query_select(self, mock_return, mock_get):
        # Setup mocks
        mock_get.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = [(1,)]

        # Test SELECT query
        result = execute_query("SELECT 1 as test")

        # Verify query execution
        self.mock_cursor.execute.assert_called_with("SELECT 1 as test", None)
        self.mock_cursor.fetchall.assert_called_once()
        self.assertEqual(result, [(1,)])
        mock_return.assert_called_once_with(self.mock_conn)

    @patch('db.src.db.get_connection')
    @patch('db.src.db.return_connection')
    def test_execute_query_insert(self, mock_return, mock_get):
        # Setup mocks
        mock_get.return_value = self.mock_conn

        # Test INSERT query
        result = execute_query("INSERT INTO table VALUES (1)")

        # Verify query execution
        self.mock_cursor.execute.assert_called_with(
            "INSERT INTO table VALUES (1)", None)
        self.mock_conn.commit.assert_called_once()
        self.assertIsNone(result)
        mock_return.assert_called_once_with(self.mock_conn)

    def test_close_all_connections(self):
        # Save original values
        original_pool = db_module._connection_pool
        original_initialized = db_module._initialized

        # Setup test conditions
        mock_conn1 = MagicMock()
        mock_conn2 = MagicMock()
        db_module._connection_pool = [mock_conn1, mock_conn2]
        db_module._initialized = True

        try:
            # Call the function to close all connections
            close_all_connections()

            # Verify all connections were closed
            mock_conn1.close.assert_called_once()
            mock_conn2.close.assert_called_once()

            # Check that the module variables were updated correctly
            self.assertEqual(db_module._connection_pool, [])
            self.assertEqual(db_module._initialized, False)
        finally:
            # Restore original values
            db_module._connection_pool = original_pool
            db_module._initialized = original_initialized


if __name__ == "__main__":
    unittest.main()
