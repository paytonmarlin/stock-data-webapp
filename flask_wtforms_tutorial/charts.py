'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal
# import lxml


#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d')

def get_API(symbol, chart_type, time_series):
    time_seriesDict = { '1': 'TIME_SERIES_INTRADAY', '2': 'TIME_SERIES_DAILY', '3': 'TIME_SERIES_WEEKLY', '4': 'TIME_SERIES_MONTHLY'}
    time_seriesResponse = time_seriesDict[time_series]
    api_key = 'GR8VROXU8ASO7XHX'
    base_url = 'https://www.alphavantage.co/query?'
    params = { 'function': time_seriesResponse,
                'symbol': symbol,
                'interval': '60min',
                'outputsize': 'full',
                'apikey': api_key}
    response = requests.get(base_url, params=params)
    return response

def generate_chart(response, start_date, end_date, time_series, chart_type, symbol):
    json_time_seriesDict = { '1': 'Time Series (60min)', '2': 'Time Series (Daily)', '3': 'Weekly Time Series', '4': 'Monthly Time Series'}
    json_response = response.json()
    time_json_object = json_time_seriesDict[time_series]

    json_date_key = []
    json_open = []
    json_high = []
    json_low = []
    json_close = []
    #Intraday function
    if time_series == '1':
        for date_key in json_response[time_json_object]:
            real_date_key = datetime.strftime(end_date,"%Y-%m-%d")
        
        
            if real_date_key in date_key:

                json_date_key.append(date_key)
                
    
                json_open.append(float(json_response[time_json_object][date_key]["1. open"]))
                

                json_high.append(float(json_response[time_json_object][date_key]["2. high"]))
                
    
                json_low.append(float(json_response[time_json_object][date_key]["3. low"]))
                
                json_close.append(float(json_response[time_json_object][date_key]["4. close"]))
    else:
    
        for date_key in json_response[time_json_object]:
            if chart_type == 1:
                    real_date_key = datetime.strptime(date_key,"%Y-%m-%d %H:%M:%S")
            else:
                real_date_key = datetime.strptime(date_key,"%Y-%m-%d")
                
            if real_date_key >= start_date and real_date_key <= end_date:

                json_date_key.append(date_key)
                

                json_open.append(float(json_response[time_json_object][date_key]["1. open"]))
                

                json_high.append(float(json_response[time_json_object][date_key]["2. high"]))
                

                json_low.append(float(json_response[time_json_object][date_key]["3. low"]))
                
                json_close.append(float(json_response[time_json_object][date_key]["4. close"]))
    
    json_date_key.reverse()
    start_dateEdit = str(start_date)
    end_dateEdit = str(end_date)
    #Chart will then open in new browser
    if chart_type == '1':
            # Bar code
        bar_chart = pygal.Bar(x_label_rotation=20)
        bar_chart.title = 'Stock Data for ' + symbol + ': ' + start_dateEdit + ' to ' + end_dateEdit
        bar_chart.x_labels = map(str, json_date_key)
        bar_chart.add('Open', json_open)
        bar_chart.add('High', json_high)
        bar_chart.add('Low', json_low)
        bar_chart.add('Close', json_close)
        return bar_chart.render()
    
    ##
    elif chart_type == '2':
        line_chart = pygal.Line(x_label_rotation=20)
        line_chart.title = 'Stock Data for ' + symbol + ': ' + start_dateEdit + ' to ' + end_dateEdit
        line_chart.x_labels = map(str, json_date_key)
        line_chart.add('Open', json_open)
        line_chart.add('High', json_high)
        line_chart.add('Low', json_low)
        line_chart.add('Close', json_close)
        return line_chart.render()
    


