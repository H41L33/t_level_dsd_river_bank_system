"""
River Bank System - Users Module

This module provides the UsersDB class to handle all database operations related to users.
"""

import sqlite3
import logging
import river_bank_system.crypto as crypto
import river_bank_system.config as config
from typing import Any


# Define the allowed columns for database queries to prevent SQL injection
ALLOWED_COLUMNS = ('id', 'username', 'display_name', 'password_hash', 'current_balance', 'savings_balance')

class UsersDB:
    """
    A class to handle the user database operations for the river bank system.
    """
    def __init__(self) -> None:
        """
        Initializes the UsersDB class.
        """
        config_obj = config.Config()
        self.logger = logging.getLogger(__name__)

        self.db_object = sqlite3.connect(config_obj.DATABASE_PATH)
        self.db_cursor = self.db_object.cursor()
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                display_name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                current_balance REAL,
                savings_balance REAL
            )
        ''')

    def __enter__(self) -> Any:
        """
        Context manager entry method.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit method.
        """
        self.close_db()

    def close_db(self) -> None:
        """
        Commits changes and closes the database connection.
        """
        self.db_object.commit()
        self.db_object.close()

    def create_new_user(self, username: str, display_name: str, password: str, current_balance: float, savings_balance: float) -> None:
        """
        Creates a new user in the database.

        Args:
            username (str): The new user's username.
            display_name (str): The new user's display name.
            password (str): The new user's plaintext password.
            current_balance (float): The starting balance for the current account.
            savings_balance (float): The starting balance for the savings account.
        """
        try:
            with self.db_object as connection:
                cursor = connection.cursor()
                password_hash = crypto.hash_bcrypt(password)
                cursor.execute(
                    "INSERT INTO tbl_accounts (username, display_name, password_hash, current_balance, savings_balance) VALUES (?, ?, ?, ?, ?)",
                    (username, display_name, password_hash, current_balance, savings_balance)
                )
        except sqlite3.OperationalError as error:
            self.logger.error(error)

    def get_column_from_username(self, column: str, target_username: str) -> Any | None:
        """
        Retrieves a specific column for a user from the database.

        Args:
            column (str): The name of the column to retrieve.
            target_username (str): The username of the user to query.

        Returns:
            Any | None: The data from the specified column, or None if not found.
        """
        if column not in ALLOWED_COLUMNS:
            raise ValueError(f"Disallowed column: {column}")

        try:
            with self.db_object as connection:
                cursor = connection.cursor()
                cursor.execute(f"SELECT {column} FROM tbl_accounts WHERE username = ?", (target_username,))
                row = cursor.fetchone()

            if row:
                return row[0]
            else:
                self.logger.warning(f"No user found with username: {target_username}")
                return None
        except sqlite3.OperationalError as error:
            self.logger.error(error)
            return None

    def set_column_from_username(self, column: str, target_username: str, new_data: Any) -> None:
        """
        Updates a specific column for a user in the database.

        Args:
            column (str): The name of the column to update.
            target_username (str): The username of the user to update.
            new_data (Any): The new data to set for the column.
        """
        if column not in ALLOWED_COLUMNS:
            raise ValueError(f"Disallowed column: {column}")

        try:
            with self.db_object as connection:
                cursor = connection.cursor()
                # Use a parameterized query to prevent SQL injection
                cursor.execute(f"UPDATE tbl_accounts SET {column} = ? WHERE username = ?", (new_data, target_username))
        except sqlite3.OperationalError as error:
            self.logger.error(error)

    def get_password_hash(self, username: str) -> str | None:
        """Retrieves the password hash for a given username."""
        return self.get_column_from_username('password_hash', username)

    def get_current_balance(self, username: str) -> float:
        """Retrieves the current account balance for a given username."""
        return float(self.get_column_from_username('current_balance', username))

    def get_savings_balance(self, username: str) -> float:
        """Retrieves the savings account balance for a given username."""
        return float(self.get_column_from_username('savings_balance', username))

    def get_account_number(self, username: str) -> int:
        """Retrieves the account number (ID) for a given username."""
        return int(self.get_column_from_username('id', username))

    def get_user_exists(self, username: str) -> bool:
        """Checks if a user exists in the database."""
        return self.get_column_from_username('username', username) is not None

    def add_current_balance(self, username: str, balance: float) -> None:
        """
        Adds an amount to the current account balance for a user.

        Args:
            username (str): The user's username.
            balance (float): The amount to add (can be negative for withdrawals).
        """
        previous_balance = self.get_current_balance(username)
        new_balance = previous_balance + balance
        self.set_column_from_username('current_balance', username, new_balance)

    def add_savings_balance(self, username: str, balance: float) -> None:
        """
        Adds an amount to the savings account balance for a user.

        Args:
            username (str): The user's username.
            balance (float): The amount to add (can be negative for withdrawals).
        """
        previous_balance = self.get_savings_balance(username)
        new_balance = previous_balance + balance
        self.set_column_from_username('savings_balance', username, new_balance)