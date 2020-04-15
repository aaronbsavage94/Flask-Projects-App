import requests
import json
from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/stockcheck")
def picker():
    return render_template('stockcheck.html', title="Stock Price Checker")

@app.route("/covid")
def covid():
    return render_template('covid_tracking.html', title="COVID-19 Tracking")

@app.route('/trackCOVID', methods=['POST'])
def getCOVIDData():

    response = requests.get('https://finnhub.io/api/v1/covid19/us?token=bpkgs0vrh5rcgrlra5v0')
    data = response.json()

    return render_template('covid_tracking.html', title="COVID-19 Tracking", results=data)


@app.route('/requestStock', methods=['POST'])
def requestStock():

    picker = request.form["picker"]

    url = "https://finnhub-realtime-stock-price.p.rapidapi.com/quote"

    queryString = {"symbol":picker}

    headers = {
        'x-rapidapi-host': "finnhub-realtime-stock-price.p.rapidapi.com",
        'x-rapidapi-key': "513b4d165fmsh4c349204d03662dp1d7b72jsn7bad13d69a6f"
        }

    response = requests.request("GET", url, headers=headers, params=queryString)
    data = response.json()

    results = []
    ticker = "Ticker: " + picker
    current = "Current price: " + str(data['c'])
    high = "High of the day: " + str(data['h'])
    low = "Low of the day: " + str(data['l'])
    opening = "Opening price of the day: " + str(data['o'])
    previous = "Previous close price: " + str(data['pc'])
    timestamp = "Timestamp: " + str(data['t'])

    results.append(ticker)
    results.append(current)
    results.append(high)
    results.append(low)
    results.append(opening)
    results.append(previous)
    results.append(timestamp)

    return render_template('stockpicker.html', title="Stock Picker", results=results)

if __name__ == '__main__':
    app.run(debug=True)