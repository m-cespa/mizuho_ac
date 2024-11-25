import psycopg
from request import TradeRecord

class DatabaseUser:
    def __init__(self, dbname, host="127.0.0.1", port="5432"):
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
            # connect to PostgreSQL server as admin/superuser to create new user
            with psycopg.connect(
                dbname=self.dbname,
                user=admin_user,
                password=admin_password,
                host=self.host,
                port=self.port
            ) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    # create new user and grant all database priviliges
                    # privileges can be edites from the PostgreSQL terminal by superuser
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

    def insert_trade(self, trade_record: TradeRecord):
        """
        Inserts a trade into the database after validating the data.

        Args:
            trade_record (TradeRecord): Trade data encapsulated in a TradeRecord object.
        """
        if not self.connection:
            print("Error: No active database connection. Please log in first.")
            return

        try:
            trade_record.validate()
            with self.connection.cursor() as cursor:
                insert_query = """
                INSERT INTO trades (date, time, trader, book, counterparty, product, direction, qty, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, trade_record.to_tuple())
                self.connection.commit()
                print("Trade inserted successfully.")
        except psycopg.Error as e:
            print(f"Error inserting trade: {e}")
        except ValueError as ve:
            print(f"Validation error: {ve}")
