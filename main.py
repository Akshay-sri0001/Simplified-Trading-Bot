# main.py
import argparse
from basic_bot import BasicBot
import config # To load API keys
from logger_setup import log # Use our configured logger
import json # For pretty printing dicts

def print_order_details(order_response):
    if order_response:
        print("\n--- Order Details ---")
        # Pretty print the JSON response
        print(json.dumps(order_response, indent=2))
        print(f"Status: {order_response.get('status')}")
        print(f"Order ID: {order_response.get('orderId')}")
    else:
        print("Order placement failed or no response received.")

def main():
    parser = argparse.ArgumentParser(description="Simplified Binance Futures Trading Bot")
    parser.add_argument('--symbol', type=str, default="BTCUSDT", help="Trading symbol (e.g., BTCUSDT)")

    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')
    subparsers.required = True

    # Market order sub-parser
    parser_market = subparsers.add_parser('market', help='Place a market order')
    parser_market.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side (BUY or SELL)')
    parser_market.add_argument('quantity', type=float, help='Quantity to trade')

    # Limit order sub-parser
    parser_limit = subparsers.add_parser('limit', help='Place a limit order')
    parser_limit.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side (BUY or SELL)')
    parser_limit.add_argument('quantity', type=float, help='Quantity to trade')
    parser_limit.add_argument('price', type=float, help='Price for the limit order')

    # Stop-Limit order sub-parser (Bonus)
    parser_stop_limit = subparsers.add_parser('stoplimit', help='Place a stop-limit order')
    parser_stop_limit.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side (BUY or SELL)')
    parser_stop_limit.add_argument('quantity', type=float, help='Quantity to trade')
    parser_stop_limit.add_argument('price', type=float, help='Price for the limit part of the order')
    parser_stop_limit.add_argument('stop_price', type=float, help='Price at which the limit order is triggered')

    # Order status sub-parser
    parser_status = subparsers.add_parser('status', help='Get order status')
    parser_status.add_argument('order_id', type=int, help='Order ID to check')
    
    # Cancel order sub-parser
    parser_cancel = subparsers.add_parser('cancel', help='Cancel an order')
    parser_cancel.add_argument('order_id', type=int, help='Order ID to cancel')

    # Get open orders sub-parser
    parser_open_orders = subparsers.add_parser('openorders', help='Get all open orders for the symbol')
    
    # Get account balance sub-parser
    parser_balance = subparsers.add_parser('balance', help='Get USDT account balance')
    parser_balance.add_argument('--asset', type=str, default="USDT", help="Asset to check balance for (default: USDT)")

    # Set leverage sub-parser
    parser_leverage = subparsers.add_parser('leverage', help='Set leverage for the symbol')
    parser_leverage.add_argument('leverage', type=int, help='Leverage value (e.g., 5 for 5x)')


    args = parser.parse_args()

    log.info(f"Starting bot with command: {args.command}")

    try:
        bot = BasicBot(api_key=config.API_KEY, api_secret=config.API_SECRET)
    except Exception as e:
        log.critical(f"Failed to initialize bot. Exiting. Error: {e}")
        print(f"Critical Error: Failed to initialize bot. Check logs. Error: {e}")
        return

    # Default symbol from top-level arg, can be overridden by specific commands if they take symbol
    symbol = args.symbol.upper() 

    if args.command == 'market':
        log.info(f"CLI: Market order: Side={args.side}, Quantity={args.quantity}, Symbol={symbol}")
        order = bot.place_market_order(symbol, args.side.upper(), args.quantity)
        print_order_details(order)
    
    elif args.command == 'limit':
        log.info(f"CLI: Limit order: Side={args.side}, Quantity={args.quantity}, Price={args.price}, Symbol={symbol}")
        order = bot.place_limit_order(symbol, args.side.upper(), args.quantity, args.price)
        print_order_details(order)

    elif args.command == 'stoplimit':
        log.info(f"CLI: Stop-Limit order: Side={args.side}, Quantity={args.quantity}, Price={args.price}, StopPrice={args.stop_price}, Symbol={symbol}")
        order = bot.place_stop_limit_order(symbol, args.side.upper(), args.quantity, args.price, args.stop_price)
        print_order_details(order)

    elif args.command == 'status':
        log.info(f"CLI: Get order status: OrderID={args.order_id}, Symbol={symbol}")
        status = bot.get_order_status(symbol, args.order_id)
        if status:
            print("\n--- Order Status ---")
            print(json.dumps(status, indent=2))
        else:
            print(f"Could not retrieve status for order ID {args.order_id}.")

    elif args.command == 'cancel':
        log.info(f"CLI: Cancel order: OrderID={args.order_id}, Symbol={symbol}")
        response = bot.cancel_order(symbol, args.order_id)
        if response:
            print("\n--- Cancel Order Response ---")
            print(json.dumps(response, indent=2))
        else:
            print(f"Could not cancel order ID {args.order_id} or it was already filled/cancelled.")
            
    elif args.command == 'openorders':
        log.info(f"CLI: Get open orders for Symbol={symbol}")
        orders = bot.get_open_orders(symbol)
        if orders is not None: # Could be an empty list which is a valid response
            print(f"\n--- Open Orders for {symbol} ---")
            if orders:
                for o in orders:
                    print(json.dumps(o, indent=2))
            else:
                print("No open orders found.")
        else:
            print("Failed to retrieve open orders.")

    elif args.command == 'balance':
        log.info(f"CLI: Get account balance for Asset={args.asset.upper()}")
        balance_info = bot.get_account_balance(asset=args.asset.upper())
        if balance_info:
            print(f"\n--- Account Balance for {args.asset.upper()} ---")
            print(f"Asset: {balance_info['asset']}")
            print(f"Balance: {balance_info['balance']}")
            print(f"Available Balance: {balance_info['availableBalance']}")
        else:
            print(f"Could not retrieve balance for asset {args.asset.upper()}.")

    elif args.command == 'leverage':
        log.info(f"CLI: Set leverage for Symbol={symbol} to Leverage={args.leverage}")
        response = bot.set_leverage(symbol, args.leverage)
        if response:
            print(f"\n--- Set Leverage Response for {symbol} ---")
            print(json.dumps(response, indent=2))
        else:
            print(f"Failed to set leverage for {symbol}.")


if __name__ == "__main__":
    main()