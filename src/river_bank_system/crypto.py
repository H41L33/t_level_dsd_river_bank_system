"""
River Bank System - Cryptography Module

This module provides functions for cryptographic operations, specifically for hashing passwords.
"""

import bcrypt


def hash_bcrypt(plaintext: str) -> str:
    """
    Hashes a plaintext string using bcrypt.

    Args:
        plaintext (str): The string to hash.

    Returns:
        str: The resulting bcrypt hash as a decoded string.
    """
    # Generate a salt and hash the plaintext password
    salt = bcrypt.gensalt()
    cipher = bcrypt.hashpw(plaintext.encode('utf-8'), salt)

    # Decode the hash to a string for storage
    return cipher.decode('utf-8')