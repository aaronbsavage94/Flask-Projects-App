import requests
import json
from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/")

#Render Home Page
@app.route("/home")
def home():
    return render_template('home.html')

#Render Stock Page
@app.route("/stockcheck")
def picker():
    return render_template('stockcheck.html', title="Stock Price Checker")

#Render Weather Page
@app.route("/weather")
def weather():
    return render_template('weathercheck.html', title="Check the Weather")

#Render COVID-19 Page
@app.route("/covid")
def covid():
    return render_template('covid_tracking.html', title="COVID-19 Tracking")

#HTTP POST for COVID-19 data
@app.route('/trackCOVID', methods=['POST'])
def getCOVIDData():
    results = []
    
    #Try POST
    try:

        #Endpoint
        response = requests.get('https://finnhub.io/api/v1/covid19/us?token=bpkgs0vrh5rcgrlra5v0')
        data = response.json()

        #If invalid API response, return error to form
        if "Invalid API" in data:
            results.append("Error encountered, please try again later.")
            return render_template('covid_tracking.html', title="COVID-19 Tracking", results=results)

        #Else, change encoding of each object in JSON response for Linux host and redirect to form
        else:

            #Append HTML for textarea         
            results.append('<textarea class="form-control" id="result" rows="15" readonly>')

            #For each object in the reply        
            for d in data:

                #Change string encoding
                d = (json.dumps(d, ensure_ascii=False)).encode("utf8")

                #Trim first and last characters to remove JSON brackets
                d = d[1:-1]

                #Append to results
                results.append(d)

            #Append HTML for textarea
            results.append('</textarea><br>')
            
            #Direct output to form
            return render_template('covid_tracking.html', title="COVID-19 Tracking", results=results)

    #Catch error, return error message
    except:
        results.append("Error encountered, please try again later.")
        return render_template('covid_tracking.html', title="COVID-19 Tracking", results=results)

#HTTP POST for stock price check
@app.route('/requestStock', methods=['POST'])
def requestStock():

    #Initialize variables
    picker = request.form["ticker"]
    results = ""
    ticker_type = request.form["ticker_type"]
    
    #If ETF, don't query company name as that endpoint does not work for non-company tickers
    if ticker_type == "ETF":

        #Try POST
        try:

            #Form query from HTML form
            queryString = {"symbol":picker}

            #Endpoints
            url = "https://finnhub-realtime-stock-price.p.rapidapi.com/quote"

            #Request header for first request
            headers = {
                'x-rapidapi-host': "finnhub-realtime-stock-price.p.rapidapi.com",
                'x-rapidapi-key': "513b4d165fmsh4c349204d03662dp1d7b72jsn7bad13d69a6f"
                }

            #Responses
            response = requests.request("GET", url, headers=headers, params=queryString)
            data = response.json()

            #Parse responses
            ticker = "Ticker: " + picker + '<br/>'
            current = "Current price: " + str(data['c']) + '<br/>'
            high = "High of the day: " + str(data['h']) + '<br/>'
            low = "Low of the day: " + str(data['l']) + '<br/>'
            opening = "Opening price of the day: " + str(data['o']) + '<br/>'
            previous = "Previous close price: " + str(data['pc']) + '<br/>'
            timestamp = "Timestamp: " + str(data['t'])

            #Append to results var
            results += ticker 
            results += current
            results += high
            results += low
            results += opening
            results += previous
            results += timestamp

            #Direct parsed response to form
            return render_template('stockcheck.html', title="Stock Price Checker", results=results)
        
        #Catch errors and return error message
        except:
            results += "Error encountered. Please double check your ticker or try again later."
            return render_template('stockcheck.html', title="Stock Price Checker", results=results)
    
    #Else query both endpoints for company information
    else:

        #Try POST
        try:
            #Form query from HTML form
            queryString = {"symbol":picker}

            #Endpoints
            url = "https://finnhub-realtime-stock-price.p.rapidapi.com/quote"
            url1 = "https://finnhub.io/api/v1/stock/profile2?symbol="+picker+"&token=bpkgs0vrh5rcgrlra5v0"

            #Request header for first request
            headers = {
                'x-rapidapi-host': "finnhub-realtime-stock-price.p.rapidapi.com",
                'x-rapidapi-key': "513b4d165fmsh4c349204d03662dp1d7b72jsn7bad13d69a6f"
                }

            #Responses
            response = requests.request("GET", url, headers=headers, params=queryString)
            data = response.json()
            
            response1 =  requests.get(url1)
            data1 = response1.json()

            #Parse responses
            company_string = str(data1["name"]) + " - " + str(data1["exchange"]) + '<br/>'
            ticker = "Ticker: " + picker + '<br/>'
            currency = "Currency: " + str(data1["currency"]) + '<br/>'
            current = "Current price: " + str(data['c']) + '<br/>'
            high = "High of the day: " + str(data['h']) + '<br/>'
            low = "Low of the day: " + str(data['l']) + '<br/>'
            opening = "Opening price of the day: " + str(data['o']) + '<br/>'
            previous = "Previous close price: " + str(data['pc']) + '<br/>'
            timestamp = "Timestamp: " + str(data['t'])

            #Append to results var
            results += company_string
            results += ticker 
            results += currency
            results += current
            results += high
            results += low
            results += opening
            results += previous
            results += timestamp

            #Direct parsed response to form
            return render_template('stockcheck.html', title="Stock Price Checker", results=results)

        #Catch errors and return error message
        except:
            results += "Error encountered. Please double check your ticker or try again later."
            return render_template('stockcheck.html', title="Stock Price Checker", results=results)

#HTTP POST for weather check
@app.route('/checkWeather', methods=['POST'])
def checkWeather():

    #Initialize variables
    zip = request.form["zip"]
    results = []

    #Try POST
    try:

        #Endpoint
        url = "http://api.openweathermap.org/data/2.5/weather?"
        api_key = "aace2be7c2713d5e8a6d908d015a0f81"

        #Query using input from HTML form
        querystring = {'appid':api_key,
                    'zip':zip}
        
        #Send request and get response
        response = requests.request("GET", url, params=querystring, timeout=1)
        data = response.json()

        
        #Weather objects
        weather = data['weather']                                                                                                                                                                                        
        weather_index = weather[0]
        weather_desc = weather_index['description']    

        #City name
        name = data['name']

        #Temp objects
        main = data['main']
        temp_orig = float(main['temp'])
        feels_like_orig = float(main['feels_like'])

        #Kelvin to Fahrenheit
        temp = ((temp_orig - 273.15)*(9.0/5.0)) + 32
        feels_like = ((feels_like_orig - 273.15)*(9.0/5.0)) + 32

        #Append output to results var
        results.append("Weather for " + name + ", " + zip + ", is: " + str(weather_desc) + " with a temperature of: " + str(round(temp, 2)) + " F, but it feels like: " + str(round(feels_like, 2)) + " F.")

        #Direct response to form
        return render_template('weathercheck.html', title="Check the Weather", results=results)

    #Catch error and return error response
    except:
        results.append("Error encountered. Double check your zip code or try again later.")
        return render_template('weathercheck.html', title="Check the Weather", results=results)

#Main method
if __name__ == '__main__':
    app.run(debug=True)