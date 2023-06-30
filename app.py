import os
import sys

from time import gmtime, strftime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute("SELECT symbol, sum(shares), price FROM history WHERE user_id = ? GROUP BY symbol", session["user_id"])
    val_stocks = 0
    for stock in stocks:
        current = lookup(stock["symbol"])
        stock["name"] = current["name"]
        stock["price"] = current["price"]
        val_stocks = val_stocks + (stock["price"] * stock["sum(shares)"])
    row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    cashavail = row[0]["cash"]
    return render_template("index.html", cash=cashavail, stocks=stocks, stocks_sub=val_stocks, total=(val_stocks + cashavail))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("buy.html")

    else:
        # User reached route via POST (as by submitting a form via POST)
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return apology("must provide symbol and shares", 400)

        # Ensure shares are numeric
        try:
            i = float(shares)
        except Exception:
            return apology("Shares must be numeric", 400)

        # Ensure shares are positive number
        if i < 0:
            return apology("shares must be + number", 400)

        # Ensure shares are not a fraction
        j = i % 1
        if j != 0:
            return apology("share must be a whole number", 400)

        # Query IEX for stock symbol
        stock = lookup(symbol.upper())
        current_time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        print(current_time)

        # Ensure stock's symbol is found at IEX
        if stock == None:
            return apology("could not find stock at IEX", 400)

        # TO DO - Execute trade by doing stuff with stock (eg. add shares to list of holdings, deduct price*shares from cash)

        # Calculate the cost of transaction
        cost = stock["price"] * float(shares)

        # Ensure the user has enough cash to make the trade
        row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if len(row) == 0:
            return apology("could not find user data", 400)
        cashavail = row[0]["cash"]
        # Testing: print(cashavail, file=sys.stderr)

        # If not enough cash, register in history as failed attempt and return 400
        if cost > cashavail:
            return apology("Not enough cash to make this trade", 400)

        # If enough cash, register in history as completed trade and register in holdings
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cashavail - cost, session["user_id"])
        db.execute("INSERT INTO history (user_id, tradetype, tiempo, symbol, shares, price) VALUES (?, ?, ?, ?, ?, ?)",\
                    session["user_id"], "buy", current_time, stock["symbol"], shares, stock["price"])

        # Redirect user to home page
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    trades = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])
    return render_template("history.html", trades=trades)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:
        symbol = request.form.get("symbol")

        # Ensure stock's symbol is valid
        if not symbol:
            return apology("must provide a stock symbol", 400)

        # Query IEX for stock symbol
        stock = lookup(symbol.upper())

        # Ensure stock's symbol is found at IEX
        if stock == None:
            return apology("could not find stock at IEX", 400)

        # Redirect user to quoted page
        return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure confirmation matches password
        elif not (request.form.get("password") == request.form.get("confirmation")):
            return apology("confirmation must match password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username not already being used
        if len(rows) != 0:
            return apology("username already taken", 400)

        # Update database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get(\
            "username"), generate_password_hash(request.form.get("password")))

        # Remember which user has logged in
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        symbol_list = db.execute("SELECT symbol FROM history WHERE user_id = ? GROUP BY symbol", session["user_id"])
        return render_template("sell.html", symbol_list=symbol_list)

    else:
        # User reached route via POST (as by submitting a form via POST)
        symbol = request.form.get("symbol")
        shares = -int(request.form.get("shares"))

        if not symbol or not shares:
            return apology("must provide symbol and shares", 400)

        # Ensure shares are numeric
        try:
            i = float(shares)
        except Exception:
            return apology("Shares must be numeric", 400)

        # Ensure shares are negative number
        if not i < 0:
            return apology("shares must be - number", 400)

        # Ensure shares are not a fraction
        j = i % 1
        if j != 0:
            return apology("Shares must be a whole number", 400)

        # Query IEX for stock symbol
        stock = lookup(symbol)
        current_time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        # Ensure stock's symbol is found at IEX
        if stock == None:
            return apology("Could not find stock at IEX", 400)

        # Ensure the user owns enough shares to make the trade
        row = db.execute("SELECT sum(shares) FROM history WHERE user_id = ? AND symbol = ? GROUP BY symbol",\
                          session["user_id"], symbol)
        if (len(row) == 0 or row[0]["sum(shares)"] < -float(shares)):
            return apology("Not enough shares for this sale", 400)

        # Prepare for trade by retrieving cash
        row_cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if len(row_cash) == 0:
            return apology("could not find user data", 400)
        cashavail = row_cash[0]["cash"]

        # Calculate the cost of transaction
        cost = stock["price"] * float(shares)

        # Execute trade by doing stuff with stock (eg. add shares to list of holdings, deduct price*shares from cash)
        # If all good, register in history as completed trade and register in holdings
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cashavail - cost, session["user_id"])
        db.execute("INSERT INTO history (user_id, tradetype, tiempo, symbol, shares, price) VALUES (?, ?, ?, ?, ?, ?)",\
                    session["user_id"], "sell", current_time, stock["symbol"], shares, stock["price"])

        # Redirect user to home page
        return redirect("/")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Add cash"""
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("account.html")

    else:
        # User reached route via POST (as by submitting a form via POST)
        new_cash = request.form.get("cash")

        # Ensure valid request for cash (eg. numeric, positive, whole number)
        if not new_cash:
            return apology("Must provide the amount of cash", 400)
        try:
            i = float(new_cash)
        except Exception:
            return apology("Cash must be numeric", 400)
        if i < 0:
            return apology("Cash must be + number", 400)
        j = i % 1
        if j != 0:
            return apology("Cash must be a whole number", 400)

        current_time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        # Query how much cash user already has
        row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if len(row) == 0:
            return apology("could not find user data", 400)
        cashavail = row[0]["cash"]

        # Register in users db
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cashavail + float(new_cash), session["user_id"])

        # Redirect user to home page
        return redirect("/")


if __name__ == "__main__":
    app.run()
