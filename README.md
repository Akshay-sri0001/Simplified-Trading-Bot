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
```

1. **Command-Specific Help (e.g., for market orders):**
   ```
   python main.py market -h
   ```

## Available Commands:

1. **Check Balance:**
   ```
   python main.py balance
   python main.py balance --asset BTC
   ```

2. **Set Leverage (for a specific symbol, e.g., BTCUSDT to 5x):**
   ```
   python main.py --symbol BTCUSDT leverage 5
   ```

3. **Place a Market Order:**
   ```
   # Buy 0.001 BTCUSDT at market price
   python main.py --symbol BTCUSDT market BUY 0.001
   # Sell 0.01 ETHUSDT at market price
   python main.py --symbol ETHUSDT market SELL 0.01
   ```

4. **Place a Stop-Limit Order:**
   - stop_price: The price at which the limit order is triggered.
   - price: The price of the limit order once triggered.
   ```
   # Buy 0.001 BTCUSDT: if market hits $20500 (stop_price), place a limit buy order at $20550 (price)
   python main.py --symbol BTCUSDT stoplimit BUY 0.001 20550 20500
   # Sell 0.01 ETHUSDT: if market hits $2900 (stop_price), place a limit sell order at $2895 (price)
   python main.py --symbol ETHUSDT stoplimit SELL 0.01 2895 2900
   ```

5. **Get Order Status:**
   (Replace 123456789 with an actual order ID)
   ```
   python main.py --symbol BTCUSDT status 123456789
   ```

6. **Get Open Orders (for a symbol):**
   ```
   python main.py --symbol BTCUSDT openorders
   ```

7. **Cancel an Order:**
   (Replace 123456789 with an actual open order ID)
   ```
   python main.py --symbol BTCUSDT cancel 123456789
   ```

## Logging

- All actions, API requests, API responses, and errors are logged.

- Console Output: Provides INFO level messages for major actions and errors.

- File Output: trading_bot.log in the project root contains detailed DEBUG level logs, including full API request/response payloads, which is useful for troubleshooting.

## Error Handling

- The bot includes error handling for:

- Invalid user inputs via the CLI.

- API errors returned by Binance (e.g., insufficient funds, invalid symbol, order validation errors).

- Connection issues.
  Errors are logged to both the console and the trading_bot.log file.
