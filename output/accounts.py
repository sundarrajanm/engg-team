from typing import Dict, List
import datetime

def get_share_price(symbol: str) -> float:
    """Returns the current price of a given stock symbol."""
    prices = {
        "AAPL": 150.0,
        "TSLA": 700.0,
        "GOOGL": 2800.0
    }
    if symbol not in prices:
        raise ValueError(f"Unknown symbol: {symbol}")
    return prices[symbol]

class Account:
    def __init__(self, user_id: str):
        """Initialize a new account for a user."""
        self._user_id = user_id
        self._balance = 0.0
        self._initial_deposit = 0.0
        self._holdings = {}
        self._transactions = []
    
    def deposit(self, amount: float) -> None:
        """Deposit funds into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        # If this is the first deposit, update the initial deposit amount
        if self._initial_deposit == 0:
            self._initial_deposit = amount
        else:
            self._initial_deposit += amount
            
        self._balance += amount
        
        # Record the transaction
        transaction = {
            "type": "deposit",
            "symbol": None,
            "quantity": None,
            "amount": amount,
            "timestamp": datetime.datetime.now(datetime.UTC if hasattr(datetime, 'UTC') else datetime.timezone.utc)
        }
        self._transactions.append(transaction)
    
    def withdraw(self, amount: float) -> None:
        """Withdraw funds from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self._balance:
            raise ValueError(f"Insufficient funds. Available balance: {self._balance}")
        
        self._balance -= amount
        
        # Record the transaction
        transaction = {
            "type": "withdraw",
            "symbol": None,
            "quantity": None,
            "amount": amount,
            "timestamp": datetime.datetime.now(datetime.UTC if hasattr(datetime, 'UTC') else datetime.timezone.utc)
        }
        self._transactions.append(transaction)
    
    def buy_shares(self, symbol: str, quantity: int) -> None:
        """Buy shares of a stock."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # Check if symbol is valid and get its price
        price = get_share_price(symbol)
        total_cost = price * quantity
        
        if total_cost > self._balance:
            raise ValueError(f"Insufficient funds to buy {quantity} shares of {symbol}. Required: {total_cost}, Available: {self._balance}")
        
        # Update balance
        self._balance -= total_cost
        
        # Update holdings
        if symbol in self._holdings:
            self._holdings[symbol] += quantity
        else:
            self._holdings[symbol] = quantity
        
        # Record the transaction
        transaction = {
            "type": "buy",
            "symbol": symbol,
            "quantity": quantity,
            "amount": total_cost,
            "timestamp": datetime.datetime.now(datetime.UTC if hasattr(datetime, 'UTC') else datetime.timezone.utc)
        }
        self._transactions.append(transaction)
    
    def sell_shares(self, symbol: str, quantity: int) -> None:
        """Sell shares of a stock."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # Check if user has enough shares to sell
        if symbol not in self._holdings or self._holdings[symbol] < quantity:
            owned = self._holdings.get(symbol, 0)
            raise ValueError(f"Insufficient shares to sell. Trying to sell {quantity} shares of {symbol}, but only have {owned}")
        
        # Get the current price
        price = get_share_price(symbol)
        total_value = price * quantity
        
        # Update balance
        self._balance += total_value
        
        # Update holdings
        self._holdings[symbol] -= quantity
        if self._holdings[symbol] == 0:
            del self._holdings[symbol]
        
        # Record the transaction
        transaction = {
            "type": "sell",
            "symbol": symbol,
            "quantity": quantity,
            "amount": total_value,
            "timestamp": datetime.datetime.now(datetime.UTC if hasattr(datetime, 'UTC') else datetime.timezone.utc)
        }
        self._transactions.append(transaction)
    
    def portfolio_value(self) -> float:
        """Calculate the total value of shares in the portfolio."""
        total_value = 0.0
        for symbol, quantity in self._holdings.items():
            price = get_share_price(symbol)
            total_value += price * quantity
        return total_value
    
    def total_account_value(self) -> float:
        """Calculate the total account value (cash + portfolio)."""
        return self._balance + self.portfolio_value()
    
    def profit_loss(self) -> float:
        """Calculate profit or loss compared to initial deposit."""
        return self.total_account_value() - self._initial_deposit
    
    def get_holdings(self) -> Dict[str, int]:
        """Get current holdings."""
        return self._holdings.copy()
    
    def get_transactions(self) -> List[Dict]:
        """Get transaction history."""
        return self._transactions.copy()