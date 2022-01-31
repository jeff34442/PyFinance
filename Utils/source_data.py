import csv
import yfinance as yf # This package allows us to connect to the yahoo finance api. 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#%matplotlib inline
import datetime as dt
from datetime import datetime, timedelta
import time 

import os
from os.path import dirname, join
from Utils.logs import logger
from dotenv import load_dotenv

load_dotenv()
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def open_file(PATH : str) -> pd.DataFrame:
    try:
        with open(PATH, 'rb') as csvfile:
            data_df = pd.read_csv(csvfile)
            return data_df
    except Exception as e:
        logger.error('Cannot open file path: {}, with error: {}'.format(PATH, e))


def get_column_from_df(column_name:str, data_df:pd.DataFrame) -> list:
    """Outputs column as list

    Args:
        column_name (str): Column name that is being searched for. 
        data_df (pd.DataFrame): Dataframe with desired data

    Returns:
        list: list of column values for specific column given as input. 
    """
    if column_name in data_df.columns:
        return list(data_df[column_name])
    else:
        logger.error('Cannot get the column name: {} from dataframe.'.format(column_name))


def get_stock_overview(ticker:str, key = "base") -> pd.Series:
    """ Returns any stock data that the user wants given a specific key

    Args:
        ticker (str): Acronym for stock. 
        key (str, optional): [description]. Defaults to "close".
            * options:
                1) base [DEFAULT]
                    a) contains: Open, High, Low, Close, Volume, Dividends, Stock Splits
                2) financials
                3) major holders
                4) institutional holders
                5) Cash Flow
                6) Earnings
                7) quarterly balance sheet
                8) quarterly cash flow
                9) quarterly financials
                10) quarterly earnings
                11) recommendations 
                
    Returns:
        [type]: DataFrame
    """
    try:
        stock = yf.Ticker(ticker)
        if key == "base":
            #history = stock.history(period="max")['Close']
            history = stock.history(period = "max")
            return history
        if key == "financials":
            #Financials will return data such as Total Revenue, Gross Profit etc. 
            return stock.financials
        if key == "major holders":
            #Returns the percentage of the total shares that are held by institutions and insiders.
            return stock.major_holders
        if key == "institutional holders":
            return stock.institutional_holders
        if key == "balance sheet":
            return stock.balance_sheet
        if key == "cash flow":
            return stock.cashflow
        if key == "earnings":
            return stock.earnings
        if key == "quarterly balance sheet":
            return stock.quarterly_balance_sheet
        if key == "quarterly cash flow":
            return stock.quarterly_cashflow
        if key == "quarterly financials":
            return stock.quarterly_financials
        if key == "quarterly earnings":
            return stock.quarterly_earnings
        if key == "recommendations":
            return stock.recommendations
    except Exception as e:
        logger.error('Key is not available. Please ensure key is lowercase.')
        

def get_NY_tickers(PATH = "Utils\\Core Data\\Ticker_Sector\\NYSE.csv") -> list:
    """Returns a list of all New York Stock Exchange Tickers. 

    Args:
        ticker (str): [description]
        PATH (str, optional): [description]. Defaults to "Utils\\Core Data\\Ticker_Sector\\NYSE.csv".

    Returns:
        list: list of all tickers
    """
    ticker_df = open_file(PATH)
    ticker_list = get_column_from_df("Ticker", ticker_df)
    return ticker_list

def data_to_csv(ticker: str, PATH = "C:\\Users\\jeff1\\Documents\\Data Repo\\Utils\\Core Data\\NYSE"):
    try:
        logger.info("Getting data for : {}".format(ticker))
        stock_close = get_stock_overview(ticker)

        if stock_close.empty:
            logger.info("Could not download data for ticker: {}".format(ticker))

        file_name = "{}\\{}.csv".format(PATH, ticker)
        stock_close.to_csv(file_name, index = False)
    except Exception as e:
        logger.info("Could not download data for ticker: {} with error {}. Error located between lines 116 and 125".format(ticker, e))


