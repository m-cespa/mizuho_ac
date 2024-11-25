import psycopg
from datetime import datetime
from request import TradeRecord

class DatabaseUser:
    def __init__(self, dbname, host="192.168.1.100", port="5432"):
        self.dbname = dbname
        self.host = host
        self.port = port
        self.connection = None

    def create_user(self, admin_user, admin_password, new_user, new_password):
        """
        Creates a new PostgreSQL user and grants them privileges on a specified database.

        Args:
            admin_user (str): Admin username to connect to the database.
            admin_password (str): Admin password for authentication.
            new_user (str): New user to be created.
            new_password (str): Password for the new user.
        """
        try:
            # Connect to the PostgreSQL database as admin
            with psycopg.connect(
                dbname=self.dbname,
                user=admin_user,
                password=admin_password,
                host=self.host,
                port=self.port
            ) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    # Create new user and grant privileges
                    cursor.execute(f"CREATE USER {new_user} WITH PASSWORD %s;", (new_password,))
                    cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {self.dbname} TO {new_user};")
                    print(f"User '{new_user}' created and privileges granted.")
        except psycopg.Error as e:
            print(f"Error creating user: {e}")

    def login(self, username, password):
        """
        Logs in to database as specified user and maintains active connection.

        Args:
            username (str): Username for authentication.
            password (str): Password for the user.
        """
        try:
            self.connection = psycopg.connect(
                dbname=self.dbname,
                user=username,
                password=password,
                host=self.host,
                port=self.port
            )
            print(f"User '{username}' logged in successfully.")
        except psycopg.Error as e:
            print(f"Login failed: {e}")

    def logout(self):
        """
        Logs out by closing any active database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            print("User logged out successfully.")
        else:
            print("No active session to log out from.")

    def insert_trade(self, trader, book, product, cpty, buy, qty, price):
        """
        Inserts a trade into the database.

        Args:
            trader (str): Name of the trader.
            book (str): Book name.
            product (str): Product name.
            cpty (str): Counterparty name.
            buy (bool): Whether the trade is a buy (True) or sell (False).
            qty (int): Quantity of the product.
            price (float): Price of the product.
        """
        if not self.connection:
            print("Error: No active database connection. Please log in first.")
            return
        
        try:
            with self.connection.cursor() as cursor:
                insert_query = """
                INSERT INTO trades (trader, book, cpty, product, buy, qty, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, (trader, book, product, cpty, buy, qty, price))
                self.connection.commit()
                print("Trade inserted successfully.")
        except psycopg.Error as e:
            print(f"Error inserting trade: {e}")
