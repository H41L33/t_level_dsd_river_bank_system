"""
Tests for the actions module.
"""

import unittest
from unittest.mock import MagicMock, patch
from river_bank_system.actions import Actions

class TestActions(unittest.TestCase):
    """
    Test suite for the Actions class.
    """
    @patch('river_bank_system.users.UsersDB')
    @patch('river_bank_system.transactions.TransactionsDB')
    def setUp(self, mock_transactions_db, mock_users_db):
        """Set up a mock Actions object for testing."""
        self.mock_users_db = mock_users_db.return_value
        self.mock_transactions_db = mock_transactions_db.return_value
        self.actions = Actions('testuser')
        self.actions.accounts_db = self.mock_users_db
        self.actions.transactions_db = self.mock_transactions_db

    def test_deposit_into_account_current(self):
        """Test depositing into the current account."""
        self.actions.deposit_into_account(100.0, 'current')
        self.mock_users_db.add_current_balance.assert_called_with('testuser', 100.0)
        self.mock_transactions_db.log_transaction.assert_called_with('testuser', 'deposit', 100.0, 'current')

    def test_deposit_into_account_savings(self):
        """Test depositing into the savings account."""
        self.actions.deposit_into_account(150.0, 'savings')
        self.mock_users_db.add_savings_balance.assert_called_with('testuser', 150.0)
        self.mock_transactions_db.log_transaction.assert_called_with('testuser', 'deposit', 150.0, 'savings')

    def test_deposit_negative_value(self):
        """Test that depositing a negative value raises a ValueError."""
        with self.assertRaises(ValueError):
            self.actions.deposit_into_account(-50.0, 'current')

    def test_withdraw_from_account_current(self):
        """Test withdrawing from the current account."""
        self.actions.withdraw_from_account(50.0, 'current')
        self.mock_users_db.add_current_balance.assert_called_with('testuser', -50.0)
        self.mock_transactions_db.log_transaction.assert_called_with('testuser', 'withdraw', 50.0, 'current')

    def test_transfer_between_accounts_current_to_savings(self):
        """Test transferring from current to savings."""
        self.actions.transfer_between_accounts(75.0, 'current')
        self.mock_users_db.add_current_balance.assert_called_with('testuser', -75.0)
        self.mock_users_db.add_savings_balance.assert_called_with('testuser', 75.0)
        self.mock_transactions_db.log_transaction.assert_called_with('testuser', 'transfer', 75.0, 'current_to_savings')

if __name__ == '__main__':
    unittest.main()