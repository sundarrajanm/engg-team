```markdown
# Module Design: accounts.py

This module implements a simple account management system for a trading simulation platform.

## Overview

- The module contains a single main class: `Account`.
- It exposes a test implementation of the external function `get_share_price(symbol)` with fixed prices for AAPL, TSLA, and GOOGL.
- `Account` allows creating a user account, depositing and withdrawing funds, recording share transactions (buy/sell), and querying portfolio status.
- It enforces constraints to prevent invalid transactions such as overdrawing funds or selling non-owned shares.
- All state is stored within an `Account` instance.
  
---

## Function: get_share_price(symbol: str) -> float

- Input:  
  - `symbol`: a string ticker symbol, e.g. "AAPL"
- Output:  
  - Returns the current price of the share as a float.
- Behavior:
  - Returns fixed prices:
    - AAPL: 150.0
    - TSLA: 700.0
    - GOOGL: 2800.0
  - Raises a ValueError if the symbol is unknown.

---

## Class: Account

Represents a single user account.

### Constructor:
```python
def __init__(self, user_id: str)
```
- Parameters:
  - `user_id`: a unique string identifier for the user.
- Behavior:
  - Initializes the account with zero balance and empty share holdings and transaction history.
  - Stores the initial deposit amount to calculate profit/loss.

### Methods:

1. ```python
   def deposit(self, amount: float) -> None
   ```
   - Deposits funds into the user's account.
   - Amount must be positive.
   - Updates the balance and initial deposit if this is the first deposit.

2. ```python
   def withdraw(self, amount: float) -> None
   ```
   - Withdraws funds from the account.
   - Checks that the withdrawal does not result in a negative balance.
   - Raises an exception if insufficient funds.

3. ```python
   def buy_shares(self, symbol: str, quantity: int) -> None
   ```
   - Records purchase of a given quantity of shares for a symbol.
   - Validates:
     - Quantity is positive.
     - Account has sufficient funds to buy (price * quantity).
   - Updates balance, holdings, and transaction log.

4. ```python
   def sell_shares(self, symbol: str, quantity: int) -> None
   ```
   - Records sale of a given quantity of shares.
   - Validates:
     - Quantity is positive.
     - Account holds enough shares to sell.
   - Updates balance, holdings, and transaction log.

5. ```python
   def portfolio_value(self) -> float
   ```
   - Computes total value of currently held shares based on current prices.
   - Sum of (quantity * current share price) across holdings.

6. ```python
   def total_account_value(self) -> float
   ```
   - Returns the total account value = cash balance + portfolio value.

7. ```python
   def profit_loss(self) -> float
   ```
   - Returns the profit or loss compared to the initial deposit.
   - Can be negative or positive.
   - Calculation: total_account_value - initial_deposit_amount.

8. ```python
   def get_holdings(self) -> Dict[str, int]
   ```
   - Returns a dictionary mapping symbol to quantity of shares currently held.
   - Example: `{"AAPL": 10, "TSLA": 5}`

9. ```python
   def get_transactions(self) -> List[Dict]
   ```
   - Returns a time-ordered list of transaction records.
   - Each transaction record is a dictionary with keys:
     - `"type"`: one of `"deposit"`, `"withdraw"`, `"buy"`, `"sell"`
     - `"symbol"`: stock symbol for buy/sell, None for deposit/withdraw
     - `"quantity"`: int for buy/sell, None for deposit/withdraw
     - `"amount"`: amount of money deposited/withdrawn or spent/received on shares
     - `"timestamp"`: timestamp of the transaction (can be datetime or ISO string)

---

## Data Structures (Instance Attributes)

- `_user_id: str` — Unique identifier.
- `_balance: float` — Current cash balance available.
- `_initial_deposit: float` — Sum of all deposits (used for profit/loss).
- `_holdings: Dict[str, int]` — Map of symbols to share quantities held.
- `_transactions: List[Dict]` — History of all transactions in chronological order.

---

## Error Handling

Methods that attempt invalid operations raise appropriate exceptions with descriptive messages:

- Withdrawals or purchases that exceed available cash.
- Sales of shares not currently owned in sufficient quantity.
- Invalid symbols passed to buying/selling.
- Negative or zero quantities or amounts where not allowed.

---

## Notes on Usage

- The module is self-contained and does not require external dependencies.
- The time-stamps for transactions can be generated internally via `datetime.datetime.utcnow()` on each transaction.
- This design assumes synchronous single-user usage per account object.
- Extending for concurrency or persistence is out of scope for this initial design.

---

# Summary

This design encapsulates the full lifecycle of a simulated trading account including funds management, share transactions, portfolio valuation, and transaction history tracking in a single class `Account` supported by a price lookup function `get_share_price`. All requirements outlined are met through careful method definitions and state management.
```