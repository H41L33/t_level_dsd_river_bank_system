"""
River Bank System - Configuration Module

This module provides a configuration class that loads settings from a .env file.
"""

import os
from dotenv import load_dotenv


class Config:
    """
    Configuration class for the River Bank System.

    Loads database paths, bcrypt settings, and locale information from a .env file.
    """
    def __init__(self) -> None:
        """
        Initializes the Config class by loading environment variables.
        """
        load_dotenv()
        self.DATABASE_PATH = os.getenv('DATABASE_PATH')
        self.BCRYPT_ROUNDS = int(os.getenv('BCRYPT_ROUNDS', 12))
        self.LOCALE = os.getenv('LOCALE', 'en_US.UTF-8')