"""
River Bank System - Authentication Module

This module provides functions for user authentication, specifically for checking passwords.
"""

import bcrypt


def check_password(input_password_plaintext: str, target_password_hash: str) -> bool:
    """
    Verifies a plaintext password against a stored bcrypt hash.

    Args:
        input_password_plaintext (str): The plaintext password to check.
        target_password_hash (str): The stored bcrypt hash to compare against.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    # Encode the stored hash and the plaintext password to bytes for bcrypt
    stored_hash = target_password_hash.encode('utf-8')
    input_bytes = input_password_plaintext.encode('utf-8')

    # Use bcrypt to check if the passwords match
    return bcrypt.checkpw(input_bytes, stored_hash)