"""
Tests for the users module.
"""

import unittest
from unittest.mock import patch, MagicMock
from river_bank_system.users import UsersDB
import river_bank_system.users  # Import the module to patch it directly

class TestUsersDB(unittest.TestCase):
    """
    Test suite for the UsersDB class.
    """
    @patch('sqlite3.connect')
    def setUp(self, mock_sqlite_connect):
        """Set up a mock UsersDB object for testing."""
        # Create a mock for the connection object
        self.mock_conn = MagicMock()
        self.mock_conn.__enter__.return_value = self.mock_conn

        # Create a single mock for the cursor
        self.mock_cursor = MagicMock()

        # Tell the mock connection to return our mock_cursor whenever .cursor() is called
        self.mock_conn.cursor.return_value = self.mock_cursor

        # Make sqlite3.connect return our mock connection
        mock_sqlite_connect.return_value = self.mock_conn

        # Instantiate the class
        self.users_db = UsersDB()

        # Reset the mock to ignore the initial CREATE TABLE call
        self.mock_cursor.reset_mock()

    def test_create_new_user(self):
        """Test creating a new user."""
        # Use patch.object to directly mock the hash_bcrypt function
        # ONLY for the code inside this 'with' block.
        with patch.object(river_bank_system.users.crypto, 'hash_bcrypt', return_value="hashed_password") as mock_hash:
            self.users_db.create_new_user("newuser", "New User", "password123", 100.0, 50.0)

        # Verify the mocked function was called
        mock_hash.assert_called_once_with("password123")

        # Now, this assertion will finally pass
        self.mock_cursor.execute.assert_called_with(
            "INSERT INTO tbl_accounts (username, display_name, password_hash, current_balance, savings_balance) VALUES (?, ?, ?, ?, ?)",
            ("newuser", "New User", "hashed_password", 100.0, 50.0)
        )

    def test_get_column_from_username(self):
        """Test retrieving a column from a username."""
        self.mock_cursor.fetchone.return_value = ("test_data",)

        result = self.users_db.get_column_from_username("display_name", "testuser")

        self.mock_cursor.execute.assert_called_with("SELECT display_name FROM tbl_accounts WHERE username = ?", ("testuser",))
        self.assertEqual(result, "test_data")

    def test_get_column_from_username_disallowed_column(self):
        """Test that a ValueError is raised for a disallowed column."""
        with self.assertRaises(ValueError):
            self.users_db.get_column_from_username("invalid_column", "testuser")

    def test_add_current_balance(self):
        """Test adding to the current balance."""
        with patch.object(self.users_db, 'get_current_balance', return_value=100.0) as mock_get:
            with patch.object(self.users_db, 'set_column_from_username') as mock_set:
                self.users_db.add_current_balance("testuser", 50.0)

                mock_get.assert_called_with("testuser")
                mock_set.assert_called_with('current_balance', 'testuser', 150.0)

if __name__ == '__main__':
    unittest.main()