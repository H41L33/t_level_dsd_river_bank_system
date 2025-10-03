# River Bank System

A simple command-line interface (CLI) banking application written in Python.

## Features

-   User registration and login
-   Deposit, withdraw, and transfer funds between current and savings accounts
-   View transaction history
-   Secure password hashing with bcrypt
-   Configuration via environment variables

---

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/H41L33/t_level_dsd_river_bank_system
    cd river_bank_system
    ```

2.  **Install Poetry:**
    If you don't have Poetry installed, follow the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

3.  **Install dependencies:**
    Poetry will create a virtual environment automatically and install the dependencies listed in the `pyproject.toml` file.
    ```bash
    poetry install
    ```

4.  **Configure environment variables:**
    -   Copy the `.env.example` file to `.env`:
        ```bash
        cp .env.example .env
        ```
    -   Edit the `.env` file with your desired settings.

---

## Usage

Run the main application using Poetry's `run` command. This ensures the script executes within the correct virtual environment managed by Poetry.

```bash
poetry run python -m river_bank_system.main
```

# Tutorial

## 🌊 How it Works: Data Flow

The application is designed to be a loop, continuously prompting the user for input until they choose to exit. Here’s a breakdown of how data moves through the system with the new structure.

### 1. Initial Startup

* The program starts by running `main.py`.
* The `main()` function immediately calls `menus.program_start()`, which clears the screen and displays the first choice: **Login**, **Register**, or **Quit**.

### 2. User Creation

* If you choose to register, you'll be guided by the `create_user_prompt()` function in `menus.py`.
* This function collects your desired `username`, `display_name`, and `password`.
* Your password is then sent to `crypto.hash_bcrypt()` to be securely hashed.
* Finally, this information is passed to `users.UsersDB().create_new_user()`, which inserts a new record into the `tbl_accounts` table in your SQLite database.

### 3. User Login

* If you opt to log in, the `login_prompt()` function in `menus.py` will ask for your `username` and `password`.
* The `username` is used to fetch the stored password hash from the database via `users.UsersDB().get_password_hash()`.
* The plain-text password you entered and the stored hash are then passed to `auth.check_password()` to see if they match. `bcrypt` handles this comparison securely without ever exposing the original password.

### 4. Account Dashboard & Actions

* Once logged in, the `home_page()` function in `main.py` takes over.
* It uses `menus.account_dashboard()` to display your account balances and the available actions: **Deposit**, **Withdraw**, **Transfer**, **View Transactions**, and **Logout**. Your balance information is fetched from the database using functions within the `users.UsersDB` class.

* When you select a financial action (like Deposit), `main.py` creates an `actions.Actions(username)` object. This object manages the two-step process for every transaction:
    1.  **Update Balance**: The `Actions` class first calls a method from the `users.UsersDB` class (e.g., `add_current_balance`) to update your balance in the `tbl_accounts` table.
    2.  **Log Transaction**: Immediately after, it calls `transactions.TransactionsDB().log_transaction()` to create a permanent record of the event in the `tbl_transactions` table.

* If you choose to view your history, `main.py` calls `transactions.TransactionsDB().get_transactions()` to retrieve and display the recent records.

---

## 🛠️ Key Libraries

To enhance the functionality and security of this command-line application, a few key external libraries were chosen:

* **Click**: This library is used to create a more user-friendly and robust command-line interface (CLI). Instead of using Python's built-in `input()`, Click provides functions for styled output (like colors), clearing the screen, and creating clean, validated prompts. This improves the overall user experience when interacting with the bank system in the terminal.

* **Bcrypt**: Security is paramount when dealing with user credentials. The `bcrypt` library is a trusted and secure way to handle password hashing. When a user creates a password, it is not stored in plain text. Instead, it is run through a hashing algorithm to create a unique, fixed-length "hash." When the user logs in, the password they enter is hashed again and compared to the stored hash. This ensures that even if the database were compromised, the actual passwords would remain protected.
