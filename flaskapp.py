import requests
import json
import traceback
import logging
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
    
#Render Mortgage Tool Kit Page
@app.route("/mortgage")
def mortgage():
    return render_template('mortgage.html', title="Mortgage Tool Kit")

#Render Weather Page
@app.route("/weather")
def weather():
    return render_template('weathercheck.html', title="Check the Weather")

#Render COVID-19 Page
@app.route("/covid")
def covid():

    #Endpoint and variables
    counter = 0
    counterArray = []
    response = requests.get('https://finnhub.io/api/v1/covid19/us?token=bpkgs0vrh5rcgrlra5v0')
    data = response.json()

    #For each object in response, parse death value to counterArray     
    for d in data:
        counterArray.append(int(d['death']))
    
    #For each int in counterArray, recursively add up
    for i in counterArray:
        counter += i

    return render_template('covid_tracking.html', title="COVID-19 Tracking", counter=str(counter))

#Render Market News Page
@app.route("/market")
def marketnews():
    return render_template('marketnews.html', title="Market News")

#HTTP POST for Top Market Headlines data
@app.route('/marketCheck', methods=['POST'])
def marketCheck():
    results = []
    headlineArray = []
    
    #Try POST
    try:

        #Endpoint
        response = requests.get('https://finnhub.io/api/v1/news?category=general&token=bpkgs0vrh5rcgrlra5v0')
        data = response.json()

        #If invalid API response, return error to form
        if "Invalid API" in data:
            results.append("Error encountered, please try again later. It appears the API key may be invalid.")
            return render_template('marketnews.html', title="Market Headlines", results=results)

        else:
            
            #For each in data response        
            for d in data:

                #Change encoding and strip ASCII characters to work around unicode hell
                headline = (json.dumps(d['headline'], ensure_ascii=False)).encode("utf8")
                headline = headline.decode('ascii', 'ignore')
                summary = (json.dumps(d['summary'], ensure_ascii=False)).encode("utf8")
                summary = summary.decode('ascii', 'ignore')

                #Grab the URL values     
                url = str(d['url'])            

                #If just quotes
                if headline != '""':
                    if summary != '""':

                        #Trim quotes and backslashes
                        headline = headline.replace("\\""","")
                        headline = headline[1:-1]
                        summary = summary.replace("\\""","")
                        summary = summary[1:-1]

                        #Append results and formatting HTML for bullets and the headline links
                        results.append("<a href=" + url + " target=_blank class='text-info'>" + headline + "</a><br>")
                        results.append("<ul><li>" + summary + "</li></ul><br>")

            #Append closing unordered list HTML
            results.append("</ul>")

            #Direct output to form
            return render_template('marketnews.html', title="Market News", results=results)

    #Catch error, return error message
    except Exception as e:
        results.append("Error encountered. Please double check your ticker or try again later.<br>Exception details: " + str(e))
        return render_template('marketnews.html', title="Market News", results=results)

#HTTP POST for COVID-19 data
@app.route('/trackCOVID', methods=['POST'])
def getCOVIDData():

    #Variables
    temparray = []
    results = []
    counterArray = []
    counter = 0
    
    #Try POST
    try:

        #Endpoint
        response = requests.get('https://finnhub.io/api/v1/covid19/us?token=bpkgs0vrh5rcgrlra5v0')
        data = response.json()

        #If invalid API response, return error to form
        if "Invalid API" in data:
            results.append("Error encountered, please try again later. It appears the API key may be invalid.")
            return render_template('covid_tracking.html', title="COVID-19 Tracking", results=results)

        #Else, change encoding of each object in JSON response for Linux host and redirect to form
        else:
            
            

            #For each object in response, parse death value to counterArray     
            for d in data:
                counterArray.append(int(d['death']))
            
            #For each int in counterArray, recursively add up
            for i in counterArray:
                counter += i

            #Append HTML for textarea and unordered list
            results.append('<textarea class="form-control" id="result" rows="15" readonly>')

            #For each object in the reply        
            for d in data:
                
                #Initialize variables
                state = str(d['state'])
                case = str(d['case'])
                death = str(d['death'])
                updated = str(d['updated'])

                #Concatenate strings and append to temparray
                temparray.append("State/Population: " + state + ", " + "Cases: " + case + ", " + "Deaths: " + death + ", " + "Updated: " + updated)

            #Sort array by alphabetical (state)
            sortedarray = sorted(temparray)

            #For each indice in the sortedarray, append it to results
            for i in sortedarray:
                results.append(i)

            #Append HTML for textarea and new line break
            results.append('</textarea><br>')
            
            #Direct output to form
            return render_template('covid_tracking.html', title="COVID-19 Tracking", results=results, counter=str(counter))

    #Catch error, return error message
    except Exception as e:
        results.append("Error encountered. Please double check your ticker or try again later.<br>Exception details: " + str(e))
        return render_template('covid_tracking.html', title="COVID-19 Tracking", results=results, counter=str(counter))

