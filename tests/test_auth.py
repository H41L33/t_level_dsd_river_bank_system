"""
Tests for the auth module.
"""

import unittest
import bcrypt
from river_bank_system.auth import check_password

class TestAuth(unittest.TestCase):
    """
    Test suite for the authentication functions.
    """
    def test_check_password(self):
        """Test that password checking works correctly."""
        password = "test_password"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.assertTrue(check_password(password, hashed_password))
        self.assertFalse(check_password("wrong_password", hashed_password))

if __name__ == '__main__':
    unittest.main()