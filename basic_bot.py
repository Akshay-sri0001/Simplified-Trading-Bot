# basic_bot.py
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from logger_setup import log # Use our configured logger

class BasicBot:
    def __init__(self, api_key, api_secret):
        """
        Initializes the BasicBot with API credentials.
        The python-binance Client will use the testnet.binancefuture.com
        endpoints for its futures_* methods if the API keys were generated
        on the Futures Testnet.
        """
        try:
            self.client = Client(api_key, api_secret)
            # The base URL for futures testnet is automatically handled by python-binance
            # if the API keys are generated from testnet.binancefuture.com.
            # We can verify by pinging the server or getting account info.
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi' # Explicitly set for clarity/safety
            
            # Test connectivity
            self.client.futures_ping()
            log.info("Successfully connected to Binance Futures Testnet.")
            
            # Optional: Set default leverage for a common symbol if needed
            # self.set_leverage("BTCUSDT", 5) 

        except BinanceAPIException as e:
            log.error(f"Binance API Exception during initialization: {e}")
            raise
        except Exception as e:
            log.error(f"Error initializing BasicBot: {e}")
            raise

    def _log_request(self, method_name, params):
        log.debug(f"API Request: {method_name} with params: {params}")

    def _log_response(self, method_name, response):
        log.debug(f"API Response from {method_name}: {response}")

    def _handle_api_error(self, e, operation_description):
        log.error(f"Binance API Exception during {operation_description}: {e}")
        log.error(f"Status Code: {e.status_code}, Message: {e.message}")
        if hasattr(e, 'response') and e.response:
             log.error(f"Full API Error Response: {e.response.text}")
        return None # Or re-raise specific custom exceptions

    def get_account_balance(self, asset="USDT"):
        """Fetches the balance for a specific asset in the futures account."""
        log.info(f"Fetching account balance for asset: {asset}")
        try:
            balances = self.client.futures_account_balance()
            self._log_response("futures_account_balance", balances)
            for balance in balances:
                if balance['asset'] == asset:
                    log.info(f"Balance for {asset}: {balance['balance']}")
                    return balance
            log.warning(f"Asset {asset} not found in futures account balance.")
            return None
        except BinanceAPIException as e:
            return self._handle_api_error(e, "fetching account balance")
        except Exception as e:
            log.error(f"Unexpected error fetching account balance: {e}")
            return None

    def set_leverage(self, symbol, leverage):
        """Sets leverage for a given symbol."""
        log.info(f"Attempting to set leverage for {symbol} to {leverage}x")
        params = {"symbol": symbol, "leverage": leverage}
        self._log_request("futures_change_leverage", params)
        try:
            response = self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
            self._log_response("futures_change_leverage", response)
            log.info(f"Successfully set leverage for {symbol} to {response.get('leverage', 'N/A')}x. Max Notional: {response.get('maxNotionalValue', 'N/A')}")
            return response
        except BinanceAPIException as e:
            return self._handle_api_error(e, f"setting leverage for {symbol}")
        except Exception as e:
            log.error(f"Unexpected error setting leverage for {symbol}: {e}")
            return None

    def place_market_order(self, symbol: str, side: str, quantity: float):
        """
        Places a market order.
        :param symbol: Trading symbol (e.g., "BTCUSDT")
        :param side: "BUY" or "SELL"
        :param quantity: Amount to trade
        :return: Order response or None on error
        """
        side_map = {"BUY": SIDE_BUY, "SELL": SIDE_SELL}
        if side.upper() not in side_map:
            log.error(f"Invalid order side: {side}. Must be 'BUY' or 'SELL'.")
            return None

        log.info(f"Placing MARKET order: {side} {quantity} {symbol}")
        params = {
            "symbol": symbol,
            "side": side_map[side.upper()],
            "type": ORDER_TYPE_MARKET,
            "quantity": str(quantity) # API expects string for quantity
        }
        self._log_request("futures_create_order (MARKET)", params)
        try:
            order = self.client.futures_create_order(**params)
            self._log_response("futures_create_order (MARKET)", order)
            log.info(f"Market order placed successfully: {order}")
            return order
        except (BinanceAPIException, BinanceOrderException) as e:
            return self._handle_api_error(e, f"placing market order for {symbol}")
        except Exception as e:
            log.error(f"Unexpected error placing market order for {symbol}: {e}")
            return None

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        """
        Places a limit order.
        :param symbol: Trading symbol (e.g., "BTCUSDT")
        :param side: "BUY" or "SELL"
        :param quantity: Amount to trade
        :param price: Price for the limit order
        :return: Order response or None on error
        """
        side_map = {"BUY": SIDE_BUY, "SELL": SIDE_SELL}
        if side.upper() not in side_map:
            log.error(f"Invalid order side: {side}. Must be 'BUY' or 'SELL'.")
            return None

        log.info(f"Placing LIMIT order: {side} {quantity} {symbol} @ {price}")
        params = {
            "symbol": symbol,
            "side": side_map[side.upper()],
            "type": ORDER_TYPE_LIMIT,
            "timeInForce": TIME_IN_FORCE_GTC, # Good Till Cancelled
            "quantity": str(quantity),
            "price": str(price) # API expects string for price
        }
        self._log_request("futures_create_order (LIMIT)", params)
        try:
            order = self.client.futures_create_order(**params)
            self._log_response("futures_create_order (LIMIT)", order)
            log.info(f"Limit order placed successfully: {order}")
            return order
        except (BinanceAPIException, BinanceOrderException) as e:
            return self._handle_api_error(e, f"placing limit order for {symbol}")
        except Exception as e:
            log.error(f"Unexpected error placing limit order for {symbol}: {e}")
            return None

    def get_order_status(self, symbol: str, order_id: int):
        """
        Retrieves the status of a specific order.
        :param symbol: Trading symbol
        :param order_id: The ID of the order
        :return: Order status details or None on error
        """
        log.info(f"Fetching status for order ID {order_id} on {symbol}")
        params = {"symbol": symbol, "orderId": order_id}
        self._log_request("futures_get_order", params)
        try:
            order_status = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            self._log_response("futures_get_order", order_status)
            log.info(f"Order Status for {order_id}: {order_status}")
            return order_status
        except BinanceAPIException as e:
            return self._handle_api_error(e, f"getting order status for {order_id}")
        except Exception as e:
            log.error(f"Unexpected error getting order status for {order_id}: {e}")
            return None

    def cancel_order(self, symbol: str, order_id: int):
        """
        Cancels an open order.
        :param symbol: Trading symbol
        :param order_id: The ID of the order to cancel
        :return: Cancellation response or None on error
        """
        log.info(f"Attempting to cancel order ID {order_id} on {symbol}")
        params = {"symbol": symbol, "orderId": order_id}
        self._log_request("futures_cancel_order", params)
        try:
            cancel_response = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            self._log_response("futures_cancel_order", cancel_response)
            log.info(f"Order {order_id} cancelled successfully: {cancel_response}")
            return cancel_response
        except BinanceAPIException as e:
            return self._handle_api_error(e, f"cancelling order {order_id}")
        except Exception as e:
            log.error(f"Unexpected error cancelling order {order_id}: {e}")
            return None

    def get_open_orders(self, symbol: str = None):
        """
        Retrieves all open orders for a specific symbol or all symbols.
        :param symbol: Trading symbol (optional)
        :return: List of open orders or None on error
        """
        log.info(f"Fetching open orders for symbol: {symbol if symbol else 'ALL'}")
        params = {"symbol": symbol} if symbol else {}
        self._log_request("futures_get_open_orders", params)
        try:
            open_orders = self.client.futures_get_open_orders(**params)
            self._log_response("futures_get_open_orders", open_orders)
            log.info(f"Found {len(open_orders)} open order(s).")
            return open_orders
        except BinanceAPIException as e:
            return self._handle_api_error(e, "getting open orders")
        except Exception as e:
            log.error(f"Unexpected error getting open orders: {e}")
            return None
            
    # --- Bonus: Stop-Limit Order ---
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, price: float, stop_price: float):
        """
        Places a Stop-Limit order.
        For a BUY order: it triggers when price >= stop_price, then a limit order at 'price' is placed.
        For a SELL order: it triggers when price <= stop_price, then a limit order at 'price' is placed.
        Usually, for BUY: stop_price > current_market_price, and price >= stop_price (or slightly higher).
        Usually, for SELL: stop_price < current_market_price, and price <= stop_price (or slightly lower).

        :param symbol: Trading symbol (e.g., "BTCUSDT")
        :param side: "BUY" or "SELL"
        :param quantity: Amount to trade
        :param price: Price for the limit order part
        :param stop_price: Price at which the limit order is triggered
        :return: Order response or None on error
        """
        side_map = {"BUY": SIDE_BUY, "SELL": SIDE_SELL}
        if side.upper() not in side_map:
            log.error(f"Invalid order side: {side}. Must be 'BUY' or 'SELL'.")
            return None

        log.info(f"Placing STOP-LIMIT order: {side} {quantity} {symbol} @ price {price}, stopPrice {stop_price}")
        params = {
            "symbol": symbol,
            "side": side_map[side.upper()],
            "type": FUTURE_ORDER_TYPE_STOP, # This is for Stop-Limit
            # "type": FUTURE_ORDER_TYPE_STOP_MARKET, # If you wanted a Stop-Market order
            "quantity": str(quantity),
            "price": str(price), # The limit price
            "stopPrice": str(stop_price), # The trigger price
            "timeInForce": TIME_IN_FORCE_GTC # Or other, GTC is common
        }
        self._log_request("futures_create_order (STOP-LIMIT)", params)
        try:
            order = self.client.futures_create_order(**params)
            self._log_response("futures_create_order (STOP-LIMIT)", order)
            log.info(f"Stop-Limit order placed successfully: {order}")
            return order
        except (BinanceAPIException, BinanceOrderException) as e:
            return self._handle_api_error(e, f"placing stop-limit order for {symbol}")
        except Exception as e:
            log.error(f"Unexpected error placing stop-limit order for {symbol}: {e}")
            return None