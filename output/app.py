import gradio as gr
from accounts import Account, get_share_price

# Initialize a single account for demo purposes
user_account = Account("demo_user")

def create_account(user_id):
    global user_account
    user_account = Account(user_id)
    return f"Account created for user: {user_id}"

def deposit_funds(amount):
    try:
        amount = float(amount)
        user_account.deposit(amount)
        return f"Successfully deposited ${amount:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def withdraw_funds(amount):
    try:
        amount = float(amount)
        user_account.withdraw(amount)
        return f"Successfully withdrew ${amount:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def buy_shares(symbol, quantity):
    try:
        quantity = int(quantity)
        user_account.buy_shares(symbol, quantity)
        return f"Successfully bought {quantity} shares of {symbol}"
    except (ValueError, TypeError) as e:
        return f"Error: {str(e)}"

def sell_shares(symbol, quantity):
    try:
        quantity = int(quantity)
        user_account.sell_shares(symbol, quantity)
        return f"Successfully sold {quantity} shares of {symbol}"
    except (ValueError, TypeError) as e:
        return f"Error: {str(e)}"

def get_account_info():
    holdings = user_account.get_holdings()
    portfolio_value = user_account.portfolio_value()
    total_value = user_account.total_account_value()
    profit_loss = user_account.profit_loss()
    
    holdings_str = "Current Holdings:\n"
    if not holdings:
        holdings_str += "None\n"
    else:
        for symbol, quantity in holdings.items():
            price = get_share_price(symbol)
            value = price * quantity
            holdings_str += f"{symbol}: {quantity} shares @ ${price:.2f} = ${value:.2f}\n"
    
    return f"""
Account Balance: ${user_account._balance:.2f}
{holdings_str}
Portfolio Value: ${portfolio_value:.2f}
Total Account Value: ${total_value:.2f}
Profit/Loss: ${profit_loss:.2f}
"""

def get_transactions():
    transactions = user_account.get_transactions()
    if not transactions:
        return "No transactions yet."
    
    result = "Transaction History:\n"
    for idx, t in enumerate(transactions, 1):
        timestamp = t["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        if t["type"] == "deposit":
            result += f"{idx}. {timestamp} - DEPOSIT: ${t['amount']:.2f}\n"
        elif t["type"] == "withdraw":
            result += f"{idx}. {timestamp} - WITHDRAW: ${t['amount']:.2f}\n"
        elif t["type"] == "buy":
            result += f"{idx}. {timestamp} - BUY: {t['quantity']} shares of {t['symbol']} for ${t['amount']:.2f}\n"
        elif t["type"] == "sell":
            result += f"{idx}. {timestamp} - SELL: {t['quantity']} shares of {t['symbol']} for ${t['amount']:.2f}\n"
    
    return result

def get_stock_price(symbol):
    try:
        price = get_share_price(symbol)
        return f"Current price of {symbol}: ${price:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Trading Account Management System") as demo:
    gr.Markdown("# Trading Account Management System")
    
    with gr.Tab("Account Setup"):
        with gr.Row():
            with gr.Column():
                create_user_input = gr.Textbox(label="User ID")
                create_account_btn = gr.Button("Create Account")
                create_account_output = gr.Textbox(label="Result")
                
                create_account_btn.click(
                    create_account,
                    inputs=[create_user_input],
                    outputs=[create_account_output]
                )
    
    with gr.Tab("Deposit/Withdraw"):
        with gr.Row():
            with gr.Column():
                deposit_input = gr.Number(label="Amount to Deposit")
                deposit_btn = gr.Button("Deposit")
                deposit_output = gr.Textbox(label="Result")
                
                deposit_btn.click(
                    deposit_funds,
                    inputs=[deposit_input],
                    outputs=[deposit_output]
                )
            
            with gr.Column():
                withdraw_input = gr.Number(label="Amount to Withdraw")
                withdraw_btn = gr.Button("Withdraw")
                withdraw_output = gr.Textbox(label="Result")
                
                withdraw_btn.click(
                    withdraw_funds,
                    inputs=[withdraw_input],
                    outputs=[withdraw_output]
                )
    
    with gr.Tab("Trading"):
        with gr.Row():
            with gr.Column():
                stock_price_input = gr.Textbox(label="Stock Symbol (e.g., AAPL, TSLA, GOOGL)")
                stock_price_btn = gr.Button("Get Current Price")
                stock_price_output = gr.Textbox(label="Current Price")
                
                stock_price_btn.click(
                    get_stock_price,
                    inputs=[stock_price_input],
                    outputs=[stock_price_output]
                )
        
        with gr.Row():
            with gr.Column():
                buy_symbol = gr.Textbox(label="Stock Symbol to Buy")
                buy_quantity = gr.Number(label="Quantity", precision=0)
                buy_btn = gr.Button("Buy Shares")
                buy_output = gr.Textbox(label="Result")
                
                buy_btn.click(
                    buy_shares,
                    inputs=[buy_symbol, buy_quantity],
                    outputs=[buy_output]
                )
            
            with gr.Column():
                sell_symbol = gr.Textbox(label="Stock Symbol to Sell")
                sell_quantity = gr.Number(label="Quantity", precision=0)
                sell_btn = gr.Button("Sell Shares")
                sell_output = gr.Textbox(label="Result")
                
                sell_btn.click(
                    sell_shares,
                    inputs=[sell_symbol, sell_quantity],
                    outputs=[sell_output]
                )
    
    with gr.Tab("Account Info"):
        with gr.Row():
            account_info_btn = gr.Button("Get Account Info")
            account_info_output = gr.Textbox(label="Account Information", lines=10)
            
            account_info_btn.click(
                get_account_info,
                inputs=[],
                outputs=[account_info_output]
            )
    
    with gr.Tab("Transaction History"):
        with gr.Row():
            transactions_btn = gr.Button("Get Transaction History")
            transactions_output = gr.Textbox(label="Transactions", lines=15)
            
            transactions_btn.click(
                get_transactions,
                inputs=[],
                outputs=[transactions_output]
            )

if __name__ == "__main__":
    demo.launch()