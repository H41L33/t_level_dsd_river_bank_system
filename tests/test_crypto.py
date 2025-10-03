"""
Tests for the crypto module.
"""

import unittest
import bcrypt
from river_bank_system.crypto import hash_bcrypt

class TestCrypto(unittest.TestCase):
    """
    Test suite for the cryptography functions.
    """
    def test_hash_bcrypt(self):
        """Test that bcrypt hashing produces a valid hash."""
        password = "my_secure_password"
        hashed = hash_bcrypt(password)
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')))

if __name__ == '__main__':
    unittest.main()