#HTTP POST for mortgage rate check
@app.route('/checkRates', methods=['POST'])
def checkRates():

    #Initialize variables
    zip = request.form["zip"]
    results = ""

    #Try POST
    try:

        #Endpoint
        url = "https://realtor.p.rapidapi.com/finance/rates"

        #Query and headers
        querystring = {"loc":zip}

        headers = {
            'x-rapidapi-host': "realtor.p.rapidapi.com",
            'x-rapidapi-key': "513b4d165fmsh4c349204d03662dp1d7b72jsn7bad13d69a6f"
            }

        #Send request and get response
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        
        #Weather objects
        rates_key = data['rates']

        #Parse responses
        zip_return = "Your Zip Code: " + zip + '<br/>'
        property_tax = "Property Tax: " + str(rates_key['property_tax']) + '<br/>'
        insurance_rate = "Insurance Rate: " + str(rates_key['insurance_rate']) + '<br/>'
        average_30_year = "Average Rate for 30 Year Fixed: " + str(rates_key['average_rate_30_year']) + '<br/>'
        average_rate_30_year_fha = "Average Rate for 30 Year FHA: " + str(rates_key['average_rate_30_year_fha']) + '<br/>'
        average_rate_30_year_va = "Average Rate for 30 Year VA: " + str(rates_key['average_rate_30_year_va']) + '<br/>'
        average_rate_20_year = "Average Rate for 20 Year Fixed: " + str(rates_key['average_rate_20_year']) + '<br/>'
        average_rate_15_year = "Average Rate for 15 Year Fixed: " + str(rates_key['average_rate_15_year']) + '<br/>'
        average_rate_51_arm = "Average Rate for 5/1 ARM: " + str(rates_key['average_rate_51_arm']) + '<br/>'
        average_rate_71_arm = "Average Rate for 7/1 ARM: " + str(rates_key['average_rate_71_arm']) + '<br/>'

        #Append to results var
        results += zip_return
        results += property_tax 
        results += insurance_rate
        results += average_30_year
        results += average_rate_30_year_fha
        results += average_rate_30_year_va
        results += average_rate_20_year
        results += average_rate_15_year
        results += average_rate_51_arm
        results += average_rate_71_arm

        #Direct parsed response to form
        return render_template('mortgage.html', title="Mortgage Tool Kit", results=results)
    
    #Catch errors and return error message
    except Exception as e:
        results += "Error encountered. Please double check your ticker or try again later.<br>Exception details: " + str(e)
        return render_template('mortgage.html', title="Mortgage Tool Kit", results=results)

#HTTP POST for mortgage rate calculation
@app.route('/calculateMortgage', methods=['POST'])
def calculateMortgage():

    #Initialize variables
    hoi = request.form["hoi"]
    tax_rate = request.form["tax_rate"]
    downpayment = request.form["downpayment"]
    price = request.form["price"]
    term = request.form["term"]
    rate = request.form["rate"]
    results = ""

    #Try POST
    try:

        #Endpoint
        url = "https://realtor.p.rapidapi.com/mortgage/calculate"

        #Query and headers
        querystring = {"hoi":hoi,"tax_rate":tax_rate,"downpayment":downpayment,"price":price,"term":term,"rate":rate}

        headers = {
            'x-rapidapi-host': "realtor.p.rapidapi.com",
            'x-rapidapi-key': "513b4d165fmsh4c349204d03662dp1d7b72jsn7bad13d69a6f"
            }

        #Send request and get response
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        
        #Weather objects
        mortgage_key = data['mortgage']

        #Parse responses
        loan_amount = "Loan Amount: " + str(mortgage_key['loan_amount']) + '<br/>'
        rate = "Rate: " + str(mortgage_key['rate']) + '<br/>'
        term = "Term: " + str(mortgage_key['term']) + '<br/>'
        monthly_payment = "Monthly Payment: " + str(mortgage_key['monthly_payment']) + '<br/>'
        principal_and_interest = "Principal and Interest: " + str(mortgage_key['principal_and_interest']) + '<br/>'
        monthly_property_taxes = "Monthly Property Taxes: " + str(mortgage_key['monthly_property_taxes']) + '<br/>'
        monthly_home_insurance = "Monthly Home Insurance: " + str(mortgage_key['monthly_home_insurance']) + '<br/>'

        #Append to results var
        results += loan_amount
        results += rate 
        results += term
        results += monthly_payment
        results += principal_and_interest
        results += monthly_property_taxes
        results += monthly_home_insurance

        #Direct parsed response to form
        return render_template('mortgage.html', title="Mortgage Tool Kit", results2=results)
    
    #Catch errors and return error message
    except Exception as e:
        results += "Error encountered. Please double check your ticker or try again later.<br>Exception details: " + str(e)
        return render_template('mortgage.html', title="Mortgage Tool Kit", results2=results)   
     
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
        except Exception as e:
            results += "Error encountered. Please double check your ticker or try again later.<br>Exception details: " + str(e)
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
        except Exception as e:
            results += "Error encountered. Please double check your ticker or try again later.<br>Exception details: " + str(e)
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
    except Exception as e:
        results.append("Error encountered. Please double check your ticker or try again later.<br>Exception details: " + str(e))
        return render_template('weathercheck.html', title="Check the Weather", results=results)

#Main method
if __name__ == '__main__':
    app.run(debug=True)