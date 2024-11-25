from flask import Flask, request, jsonify, session
from flask_session import Session
from database_user import DatabaseUser
from request import TradeRecord
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key_here' # secret production key
Session(app)

# database variable is set by user in html UI
db = None

@app.route('/login', methods=['POST'])
def login():
    """
    Logs in a user by passing credentials to the DatabaseUser class.
    """
    # retrieve data from posted request
    data = request.get_json()
    dbname = data.get('dbname')
    username = data.get('username')
    password = data.get('password')

    print(f"Received data - dbname: {dbname}, username: {username}, password: {password}")

    if not dbname or not username or not password:
        return jsonify({"error": "Database name, username, and password are required."}), 400

    try:
        # initialize specified db
        global db
        db = DatabaseUser(dbname=dbname)

        # attempt to login to specified db with user data
        db.login(username, password)

        # store the username and dbname to track user changes
        session['username'] = username
        session['dbname'] = dbname
        return jsonify({"message": f"User '{username}' logged in successfully to '{dbname}'."}), 200
    except Exception as e:
        print(f"Error during login: {str(e)}")  # Add a print statement here for debugging
        return jsonify({"error": str(e)}), 400


@app.route('/logout', methods=['POST'])
def logout():
    """
    Logs out the current user by clearing the session.
    """
    session.pop('username', None)
    session.pop('dbname', None)
    if db:
        db.logout()  # Close the database connection
    return jsonify({"message": "Logout successful."}), 200


@app.route('/insert_trade', methods=['POST'])
def insert_trade():
    """
    Inserts a trade record into the database after validating user session and trade data.
    """
    # unauthorised user catch
    if 'username' not in session or 'dbname' not in session:
        return jsonify({"error": "User is not logged in."}), 401

    data = request.get_json()

    try:
        # creates TradeRecord object from request data
        trade_record = TradeRecord(
            trader=data['trader'],
            book=data['book'],
            product=data['product'],
            counterparty=data['counterparty'],
            buy=data['buy'],
            qty=data['qty'],
            price=data['price']
        )
        
        # initialise database connection for specified db
        db = DatabaseUser(dbname=session['dbname'])
        
        db.insert_trade(trade_record)
        
        return jsonify({"message": "Trade inserted successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
