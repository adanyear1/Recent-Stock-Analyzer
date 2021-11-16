"""using pandas web data reader to extract stock prices"""
"""We will be grabbing stock data from Yahoo Finance"""
import pandas as pd 
import numpy as np
import datetime #date library
from datetime import date
import pandas_datareader.data as web
from pandas import Series, DataFrame
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
from pandas_datareader._utils import RemoteDataError
from pandas_datareader.data import Options
from sys import exit

class Engine(object):

    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol
            
    def analyze(self):
        current_analysis = self.stock_symbol.opening_analysis()
        last_analysis = self.stock_symbol.next_analysis('finished')

        while current_analysis != last_analysis:
            if current_analysis != None:
                next_analysis_name = current_analysis.enter()
                current_analysis = self.stock_symbol.next_analysis(next_analysis_name)

            else:
                break

        #print out last scene
        current_analysis.enter()

class Datainput(object):

    #This function validates stock ticker symbol and creates graphs
    def enter(self):

        stockinput = (input("Enter Stock Ticker Symbol: "))
        stock = stockinput.upper()
        #dates
        today = date.today()
        start = datetime.datetime(2017, 1, 1)
        end = datetime.datetime(today.year, today.month, today.day)

        while True:
            try:
                """Using Dataframe Constructor"""
                df1 = web.DataReader(stock, 'yahoo', start, end)
                #write csv data
                csvurl1 = stock+'_shortterm.csv'
                outputdata1 = df1.to_csv(csvurl1)

                #Read csv to show end of the csv data
                inputdata1 = pd.read_csv(csvurl1)

                """ Data For Overview """
                fig = go.Figure([go.Scatter(x = inputdata1['Date'], y = inputdata1['Close'])])

                fig.update_layout(title=stock, plot_bgcolor='rgb(230,230,230)', showlegend=False)
                 
                fig.show()
                return 'finished'
                break
            except KeyError:
                print("invalid stock ticker symbol")
                return 'datainput'
                break
            except RemoteDataError:
                print("invalid stock ticker symbol")
                return 'datainput'
                break

class Continue(object):

    #This function asks user if they would like to continue analyzing stocks
    #If so user will be able to continue    
    def enter(self):
        print("Would You Like To Analyze More Stocks?")

        response = (input("> "))
        inputResponse = response.upper()

        if inputResponse == "YES":
            a_analysis.analyze()
        elif inputResponse == "NO":
            print("You May Exit the Stocks Analyzer Tool")
            exit(0)
        else:
            print("Enter Yes or No")
            self.enter()
            
          
class StockAnalyzer(object):

    analyzer = {
        'datainput': Datainput(),
        'finished': Continue(),
    }

    def __init__(self, start_analysis):
        self.start_analysis = start_analysis

    def next_analysis(self, analysis_name):
        val = StockAnalyzer.analyzer.get(analysis_name)
        return val

    def opening_analysis(self):
        return self.next_analysis(self.start_analysis)

a_stockanalyzer = StockAnalyzer('datainput')
a_analysis = Engine(a_stockanalyzer)
a_analysis.analyze()
