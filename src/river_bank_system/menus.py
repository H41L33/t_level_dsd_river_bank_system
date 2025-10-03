"""
River Bank System - Menus Module

This module provides all the command-line interface menus and prompts for the application.
"""

import click
import river_bank_system.auth as auth
import river_bank_system.users as users
from enum import Enum


class ProgramStartAction(Enum):
    """Enumeration for the initial program actions."""
    LOGIN = 1
    CREATE_USER = 2
    QUIT = 3

class AccountActions(Enum):
    """Enumeration for the actions available in the account dashboard."""
    DEPOSIT = 1
    WITHDRAW = 2
    TRANSFER = 3
    TRANSACTION_LOG = 4
    LOGOUT = 5

def format_currency(value: float) -> str:
    """
    Formats a float value as a currency string.

    Args:
        value (float): The value to format.

    Returns:
        str: The formatted currency string (e.g., £1,234.56).
    """
    return "£{:,.2f}".format(value)

def program_start() -> ProgramStartAction | None:
    """
    Displays the initial program start menu and gets the user's choice.

    Returns:
        Optional[ProgramStartAction]: The action selected by the user, or None.
    """
    click.clear()
    click.secho('Welcome to River Bank!', fg='cyan')
    click.echo('\t (l)ogin to existing account.')
    click.echo('\t (r)egister a new account.')
    click.echo('\t (q)uit the application.')

    allowed_actions: tuple[str, ...] = ('l', 'r', 'q')
    input_index = action_prompt(allowed_actions)

    match input_index:
        case 0:
            return ProgramStartAction.LOGIN
        case 1:
            return ProgramStartAction.CREATE_USER
        case 2:
            return ProgramStartAction.QUIT
        case _:
            return None

def login_prompt() -> str | bool:
    """
    Prompts the user for their username and password to log in.

    Returns:
        str | bool: The username if the login is successful, otherwise False.
    """
    click.clear()
    input_username = click.prompt("Enter a username", type=str)

    with users.UsersDB() as accounts_db:
        # Check if the user exists before prompting for a password
        if not accounts_db.get_user_exists(input_username):
            return False

        input_password_plain = click.prompt(f"Enter password for {input_username}", type=str)
        target_hash = accounts_db.get_password_hash(input_username)

    if target_hash and auth.check_password(input_password_plain, target_hash):
        return input_username
    else:
        return False

def create_user_prompt() -> str:
    """
    Prompts the user for the information needed to create a new user account.

    Returns:
        str: The username of the newly created user.
    """
    click.clear()
    with users.UsersDB() as accounts_db:
        while True:
            new_username = click.prompt("Create a new username", type=str)
            if len(new_username) >= 3 and new_username.isalnum():
                if not accounts_db.get_user_exists(new_username):
                    break
                else:
                    click.echo("Username already exists. Please choose another.")
            else:
                click.echo("Username must be at least 3 alphanumeric characters long.")

        new_display_name = click.prompt("Create a new display name", type=str)

        while True:
            new_password = click.prompt("Set a new password", type=str)
            if len(new_password) >= 8:
                break
            else:
                click.echo("Password must be at least 8 characters long.")
                continue

        current_balance = click.prompt("Enter starting current account balance", type=float, default=0.0)
        savings_balance = click.prompt("Enter starting savings account balance", type=float, default=0.0)

        accounts_db.create_new_user(new_username, new_display_name, new_password, current_balance, savings_balance)

    return new_username

def string_input(prompt_message: str, valid_options: tuple[str, ...]) -> str:
    """
    Prompts the user for a string input from a list of valid options.

    Args:
        prompt_message (str): The message to display to the user.
        valid_options (tuple[str, ...]): A tuple of valid string options.

    Returns:
        str: The user's valid input.
    """
    while True:
        user_input = click.prompt(f"{prompt_message}", type=str).lower()
        if user_input in valid_options:
            return user_input
        click.echo("Not a valid option, try again.")

def float_input(prompt_message: str) -> float:
    """
    Prompts the user for a float input.

    Args:
        prompt_message (str): The message to display to the user.

    Returns:
        float: The user's float input.
    """
    return click.prompt(f"{prompt_message}", type=float)

def action_prompt(allowed_action_chars: tuple[str, ...]) -> int:
    """
    Prompts the user to enter an action from a tuple of allowed characters.

    Args:
        allowed_action_chars (tuple[str, ...]): A tuple of allowed action characters.

    Returns:
        int: The index of the selected action in the allowed_action_chars tuple.
    """
    while True:
        input_action = click.prompt('Enter an action (the letter in brackets)', type=str)
        if input_action in allowed_action_chars:
            return allowed_action_chars.index(input_action)
        click.echo('Invalid action. Try again.')

def account_dashboard(username: str) -> AccountActions | None:
    """
    Displays the main account dashboard with balances and available actions.

    Args:
        username (str): The username of the logged-in user.

    Returns:
        Optional[AccountActions]: The action selected by the user, or None.
    """
    with users.UsersDB() as accounts_db:
        click.clear()
        click.echo(click.style(f"Welcome, {username}! ☀️", fg='green'))
        account_number = accounts_db.get_account_number(username)
        current_account_balance = accounts_db.get_current_balance(username)
        savings_account_balance = accounts_db.get_savings_balance(username)

    click.echo(f"Your account number: {account_number}")
    click.echo(f"\t Your current account balance: {click.style(format_currency(current_account_balance), fg='green')}")
    click.echo(f"\t Your savings account balance: {click.style(format_currency(savings_account_balance), fg='green')}")
    click.echo('\nActions')
    click.echo('\t (d)eposit money into an account.')
    click.echo('\t (w)ithdraw money from an account.')
    click.echo('\t (t)ransfer money between my accounts.')
    click.echo('\t (v)iew recent transactions.')
    click.echo('\t (l)ogout.')

    allowed_actions: tuple[str, ...] = ('d', 'w', 't', 'v', 'l')
    input_index = action_prompt(allowed_actions)

    match input_index:
        case 0:
            return AccountActions.DEPOSIT
        case 1:
            return AccountActions.WITHDRAW
        case 2:
            return AccountActions.TRANSFER
        case 3:
            return AccountActions.TRANSACTION_LOG
        case 4:
            return AccountActions.LOGOUT
        case _:
            return None