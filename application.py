import requests
from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/stockpicker")
def picker():
    return render_template('stockpicker.html', title="Stock Picker")

@app.route('/requestStock', methods=['POST'])
def requestStock():

    picker = request.form["picker"]

    url = "https://finnhub-realtime-stock-price.p.rapidapi.com/quote"

    querystring = {"symbol":picker}

    headers = {
        'x-rapidapi-host': "finnhub-realtime-stock-price.p.rapidapi.com",
        'x-rapidapi-key': "513b4d165fmsh4c349204d03662dp1d7b72jsn7bad13d69a6f"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    results = []
    current = "Current price: " + str(data['c'])
    high = "High of the day: " + str(data['h'])
    low = "Low of the day: " + str(data['l'])
    opening = "Oppening price of the day: " + str(data['o'])
    previous = "Previous close price: " + str(data['pc'])
    timestamp = "Timestamp: " + str(data['t'])

    results.append(current)
    results.append(high)
    results.append(low)
    results.append(opening)
    results.append(previous)
    results.append(timestamp)

    return render_template('stockpicker.html', title="Stock Picker", results=results)

if __name__ == '__main__':
    app.run(debug=True)