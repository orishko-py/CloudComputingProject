from flask import Flask, request, jsonify, json, render_template, flash, redirect, session, abort, url_for
import requests
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_agg import FigureCanvasAgg
from CassandraHandler import *

app = Flask(__name__)
app.secret_key = 'dev_key'
#startDB()

TOKEN = "PM2ZL6lvhCEkRWVlz696EOJuXqH8"


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty")
            return redirect(url_for('signup'))
        else:
            username = username.strip()
            password = password.strip()

        userInfo = queryExistingUser(username)
        if not userInfo:
            flash("Username {} is not available.".format(username))
            return redirect(url_for('signup'))
        else:
            enc_password = generate_password_hash(password, 'sha256')
            userSignUp(username, enc_password)
            flash("User account has been created.")
            return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        userInfo = queryExistingUser(username)
        if userInfo and check_password_hash(userInfo.enc_password, password):
            return redirect(url_for("home", username=username))
        else:
            flash("Invalid username or password.")

    return render_template("login.html")

@app.route('/home/<username>/')
def home(username):
    return render_template('index.html', username = username)

@app.route('/getStockQuotes', methods = ['POST'])
def getStockQuotes():
    stockIndex = request.form['stock_index']
    startDate = request.form['start_date']
    endDate = request.form['end_date']

    response = requests.get('https://sandbox.tradier.com/v1/markets/history',
        params={'symbol': stockIndex, 'interval': 'daily', 'start': startDate, 'end': endDate},
        headers={'Authorization': 'Bearer ' +TOKEN, 'Accept': 'application/json'}
        )
    dates, prices = prepareStockQuotes(response)

    return render_template('stockQuotes.html', data = [dates, prices], stockIndex = stockIndex)

@app.route('/getStockQuotes/<stockIndex>/graph', methods = ['GET'])
def plotStockGraph(stockIndex):
    pass


def prepareStockQuotes(response):
    quote_list = response.json()['history']['day']
    # prepare data for unplugg api
    dates = []
    prices = []
    for quote in quote_list:
        for key in quote.keys():
            if key == 'date':
                dates.append(datetime.strptime(quote['date'], '%Y-%m-%d'))
            elif key == 'close':
                prices.append(quote['close'])
    return dates, prices



if __name__ =='__main__':
    app.run(host='0.0.0.0', port=80, debug=True)