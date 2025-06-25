# Simplified-Trading-Bot
A Python-based command-line trading bot for interacting with the Binance Futures Testnet. Place market, limit, and stop-limit orders, check balances, and manage orders. Designed for learning and testing trading strategies without real financial risk. Features comprehensive logging and error handling.

# Simplified Binance Futures Trading Bot (Python)

A command-line interface (CLI) application built in Python for interacting with the Binance Futures Testnet (USDT-M). This bot allows users to place market, limit, and stop-limit orders, check account balances, get order statuses, and cancel orders. It's designed for educational purposes and for testing trading strategies in a risk-free environment.

## Features

*   **Binance Futures Testnet:** All operations are performed on the testnet, using test funds.
*   **Order Types:**
    *   Market Orders
    *   Limit Orders
    *   Stop-Limit Orders (Bonus Feature)
*   **Order Sides:** Supports both BUY and SELL orders.
*   **Account Management:**
    *   Check USDT (or other asset) balance.
    *   Set leverage for a symbol.
*   **Order Management:**
    *   Get status of a specific order.
    *   List all open orders for a symbol.
    *   Cancel an open order.
*   **Command-Line Interface:** Easy-to-use CLI for all operations.
*   **Logging:** Detailed logging of API requests, responses, and errors to `trading_bot.log` and console.
*   **Error Handling:** Robust error handling for API exceptions and user input.
*   **Python `python-binance`:** Utilizes the official `python-binance` library for API interaction.

## Prerequisites

*   Python 3.7+
*   A Binance Futures Testnet account: [Register Here](https://testnet.binancefuture.com)
*   API Key and API Secret generated from your Binance Futures Testnet account.
    *   **Important:** Ensure "Enable Futures" trading permission is checked for the API key.

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url> # Replace <your-repository-url> with the actual URL
    cd simplified-binance-futures-bot # Or your chosen directory name
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    # venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    The `requirements.txt` file should contain:
    ```
    python-binance
    python-dotenv
    ```

## Configuration (API Keys)

The bot requires your Binance Futures Testnet API key and secret to function. These should be stored in a `.env` file in the project root directory.

1.  **Create a `.env` file** in the root of the project:
    ```
    touch .env
    ```

2.  **Add your API credentials to the `.env` file:**
    ```env
    # .env
    BINANCE_TESTNET_API_KEY="YOUR_FUTURES_TESTNET_API_KEY_HERE"
    BINANCE_TESTNET_API_SECRET="YOUR_FUTURES_TESTNET_API_SECRET_HERE"
    ```
    Replace placeholders with your actual Testnet API key and secret.

    **⚠️ Important: Never commit your `.env` file or API keys directly to version control (e.g., Git).** The provided `.gitignore` file (if you created one) should ideally exclude `.env`. If you haven't, ensure you create a `.gitignore` file and add `.env` to it before your first commit.

## Usage (Command-Line Interface)

The main interaction with the bot is through `main.py`.

**General Help:**
```bash
python main.py -h
