"""
River Bank System - Transactions Module

This module provides the TransactionsDB class to handle all transaction logging operations.
"""

import sqlite3
import logging
import river_bank_system.config as config
from typing import Any


class TransactionsDB:
    """
    A class to handle the transactions database operations.
    """
    def __init__(self) -> None:
        """
        Initializes the TransactionsDB class.
        """
        config_obj = config.Config()
        self.logger = logging.getLogger(__name__)

        self.db_object = sqlite3.connect(config_obj.DATABASE_PATH)
        self.db_cursor = self.db_object.cursor()
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                account TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
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

    def log_transaction(self, username: str, transaction_type: str, amount: float, account: str) -> None:
        """
        Logs a transaction in the database.

        Args:
            username (str): The username of the user performing the transaction.
            transaction_type (str): The type of transaction (e.g., 'deposit', 'withdraw').
            amount (float): The transaction amount.
            account (str): The account involved in the transaction.
        """
        try:
            with self.db_object as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO tbl_transactions (username, transaction_type, amount, account) VALUES (?, ?, ?, ?)",
                    (username, transaction_type, amount, account)
                )
        except sqlite3.OperationalError as error:
            self.logger.error(error)

    def get_transactions(self, username: str) -> list[tuple[Any, ...]]:
        """
        Retrieves the last 7 days of transactions for a user.

        Args:
            username (str): The username to retrieve transactions for.

        Returns:
            List[Tuple[Any, ...]]: A list of transactions.
        """
        try:
            with self.db_object as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT * FROM tbl_transactions WHERE username = ? AND timestamp >= date('now', '-7 days') ORDER BY timestamp DESC",
                    (username,)
                )
                return cursor.fetchall()
        except sqlite3.OperationalError as error:
            self.logger.error(error)
            return []