import os
import pandas as pd
import sys
import cufflinks as cf 
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()
from plotly.subplots import make_subplots
from Utils.logs import logger
from Utils.source_data import * 

def get_fill_color(label):
    if label >= 1:
        return 'rgba(0,250,0,0.4)'
    else:
        return 'rgba(250,0,0,0.4)'

def calculate_daily_returns(df:pd.DataFrame) -> pd.DataFrame:
    try:
        df['daily_return'] = ((df['Close'] + df['Dividends'])/ df['Close'].shift(1)) - 1
        return df
    except Exception as e:
        logger.info("Cannot get returns with error: {}".format(e))

def add_total_return(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df['total_return'] = (df['Close'] - df['Close'].shift[1]) + df['Dividends']
    except Exception as e:
        logger.info("Cannot get total returns with error: {}".format(e))

def add_cumulative_returns(df:pd.DataFrame) -> pd.DataFrame: 
    try:
        df['cumulative_return'] = (1 + df['daily_return']).cumprod()
        return df
    except Exception as e:
        logger.info("Cannot get cumulative returns with error: {}".format(e))

def add_bollinger_bands(df: pd.DataFrame, time_window = 20) -> pd.DataFrame:
    try:
        df['middle_band'] = df['Close'].rolling(window = time_window).mean()
        df['upper_band'] = df['middle_band'] + 1.96 * df['Close'].rolling(window = time_window).std()
        df['lower_band'] = df['middle_band'] - 1.96 * df['Close'].rolling(window = time_window).std()
    except:
        logger.error('Bollinger Bands cannot be calculated. Ensure that the close price column in set dataframe is populated.')
    return df

def plot_bollinger_bands(df: pd.DataFrame, ticker: str):
    fig = go.Figure()

    candle = go.Candlestick(x=df.index, open=df['Open'],
    high=df['High'], low=df['Low'],
    close=df['Close'], name="Candlestick")

    upper_line = go.Scatter(x=df.index, y=df['upper_band'], 
    line=dict(color='rgba(250, 0, 0, 0.75)', 
    width=1), name="Upper Band")

    mid_line = go.Scatter(x=df.index, y=df['middle_band'], 
    line=dict(color='rgba(0, 0, 250, 0.75)', 
    width=0.7), name="Middle Band")

    lower_line = go.Scatter(x=df.index, y=df['lower_band'], 
    line=dict(color='rgba(0, 250, 0, 0.75)', 
    width=1), name="Lower Band")

    fig.add_trace(candle)
    fig.add_trace(upper_line)
    fig.add_trace(mid_line)
    fig.add_trace(lower_line)

    fig.update_xaxes(title="Date", rangeslider_visible=True)
    fig.update_yaxes(title="Price")
        
    fig.update_layout(title=ticker + " Bollinger Bands",
    height=1200, width=1800, showlegend=True)
    fig.show()

def add_ichimoku(df: pd.DataFrame):

    """
    Adds Ichimoku data to dataframe

    Args:
        df ([type]): data in dataframe form

    Notes:
    The Ichimoke provides information on momentum and resistance. It is composed of five lines indicated below. 
    1) Conversion line: Represents support, resistance and reversals. 
    2) Baseline: Represents support, resistance and confirms trend changes
    3) Leading Span A: Used to identify future areas of support and resistance
    4) Leading Span B: Also used to identify support and resistances. 
    5) Lagging Span: Shows possible support and resistance. Used to confirm signals. 
    6) "Cloud" : Area between Span A and Span B. Represents the divergence in prices. 
    """

    #Conversion Line:
    high_val = df['High'].rolling(window = 9).max()
    low_val = df['Low'].rolling(window = 9).min()
    df['Conversion'] = (high_val + low_val)/2

    #Base Line:

    high_base = df['High'].rolling(window = 26).max()
    low_base = df['Low'].rolling(window = 26).min()
    df['Baseline'] = (high_base + low_base)/2

    #SpanA
    df['SpanA'] = ((df['Conversion'] + df['Baseline']) / 2)

    #SpanB
    high_spanB = df['High'].rolling(window = 52).max()
    low_spanB = df['Low'].rolling(window = 52).min()
    df['SpanA'] = ((high_spanB + low_spanB)/2).shift(26)

    #Laggin Span
    df['Lagging'] = df['Close'].shift(-26)

    return df

def plot_ichimoku(df: pd.DataFrame):
    candle = go.Candlestick(x=df.index, open=df['Open'],
    high=df['High'], low=df["Low"], close=df['Close'], name="Candlestick")

    df1 = df.copy()
    fig = go.Figure()
    df['label'] = np.where(df['SpanA'] > df['SpanB'], 1, 0)
    df['group'] = df['label'].ne(df['label'].shift()).cumsum()

    df = df.groupby('group')

    dfs = []
    for name, data in df:
        dfs.append(data)

    for df in dfs:
        fig.add_traces(go.Scatter(x=df.index, y=df.SpanA,
        line=dict(color='rgba(0,0,0,0)')))

        fig.add_traces(go.Scatter(x=df.index, y=df.SpanB,
        line=dict(color='rgba(0,0,0,0)'),
        fill='tonexty',
        fillcolor=get_fill_color(df['label'].iloc[0])))

    baseline = go.Scatter(x=df1.index, y=df1['Baseline'], 
    line=dict(color='pink', width=2), name="Baseline")

    conversion = go.Scatter(x=df1.index, y=df1['Conversion'], 
    line=dict(color='black', width=1), name="Conversion")

    lagging = go.Scatter(x=df1.index, y=df1['Lagging'], 
    line=dict(color='purple', width=2), name="Lagging")

    span_a = go.Scatter(x=df1.index, y=df1['SpanA'], 
    line=dict(color='green', width=2, dash='dot'), name="Span A")

    span_b = go.Scatter(x=df1.index, y=df1['SpanB'], 
    line=dict(color='red', width=1, dash='dot'), name="Span B")

    fig.add_trace(candle)
    fig.add_trace(baseline)
    fig.add_trace(conversion)
    fig.add_trace(lagging)
    fig.add_trace(span_a)
    fig.add_trace(span_b)
    
    fig.update_layout(height=1200, width=1800, showlegend=True)

    fig.show()