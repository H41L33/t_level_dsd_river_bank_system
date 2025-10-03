"""
River Bank System - Account Actions Module

This module provides the Actions class which handles all banking operations
including deposits, withdrawals, and transfers between current and savings accounts.
"""

import river_bank_system.users as users
import river_bank_system.transactions as transactions
import logging
from typing import Any


class Actions:
    """
    A class to handle banking operations for the river bank system.

    This class provides methods for depositing money into accounts, withdrawing money
    from accounts, and transferring money between current and savings accounts.
    It maintains a connection to the users database and includes proper logging.

    Attributes:
        accounts_db (users.UsersDB): Database connection for user account operations.
        transactions_db (transactions.TransactionsDB): Database connection for logging transactions.
        logger (logging.Logger): Logger instance for this module.
    """

    def __init__(self, username: str) -> None:
        """
        Initialize the Actions class.

        Sets up the database connection and logger for banking operations.
        """
        self.username = username
        # Initialize database connection for user account operations
        self.accounts_db = users.UsersDB()
        self.transactions_db = transactions.TransactionsDB()

        # Set up logger for this module
        self.logger = logging.getLogger(__name__)

    def __enter__(self) -> Any:
        """
        Context manager entry method.

        Returns:
            Actions: The Actions instance for use in with statements.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit method to ensure proper cleanup.

        Args:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Exception traceback if an exception occurred.
        """
        # Ensure database connection is properly closed
        self.accounts_db.close_db()
        self.transactions_db.close_db()

    def deposit_into_account(self, value: float, target_account: str) -> None:
        """
        Deposit money into a specified account.

        Args:
            value (float): The amount to deposit (must be positive).
            target_account (str): The target account type ('current' or 'savings').

        Raises:
            ValueError: If target_account is not 'current' or 'savings'.
            ValueError: If value is negative or zero.
        """
        # Validate input parameters
        if value <= 0:
            raise ValueError("Deposit amount must be positive")

        if target_account not in ['current', 'savings']:
            raise ValueError("target_account must be 'current' or 'savings'")

        # Deposit into current account
        if target_account == 'current':
            self.accounts_db.add_current_balance(self.username, value)
            self.transactions_db.log_transaction(self.username, "deposit", value, "current")
            self.logger.info(f"Deposited {value} into current account for user {self.username}")

        # Deposit into savings account
        elif target_account == 'savings':
            self.accounts_db.add_savings_balance(self.username, value)
            self.transactions_db.log_transaction(self.username, "deposit", value, "savings")
            self.logger.info(f"Deposited {value} into savings account for user {self.username}")

    def withdraw_from_account(self, value: float, target_account: str) -> None:
        """
        Withdraw money from a specified account.

        Args:
            value (float): The amount to withdraw (must be positive).
            target_account (str): The target account type ('current' or 'savings').

        Raises:
            ValueError: If target_account is not 'current' or 'savings'.
            ValueError: If value is negative or zero.
        """
        # Validate input parameters
        if value <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if target_account not in ['current', 'savings']:
            raise ValueError("target_account must be 'current' or 'savings'")

        # Withdraw from current account (add negative value)
        if target_account == 'current':
            self.accounts_db.add_current_balance(self.username, -value)
            self.transactions_db.log_transaction(self.username, "withdraw", value, "current")
            self.logger.info(f"Withdrew {value} from current account for user {self.username}")

        # Withdraw from savings account (add negative value)
        elif target_account == 'savings':
            self.accounts_db.add_savings_balance(self.username, -value)
            self.transactions_db.log_transaction(self.username, "withdraw", value, "savings")
            self.logger.info(f"Withdrew {value} from savings account for user {self.username}")

    def transfer_between_accounts(self, value: float, source_account: str) -> None:
        """
        Transfer money between current and savings accounts for the same user.

        Args:
            value (float): The amount to transfer (must be positive).
            source_account (str): The source account type ('current' or 'savings').

        Raises:
            ValueError: If source_account is not 'current' or 'savings'.
            ValueError: If value is negative or zero.
        """
        # Validate input parameters
        if value <= 0:
            raise ValueError("Transfer amount must be positive")

        if source_account not in ['current', 'savings']:
            raise ValueError("source_account must be 'current' or 'savings'")

        # Transfer from current to savings
        if source_account == 'current':
            # Deduct from current account
            self.accounts_db.add_current_balance(self.username, -value)
            # Add to savings account
            self.accounts_db.add_savings_balance(self.username, value)
            self.transactions_db.log_transaction(self.username, "transfer", value, "current_to_savings")
            self.logger.info(f"Transferred {value} from current to savings for user {self.username}")

        # Transfer from savings to current
        elif source_account == 'savings':
            # Add to current account
            self.accounts_db.add_current_balance(self.username, value)
            # Deduct from savings account
            self.accounts_db.add_savings_balance(self.username, -value)
            self.transactions_db.log_transaction(self.username, "transfer", value, "savings_to_current")
            self.logger.info(f"Transferred {value} from savings to current for user {self.username}")