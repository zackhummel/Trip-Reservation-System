import requests
from datetime import datetime as dt
from apiKey import getAPIKey

APIkey = getAPIKey()

def getRequestedSymbolData(stockSymbol, timeSeries, startDate, endDate):
    returnValue = {}
    
    try:
        trueTimeSeries = ""
        timeSlice = ""

        match timeSeries:
            case 1:
                trueTimeSeries = "TIME_SERIES_INTRADAY"
                timeSlice = "Intraday"
            case 2:
                trueTimeSeries = "TIME_SERIES_DAILY"
                timeSlice = 'Time Series (Daily)'
            case 3:
                trueTimeSeries = "TIME_SERIES_WEEKLY"
                timeSlice = 'Weekly Time Series'
            case 4:
                trueTimeSeries = "TIME_SERIES_MONTHLY"
                timeSlice = 'Monthly Time Series'
            case _:
                raise KeyError()


        convertedStart = dt.strptime(startDate, "%Y-%m-%d")

        convertedEnd = dt.strptime(endDate, "%Y-%m-%d")

        if convertedEnd < convertedStart:
            raise ValueError()
        
        
        if timeSeries == 1:  # Intraday
            url = (
                f"https://www.alphavantage.co/query"
                f"?function={trueTimeSeries}"
                f"&symbol={stockSymbol}"
                f"&interval=5min"
                f"&apikey={APIkey}"
            )
        else:  # Daily, Weekly, Monthly
            url = (
                f"https://www.alphavantage.co/query"
                f"?function={trueTimeSeries}"
                f"&symbol={stockSymbol}"
                f"&apikey={APIkey}"
            )

        r = requests.get(url)
        r.raise_for_status()  # Catch HTTP-level errors
        
        data = r.json()[timeSlice]

        dicKeys = []

        for i in data.keys():
            if dt.strptime(i, "%Y-%m-%d") >= convertedStart and dt.strptime(i, "%Y-%m-%d") <= convertedEnd:
                #print(i)
                dicKeys.append(i)

        # TODO: Use the keys in 'dicKeys's to get only between the dates selected
        # ie: data[dicKeys[0]] though in a loop to get all of them at once

        for i in dicKeys:
            returnValue[i] = data[i]
            #print(returnValue[i])
    
    except KeyError as e:
        print(f"Invalid key used.\n{e}")
        returnValue.clear()

    except ValueError as e:
        print(f"End date before start date.\n{e}")
        returnValue.clear()

    except Exception as e:
        print(f"An error occurred: {e}")
        returnValue.clear()
    
    return returnValue

# only runs if ran from this file
# for testing
if __name__ == "__main__":
    print(getRequestedSymbolData("GOOGL", 2, "2025-12-01", "2025-12-31"))