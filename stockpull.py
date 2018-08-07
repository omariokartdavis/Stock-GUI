from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.file_name = self.ticker + 'Intraday Data.xlsx'
        self.sheet_name = 'Sheet1'
        self.date_time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        self.output_size = 'compact'
        self.time_interval = '1min'
        self.key = 'DMQB0PL4AAPZEQSC' # alphavantage key
        
    def get_data(self):
        """Pulls the stock data from alphavantage"""
    
        ts = TimeSeries(key=self.key, output_format = 'pandas')
        self.data, self.meta_data = ts.get_intraday(self.ticker, interval = self.time_interval, outputsize = self.output_size)
        
        time_range = range(len(self.data), 0, -1)
        
        self.df = pd.DataFrame({'Price':self.data['4. close'],
                           'Time':time_range})
        
    def plot_data(self):
        """Plots the data using matplotlib"""    
                
        x = self.df['Time']
        y = self.df['Price']
        
        if self.output_size == 'compact':
            my_xticks = range(len(self.data), -1, -5)
        else:
            my_xticks = range(len(self.data), -1, -300)
        
        plt.xticks(my_xticks)
        plt.gca().invert_xaxis()
        
        plt.plot(x,y)
        plt.title(self.ticker + ''' Intraday Share Price
        (''' + self.date_time + ')')
        plt.xlabel('Time (In minutes from current time)')
        plt.ylabel('Share Price')
        plt.grid()
        plt.show()
        
    def write_data(self):
        """Writes the pandas dataframe of the data to an excel file"""
        
        writer = ExcelWriter(self.file_name)
        self.df.to_excel(writer, self.sheet_name, index = False)
        writer.save()
