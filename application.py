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

@app.route('/quote', methods=['POST'])
def getQuote():
    results = []

    try:
        url = "https://quotes15.p.rapidapi.com/quotes/random/"

        querystring = {"language_code":"en"}

        headers = {
            'x-rapidapi-host': "quotes15.p.rapidapi.com",
            'x-rapidapi-key': "513b4d165fmsh4c349204d03662dp1d7b72jsn7bad13d69a6f"
            }

        response = requests.request("GET", url, headers=headers, params=querystring, timeout=1)
        data = response.json()

        
        quote = str(data['content'] + "\n")
        originator = data['originator']
        author = "--" + str(originator['name'])
        
        results.append(quote)
        results.append(author)

        return render_template('home.html', results=results)

    except:
        results.append("Error encountered, please try again later.")
        return render_template('home.html', results=results)

@app.route('/trackCOVID', methods=['POST'])
def getCOVIDData():
    results = []
    
    try:
        response = requests.get('https://finnhub.io/api/v1/covid19/us?token=bpkgs0vrh5rcgrlra5v0')
        data = response.json()

        if "Invalid API" in data:
            results.append("Error encountered, please try again later.")
            return render_template('covid_tracking.html', title="COVID-19 Tracking", results=results)

        else:

            for d in data:
                results.append((json.dumps(d, ensure_ascii=False)).encode("utf8"))

            return render_template('covid_tracking.html', title="COVID-19 Tracking", results=results)

    
    except:
        results.append("Error encountered, please try again later.")
        return render_template('covid_tracking.html', title="COVID-19 Tracking", results=results)

@app.route('/requestStock', methods=['POST'])
def requestStock():

    picker = request.form["ticker"]
    results = []

    try:
        url = "https://finnhub-realtime-stock-price.p.rapidapi.com/quote"

        queryString = {"symbol":picker}

        headers = {
            'x-rapidapi-host': "finnhub-realtime-stock-price.p.rapidapi.com",
            'x-rapidapi-key': "513b4d165fmsh4c349204d03662dp1d7b72jsn7bad13d69a6f"
            }

        response = requests.request("GET", url, headers=headers, params=queryString)
        data = response.json()

        
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

        return render_template('stockcheck.html', title="Stock Price Checker", results=results)

    except:
        results.append("Error encountered, please try again later.")
        return render_template('stockcheck.html', title="Stock Price Checker", results=results)


if __name__ == '__main__':
    app.run(debug=True)