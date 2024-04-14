import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt
from functions import *
import plotly.graph_objects as go
from patterns import candlestick_patterns
import talib

st.set_page_config(page_title="StockUP", layout="wide", page_icon=":chart_with_upwards_trend:")
csv = pd.read_csv('symbols.csv')
symbol = csv['Symbol'].tolist()
for i in range(0, len(symbol)):
    symbol[i] = symbol[i] + ".NS"
a = '''
<style>
[data-testid="StyledLinkIconContainer"]{
    text-align: center;
}
[id='pattern-recognition']{
    padding:0px;
    }
[data-testid="stAppViewBlockContainer"]{
    padding-top:60px;
}
</style>
'''
st.markdown(a, unsafe_allow_html=True)
st.title('Pattern Recognition')
st.divider()
st.markdown(' :green[ Bullish - The stock is in up trendline]')
st.markdown(' :white[Neutral - Not such activity or no trendline present at current moment]')
st.markdown(' :red[Bearish - The stock is in down trendline]')
ticker_input = st.selectbox('Enter or Choose NSE listed stock', symbol,index=symbol.index('SUZLON.NS'))

show = st.radio(
        "Show/Hide Graph",
        ('Show', 'Hide'))
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
if (show == 'Show'):

        min_value = dt.datetime.today() - dt.timedelta(10 * 365)
        max_value = dt.datetime.today()

        start_input = st.date_input(
            'Enter starting date',
            value=dt.datetime.today() - dt.timedelta(90),
            min_value=min_value, max_value=max_value, help='Enter the starting date from which you have to look the price'
        )

        end_input = st.date_input(
            'Enter last date',
            value=dt.datetime.today(),
            min_value=min_value, max_value=max_value, help='Enter the last date till which you have to look the price'
        )

        hist_price = yf.download(ticker_input, start_input, end_input)
        hist_price = hist_price.reset_index()
        hist_price['Date'] = pd.to_datetime(hist_price['Date'])

        chart = st.radio(
            "Choose Style",
            ('Candlestick', 'Line Chart'))
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        if (chart == 'Line Chart'):
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=hist_price['Date'],
                    y=hist_price['Adj Close']
                )
            )

            fig.update_layout(
                title={
                    'text': 'Stock Prices of ' + ticker_input,
                    'x': 0.5,
                    'xanchor': 'center'
                    }, height=600, template='gridon')
            fig.update_yaxes(tickprefix='₹')
            st.plotly_chart(fig, use_container_width=True)

        if (chart == 'Candlestick'):
            fig = go.Figure()
            fig.add_trace(
                go.Candlestick(
                    x=hist_price['Date'],
                    open=hist_price['Open'],
                    high=hist_price['High'],
                    low=hist_price['Low'],
                    close=hist_price['Close']
                )
            )

            fig.update_layout(
                title={
                    'text': 'Stock Prices of ' + ticker_input,
                    'x': 0.5,
                    'xanchor': 'center'
                    }, height=600, template='gridon')
            fig.update_yaxes(tickprefix='₹')
            st.plotly_chart(fig, use_container_width=True)
else:
        st.write('Select show to check prices')
        
start_input = dt.datetime.today() - dt.timedelta(365)
end_input = dt.datetime.today()
df = yf.download(ticker_input, start_input, end_input)
df = df.reset_index()
df['Date'] = pd.to_datetime(df['Date']).dt.date

candle_names = candlestick_patterns.keys()

for candle,names in candlestick_patterns.items():
        df[candle] = getattr(talib, candle)(df['Open'], df['High'], df['Low'], df['Close'])
        

tmp_df = df.drop(['Date', 'Open','High', 'Low', 'Close', 'Adj Close', 'Volume'], axis=1,)

if not tmp_df.empty:
    tmp_df_1 = tmp_df.T
    tmp_last = tmp_df_1.iloc[: , -1].tolist()
    signal_df = pd.DataFrame()
    signal_df['Pattern Names'] = candlestick_patterns.values()
    signal_df['Signal'] = tmp_last
    signal_df['Signal'] = signal_df['Signal'].map({0: 'Neutral', -100:'Bearish', 100:'Bullish'})
    bullish_count = len(signal_df[signal_df['Signal'] == 'Bullish'])
    bearish_count = len(signal_df[signal_df['Signal'] == 'Bearish'])
    
    with st.container():
        st.write('#### Overview of pattern recognition')
        coll_11, coll_22, coll_33 = st.columns(3)
        coll_11.metric('Patterns with bullish signals', bullish_count)
        coll_22.metric('Pattersn with bearish signals', bearish_count)
        
 
    def color(val):
        color = 'green' if val == 'Bullish' else 'red' if val == 'Bearish' else None
        return f'background-color: {color}'
    
    st.write('#### All candlestick patterns signals ')
    st.table(signal_df.style.applymap(color, subset=['Signal']))
    sample = len(signal_df[signal_df['Signal'] == 'Bullish'])
else:
    st.write("No data available for the selected ticker.")





