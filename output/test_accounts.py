import unittest
from unittest.mock import patch
import datetime

# Import the module we're testing
from accounts import Account, get_share_price

class TestGetSharePrice(unittest.TestCase):
    """Tests for the get_share_price function"""
    
    def test_valid_symbols(self):
        """Test that get_share_price returns correct prices for valid symbols"""
        self.assertEqual(get_share_price("AAPL"), 150.0)
        self.assertEqual(get_share_price("TSLA"), 700.0)
        self.assertEqual(get_share_price("GOOGL"), 2800.0)
    
    def test_invalid_symbol(self):
        """Test that get_share_price raises ValueError for invalid symbols"""
        with self.assertRaises(ValueError):
            get_share_price("INVALID")

class TestAccount(unittest.TestCase):
    """Tests for the Account class"""
    
    def setUp(self):
        """Create a fresh account before each test"""
        self.account = Account("test_user")
    
    def test_initialization(self):
        """Test that a new account is initialized with correct values"""
        self.assertEqual(self.account._user_id, "test_user")
        self.assertEqual(self.account._balance, 0.0)
        self.assertEqual(self.account._initial_deposit, 0.0)
        self.assertEqual(self.account._holdings, {})
        self.assertEqual(self.account._transactions, [])
    
    def test_deposit_success(self):
        """Test successful deposit"""
        self.account.deposit(1000.0)
        self.assertEqual(self.account._balance, 1000.0)
        self.assertEqual(self.account._initial_deposit, 1000.0)
        self.assertEqual(len(self.account._transactions), 1)
        self.assertEqual(self.account._transactions[0]["type"], "deposit")
        self.assertEqual(self.account._transactions[0]["amount"], 1000.0)
        
        # Test multiple deposits
        self.account.deposit(500.0)
        self.assertEqual(self.account._balance, 1500.0)
        self.assertEqual(self.account._initial_deposit, 1500.0)
        self.assertEqual(len(self.account._transactions), 2)
    
    def test_deposit_invalid_amount(self):
        """Test deposit with invalid amount"""
        with self.assertRaises(ValueError):
            self.account.deposit(0)
        with self.assertRaises(ValueError):
            self.account.deposit(-100)
    
    def test_withdraw_success(self):
        """Test successful withdrawal"""
        self.account.deposit(1000.0)
        self.account.withdraw(500.0)
        self.assertEqual(self.account._balance, 500.0)
        self.assertEqual(len(self.account._transactions), 2)
        self.assertEqual(self.account._transactions[1]["type"], "withdraw")
        self.assertEqual(self.account._transactions[1]["amount"], 500.0)
    
    def test_withdraw_invalid_amount(self):
        """Test withdrawal with invalid amount"""
        self.account.deposit(1000.0)
        with self.assertRaises(ValueError):
            self.account.withdraw(0)
        with self.assertRaises(ValueError):
            self.account.withdraw(-100)
    
    def test_withdraw_insufficient_funds(self):
        """Test withdrawal with insufficient funds"""
        self.account.deposit(1000.0)
        with self.assertRaises(ValueError):
            self.account.withdraw(1001.0)
    
    @patch("accounts.get_share_price")
    def test_buy_shares_success(self, mock_get_share_price):
        """Test successful purchase of shares"""
        mock_get_share_price.return_value = 100.0
        
        self.account.deposit(1000.0)
        self.account.buy_shares("AAPL", 5)
        
        self.assertEqual(self.account._balance, 500.0)
        self.assertEqual(self.account._holdings, {"AAPL": 5})
        self.assertEqual(len(self.account._transactions), 2)
        self.assertEqual(self.account._transactions[1]["type"], "buy")
        self.assertEqual(self.account._transactions[1]["symbol"], "AAPL")
        self.assertEqual(self.account._transactions[1]["quantity"], 5)
        self.assertEqual(self.account._transactions[1]["amount"], 500.0)
    
    @patch("accounts.get_share_price")
    def test_buy_shares_insufficient_funds(self, mock_get_share_price):
        """Test buying shares with insufficient funds"""
        mock_get_share_price.return_value = 100.0
        
        self.account.deposit(100.0)
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 2)
    
    def test_buy_shares_invalid_quantity(self):
        """Test buying shares with invalid quantity"""
        self.account.deposit(1000.0)
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 0)
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", -5)
    
    @patch("accounts.get_share_price")
    def test_buy_shares_invalid_symbol(self, mock_get_share_price):
        """Test buying shares with invalid symbol"""
        mock_get_share_price.side_effect = ValueError("Unknown symbol: INVALID")
        
        self.account.deposit(1000.0)
        with self.assertRaises(ValueError):
            self.account.buy_shares("INVALID", 5)
    
    @patch("accounts.get_share_price")
    def test_sell_shares_success(self, mock_get_share_price):
        """Test successful sale of shares"""
        mock_get_share_price.return_value = 100.0
        
        self.account.deposit(1000.0)
        self.account.buy_shares("AAPL", 5)
        
        mock_get_share_price.return_value = 120.0
        self.account.sell_shares("AAPL", 3)
        
        self.assertEqual(self.account._balance, 860.0)  # 500 + 360
        self.assertEqual(self.account._holdings, {"AAPL": 2})
        self.assertEqual(len(self.account._transactions), 3)
        self.assertEqual(self.account._transactions[2]["type"], "sell")
        self.assertEqual(self.account._transactions[2]["symbol"], "AAPL")
        self.assertEqual(self.account._transactions[2]["quantity"], 3)
        self.assertEqual(self.account._transactions[2]["amount"], 360.0)
    
    @patch("accounts.get_share_price")
    def test_sell_all_shares(self, mock_get_share_price):
        """Test selling all shares of a symbol removes it from holdings"""
        mock_get_share_price.return_value = 100.0
        
        self.account.deposit(1000.0)
        self.account.buy_shares("AAPL", 5)
        self.account.sell_shares("AAPL", 5)
        
        self.assertEqual(self.account._holdings, {})
    
    def test_sell_shares_insufficient_shares(self):
        """Test selling shares with insufficient quantity"""
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 1)
        
        self.account.deposit(1000.0)
        with patch("accounts.get_share_price", return_value=100.0):
            self.account.buy_shares("AAPL", 5)
        
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 6)
    
    def test_sell_shares_invalid_quantity(self):
        """Test selling shares with invalid quantity"""
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 0)
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", -5)
    
    @patch("accounts.get_share_price")
    def test_portfolio_value(self, mock_get_share_price):
        """Test portfolio_value returns correct value"""
        # Setup holdings
        mock_get_share_price.return_value = 100.0
        self.account.deposit(2000.0)
        self.account.buy_shares("AAPL", 5)
        self.account.buy_shares("TSLA", 5)
        
        # Test different prices when calculating portfolio value
        def mock_prices(symbol):
            prices = {"AAPL": 120.0, "TSLA": 150.0}
            return prices[symbol]
            
        mock_get_share_price.side_effect = mock_prices
        
        expected_value = (5 * 120.0) + (5 * 150.0)  # 1350.0
        self.assertEqual(self.account.portfolio_value(), expected_value)
    
    @patch("accounts.get_share_price")
    def test_total_account_value(self, mock_get_share_price):
        """Test total_account_value returns correct value"""
        # Setup holdings
        mock_get_share_price.return_value = 100.0
        self.account.deposit(2000.0)
        self.account.buy_shares("AAPL", 10)  # Costs 1000.0
        
        # Test with new share price
        def mock_prices(symbol):
            prices = {"AAPL": 120.0}
            return prices[symbol]
            
        mock_get_share_price.side_effect = mock_prices
        
        # Balance is 1000.0, portfolio value is 1200.0
        expected_value = 1000.0 + 1200.0
        self.assertEqual(self.account.total_account_value(), expected_value)
    
    @patch("accounts.get_share_price")
    def test_profit_loss(self, mock_get_share_price):
        """Test profit_loss returns correct value"""
        # Initial deposit
        self.account.deposit(1000.0)
        
        # Buy shares
        mock_get_share_price.return_value = 100.0
        self.account.buy_shares("AAPL", 5)  # Costs 500.0
        
        # No gain/loss yet
        mock_get_share_price.return_value = 100.0
        self.assertEqual(self.account.profit_loss(), 0.0)
        
        # Share price increases
        mock_get_share_price.return_value = 120.0
        expected_profit = (5 * 120.0) - (5 * 100.0)  # 100.0
        self.assertEqual(self.account.profit_loss(), expected_profit)
        
        # Share price decreases
        mock_get_share_price.return_value = 80.0
        expected_loss = (5 * 80.0) - (5 * 100.0)  # -100.0
        self.assertEqual(self.account.profit_loss(), expected_loss)
    
    @patch("accounts.get_share_price")
    def test_get_holdings(self, mock_get_share_price):
        """Test get_holdings returns a copy of holdings"""
        mock_get_share_price.return_value = 100.0
        self.account.deposit(1000.0)
        self.account.buy_shares("AAPL", 5)
        
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {"AAPL": 5})
        
        # Verify it's a copy by modifying it
        holdings["AAPL"] = 10
        self.assertEqual(self.account._holdings, {"AAPL": 5})  # Original unchanged
    
    def test_get_transactions(self):
        """Test get_transactions returns a copy of transactions"""
        self.account.deposit(1000.0)
        
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 1)
        
        # Verify it's a copy by modifying it
        transactions.clear()
        self.assertEqual(len(self.account._transactions), 1)  # Original unchanged

if __name__ == "__main__":
    unittest.main()