"""
River Bank System - Main Application

This module serves as the main entry point for the River Bank System application.
It orchestrates the user interface flow, including login, user creation, and account actions.
"""

import river_bank_system.menus as menus
import river_bank_system.config as config
import river_bank_system.actions as actions
import river_bank_system.transactions as transactions
import locale
import logging
import click


# Define valid account types
VALID_ACCOUNTS = ("current", "savings")

def home_page(username: str) -> None:
    """
    Displays the user's account dashboard and handles all account actions.

    Args:
        username (str): The username of the logged-in user.
    """
    while True:
        # Show the account dashboard and get the user's desired action
        user_action = menus.account_dashboard(username)

        with actions.Actions(username) as bank_actions:
            # Match the user's action to the corresponding function
            match user_action:
                case menus.AccountActions.DEPOSIT:
                    # Get deposit details from the user
                    input_account = menus.string_input("Account to deposit into (current, savings)", VALID_ACCOUNTS).lower()
                    input_value = menus.float_input("Amount to deposit")
                    # Perform the deposit
                    bank_actions.deposit_into_account(input_value, input_account)

                case menus.AccountActions.WITHDRAW:
                    # Get withdrawal details from the user
                    input_account = menus.string_input("Account to withdraw from (current, savings)", VALID_ACCOUNTS).lower()
                    input_value = menus.float_input("Amount to withdraw")
                    # Perform the withdrawal
                    bank_actions.withdraw_from_account(input_value, input_account)

                case menus.AccountActions.TRANSFER:
                    # Get transfer details from the user
                    input_account = menus.string_input("Account to transfer from (current, savings)", VALID_ACCOUNTS).lower()
                    input_value = menus.float_input("Amount to transfer")
                    # Perform the transfer
                    bank_actions.transfer_between_accounts(input_value, input_account)

                case menus.AccountActions.TRANSACTION_LOG:
                    # Display the user's transaction history
                    with transactions.TransactionsDB() as trans_db:
                        logs = trans_db.get_transactions(username)
                        click.echo("Transactions in the last 7 days:")
                        for log in logs:
                            click.echo(f"- {log[2]} of £{log[3]} on account '{log[4]}' at {log[5]}")

                case menus.AccountActions.LOGOUT:
                    # Exit the home page loop to log the user out
                    break

                case _:
                    # Continue the loop if no valid action is selected
                    continue

def main() -> None:
    """
    The main function of the application.

    Handles the initial program start menu for logging in or creating a new user.
    """

    logging.basicConfig(level=logging.DEBUG)

    # Load configuration and set locale
    config_obj = config.Config()
    try:
        locale.setlocale(locale.LC_ALL, config_obj.LOCALE)
    except locale.Error:
        # Fallback to a default locale if the configured one is not available
        locale.setlocale(locale.LC_ALL, 'C')

    while True:
        # Display the start menu and get the user's action
        action = menus.program_start()

        match action:
            case menus.ProgramStartAction.LOGIN:
                # Prompt the user for login credentials
                res = menus.login_prompt()
                if res:
                    # If login is successful, show the home page
                    home_page(res)
                else:
                    # Show an error for incorrect login details
                    click.secho("Incorrect login details, please try again.", fg="red")
            case menus.ProgramStartAction.CREATE_USER:
                # Prompt the user to create a new account
                res = menus.create_user_prompt()
                # Go to the home page after creating the user
                home_page(res)
            case menus.ProgramStartAction.QUIT:
                quit()

if __name__ == "__main__":
    main()