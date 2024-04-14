import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt
from functions import *
from millify import millify

st.set_page_config(page_title="StockUP", layout="wide", page_icon=":chart_with_upwards_trend:")
st.title('Screener')
a = '''
<style>
[data-testid="StyledLinkIconContainer"]{
    text-align: center;
}
[id='screener']{
    padding:0px;
    }
[data-testid="stAppViewBlockContainer"]{
    padding-top:60px;
}
</style>
'''
st.markdown(a, unsafe_allow_html=True)
csv = pd.read_csv('symbols.csv')
symbol = csv['Symbol'].tolist()
for i in range(0, len(symbol)):
    symbol[i] = symbol[i] + ".NS"

ticker_input = ticker = st.selectbox(
        'Enter or Choose NSE listed Stock Symbol',
        symbol,placeholder='Enter or Choose a NSE listed Stock Symbol',index=None,label_visibility='hidden')
if ticker is None :
        st.warning('Please select a stock to continue.')
else:
        start_input = dt.datetime.today() - dt.timedelta(120)
        end_input = dt.datetime.today()

        df = yf.download(ticker_input,start_input,end_input)
        df = df.reset_index()
        df['Date'] = pd.to_datetime(df['Date']).dt.date


        stock = yf.Ticker(ticker_input)
        info = stock.info
        closing_price = round((df['Close'].iloc[-1:]),2)
        opening_price = round(df['Open'].iloc[-1:],2).astype('str')
        
        sma_df = calc_moving_average(df,12)
        sma_df_tail = round(sma_df['sma'].iloc[-1:].astype('int64'),2)
        ema_df_tail = round(sma_df['ema'].iloc[-1:].astype('int64'),2)

        macd_df = calc_macd(df)
        ema26_df_tail = round(macd_df['ema26'].iloc[-1:].astype('int64'),2)
        macd_df_tail = round(macd_df['macd'].iloc[-1:].astype('int64'), 2)
        signal_df_tail = round(macd_df['signal'].iloc[-1:].astype('int64'), 2)

        rsi_df = RSI(df,14)
        rsi_df_tail = round(rsi_df['RSI'].iloc[-1:].astype('int64'), 2)

        adx_df = ADX(df,14)
        adx_df_tail = round(adx_df.iloc[-1:].astype('int64'), 2)

        breaking_out = is_breaking_out(df)
        consolidating = is_consolidating(df)

        st.divider()  
        with st.container():
                col1, col2, col3, col4 = st.columns(4)
                if 'fiftyTwoWeekLow'in info: 
                        col1.metric('52 Week Low', millify(info['fiftyTwoWeekLow'],2))
                else:
                        col1.metric('52 Week Low', 'N/A')
                if 'fiftyTwoWeekHigh' in info:
                        col2.metric('52 Week High', millify(info['fiftyTwoWeekHigh'],2))
                else:
                        col2.metric('52 Week High', 'N/A')                
        
                if 'regularMarketDayLow' in info:
                        col3.metric('Market Day Low', millify(info['regularMarketDayLow'],2))
                else:
                        col3.metric('Market Day Low', 'N/A')
                if 'regularMarketDayHigh' in info:                
                        col4.metric('Market Day High', millify(info['regularMarketDayHigh'],2))
                else:
                        col4.metric('Market Day High', 'N/A')
        st.divider()                  
        with st.container():
                co_1, co_2,co_3,co_4 = st.columns(4)
                if 'ebitdaMargins' in info:
                        co_1.metric('EBITDA Margin', round(info['ebitdaMargins'],3))
                else:
                        co_1.metric('EBITDA Margin', 'N/A')
                if 'profitMargins' in info:        
                        co_2.metric('Profit Margin', round(info['profitMargins'],3))
                else:
                        co_2.metric('Profit Margin', 'N/A')
                if 'grossMargins' in info:
                        co_3.metric('Gross Margin', round(info['grossMargins'],3))
                else:
                        co_3.metric('Gross Margin', 'N/A')
                if 'operatingMargins' in info:
                        co_4.metric('Operating Margin', round(info['operatingMargins'],3))
                else:
                        co_4.metric('Operating Margin', 'N/A')        
                
        st.divider()  
        with st.container():
                co_11, co_22,co_33,co_44 = st.columns(4)
                if 'currentRatio' in info:
                        co_11.metric('Current Ratio', info['currentRatio'])
                else:
                        co_11.metric('Current Ratio', 'N/A')        
                if 'returnOnAssets' in info:
                        co_22.metric('Return on Assets', info['returnOnAssets'])
                else:
                        co_22.metric('Return on Assets', 'N/A')
                if 'debtToEquity' in info:
                        co_33.metric('Debt to Equity', info['debtToEquity'])
                else:
                        co_33.metric('Debt to Equity', 'N/A')
                if 'returnOnEquity' in info:
                        co_44.metric('Return on Equity', info['returnOnEquity'])
                else:
                        co_44.metric('Return on Equity', 'N/A')
        st.divider()                  
        with st.container():
                c_1, c_2,c_3,c_4 = st.columns(4)
                if 'closing_price' in locals():
                        c_1.metric('Closing Price', millify(closing_price, precision=2))
                else:
                        c_1.metric('Closing Price', 'N/A')
                if 'sma_df_tail' in locals():
                        c_2.metric('Simple Moving Average', millify(sma_df_tail, precision=2))
                else:
                        c_2.metric('Simple Moving Average', 'N/A')
                if 'ema_df_tail' in locals():
                        c_3.metric('Exponential Moving Average', millify(ema_df_tail, precision=2))
                else:
                        c_3.metric('Exponential Moving Average', 'N/A')
                if 'ema26_df_tail' in locals():
                        c_4.metric('Exponential Moving Average over period 26', millify(ema26_df_tail,2))
                else:
                        c_4.metric('Exponential Moving Average over period 26', 'N/A')
        
        st.divider()  
        with st.container():
                c_11, c_22,c_33,c_44 = st.columns(4)
                if 'rsi_df_tail' in locals():
                        c_11.metric('Relative Strength Index', rsi_df_tail)
                else:
                        c_11.metric('Relative Strength Index', 'N/A')
                if 'adx_df_tail' in locals():
                        c_22.metric('Average Directional Index', adx_df_tail)
                else:
                        c_22.metric('Average Directional Index', 'N/A')
                if 'macd_df_tail' in locals():
                        c_33.metric('MACD', macd_df_tail)
                else:
                        c_33.metric('MACD', 'N/A')
                if 'signal_df_tail' in locals():
                        c_44.metric('Signal', signal_df_tail)
                else:
                        c_44.metric('Signal', 'N/A')
                         
        st.divider()   
        
        with st.container():
                cc_11, cc_22,cc_33,cc_44 = st.columns(4)
                if 'breaking_out' in locals():
                        cc_11.metric('Breaking Out', breaking_out)
                else:
                        cc_11.metric('Breaking Out', 'N/A')
                if 'consolidating' in locals():
                        cc_22.metric('Consolidating', consolidating)
                else:
                        cc_22.metric('Consolidating', 'N/A')
                if 'fiftyDayAverage' in info:
                        cc_33.metric('50 Day Average', millify(info['fiftyDayAverage'],2))
                else:
                        cc_33.metric('50 Day Average', 'N/A')
                if 'recommendationKey' in info:
                        cc_44.metric('Recommendation', info['recommendationKey'].upper())
                else:
                        cc_44.metric('Recommendation', 'N/A')
        st.divider()                
        
