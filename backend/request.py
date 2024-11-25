from datetime import datetime

class TradeRecord:
    def __init__(self, trader: str, book: str, product: str, cpty: str, buy: bool, qty: int, price: float):
        """
        Initializes a trade record object to store relevant trade data.

        Args:
            trader: Name of the trader.
            book: Identifier for the group of trades.
            product: The shares being traded.
            cpty: Counterparty of the trade.
            buy: True if the trade is a buy, False if it's a sell.
            qty: Integer quantity [1, 100000] of shares.
            price: Float value within 0.5 of the previous market price.
        """
        self.trader = trader
        self.book = book
        self.product = product
        self.cpty = cpty
        self.buy = buy
        self.qty = qty
        self.price = price
        now = datetime.now()
        self.dateID = now.strftime("%Y-%m-%d")
        self.timeID = now.strftime("%H:%M:%S")

    def getLastMarketStockPrice(self, product: str) -> float:
       """
       API call to fetch last market stock price.
       """
       pass

    def canCounterpartyTrade(self, cpty: str, product: str) -> bool:
        """
        API call to verify if counterparty is allowed to trade specified product.
        """
        pass

    def validate(self):
        """
        Validates the trade record data before insertion into the database.
        """
        if not (1 <= self.qty <= 100000):
            raise ValueError(f"Quantity {self.qty} must be between 1 and 100000.")
        
        if self.price <= 0:
            raise ValueError(f"Price {self.price} must be greater than 0.")
        
        last_market_price = self.getLastMarketStockPrice(self.product)
        if abs(last_market_price - self.price) > 0.5:
            raise ValueError(f"Price {self.price} is more than 0.5 away from last market price of {last_market_price} for product {self.product}.")
        
        if not self.canCounterpartyTrade(self.cpty, self.product):
            raise ValueError(f"Counterparty {self.cpty} not allowed to trade product {self.product}.")

    def to_tuple(self):
        """
        Converts the trade record into a tuple for database insertion.
        """
        direction = "Buy" if self.buy else "Sell"
        return (self.dateID, self.timeID, self.trader, self.book, self.cpty, self.product, direction, self.qty, self.price)

    def __str__(self):
        """
        String representation of the trade record.
        """
        direction = "Buy" if self.buy else "Sell"
        return f"TradeRecord(trader={self.trader}, book={self.book}, product={self.product}, direction={direction}, qty={self.qty}, price={self.price})"
