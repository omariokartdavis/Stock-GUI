from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime

def GetStock(name):
    """takes ticker and pulls info from alphavantage"""
    
    stock_symbol = name
    file_name = stock_symbol + ' Intraday Data.xlsx'
    sheet_name = 'Sheet1'
    date_time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    output_size = 'compact'    #can be compact or full. compact is last 100 mins.
    time_interval = '1min'     #can be 1, 5, 15, 30, or 60min for intraday data
    alphavantage_key = 'DMQB0PL4AAPZEQSC'
    
    ts = TimeSeries(key=alphavantage_key, output_format='pandas') #output_format changes data from JSON to pandas. can also be a csv file
    data, meta_data = ts.get_intraday(symbol=stock_symbol,interval=time_interval, outputsize=output_size)

    #define the time to be used for the x-axis to the length of the data dictionary going from high end to 0.
    time_range = range(len(data), 0, -1)

    
    df = pd.DataFrame({'Price':data['close'],
                   'Time':time_range})

    writer = ExcelWriter(file_name)
    df.to_excel(writer,sheet_name,index=False)
    writer.save()

    x = df['Time']
    y = df['Price']

    if output_size == 'compact':
        my_xticks = range(len(data), -1, -5)
    else:
        my_xticks = range(len(data), -1, -300)

    #some bull to get the x axis to properly show time from xxx mins ago to now.
    
    plt.xticks(my_xticks)
    plt.gca().invert_xaxis()

    plt.plot(x,y)
    plt.title(stock_symbol + ''' Intraday Share Price
    ('''+ date_time+ ')')
    plt.xlabel('Time (In minutes from current time)')
    plt.ylabel('Share Price')
    plt.grid()
    plt.show()
