"""
Tests for the transactions module.
"""

import unittest
from unittest.mock import patch, MagicMock
from river_bank_system.transactions import TransactionsDB

class TestTransactionsDB(unittest.TestCase):
    """
    Test suite for the TransactionsDB class.
    """
    @patch('sqlite3.connect')
    def setUp(self, mock_sqlite_connect):
        """Set up a mock TransactionsDB object for testing."""
        # Create a mock for the connection object
        self.mock_conn = MagicMock()
        # The connection's __enter__ method should return the connection itself for the 'with' statement
        self.mock_conn.__enter__.return_value = self.mock_conn

        # Create a single mock for the cursor
        self.mock_cursor = MagicMock()

        # IMPORTANT: Tell the mock connection to return our mock_cursor whenever .cursor() is called
        self.mock_conn.cursor.return_value = self.mock_cursor

        # Make sqlite3.connect return our mock connection
        mock_sqlite_connect.return_value = self.mock_conn

        # Now, we instantiate the class. Its __init__ method will run and call CREATE TABLE.
        self.transactions_db = TransactionsDB()

        # We reset the mock here to clear the record of the CREATE TABLE call.
        # This ensures our tests only care about what happens inside the test methods themselves.
        self.mock_cursor.reset_mock()


    def test_log_transaction(self):
        """Test that a transaction is logged correctly."""
        self.transactions_db.log_transaction("testuser", "deposit", 100.0, "current")

        # Now, this assertion will pass because the cursor used inside log_transaction is our mock_cursor
        self.mock_cursor.execute.assert_called_with(
            "INSERT INTO tbl_transactions (username, transaction_type, amount, account) VALUES (?, ?, ?, ?)",
            ("testuser", "deposit", 100.0, "current")
        )

    def test_get_transactions(self):
        """Test retrieving transactions for a user."""
        # Set up a mock return value for the fetchall method
        self.mock_cursor.fetchall.return_value = [
            (1, 'testuser', 'deposit', 100.0, 'current', '2023-10-27 10:00:00')
        ]

        # Call the method to get transactions
        result = self.transactions_db.get_transactions("testuser")

        # This assertion will also now pass
        self.mock_cursor.execute.assert_called_with(
            "SELECT * FROM tbl_transactions WHERE username = ? AND timestamp >= date('now', '-7 days') ORDER BY timestamp DESC",
            ("testuser",)
        )

        # Verify that the result matches the mock return value
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "testuser")

if __name__ == '__main__':
    unittest.main()