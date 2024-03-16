import streamlit as st
st.set_page_config(page_title="StockUP", layout="wide", page_icon=":chart_with_upwards_trend:")
a = '''
<style>
[id="about-us"]{
    padding:0px;
    }
[data-testid="stAppViewBlockContainer"]{
    padding-top:60px;
}
</style>
'''
st.markdown(a, unsafe_allow_html=True)
st.title('About Us')
st.markdown(" ### StockUP is the all in one financial website for the retail investors where retail investors can take a look at all Fundamental Information, Screeners, Pattern Recognition and Next-Day Forecasting of all the National Stock Exchange (NSE) listed stocks.")
st.divider()
st.markdown('#### Features of StockUP:')
st.markdown('##### -  One can gain information of all the stocks that are listed on National Stock Exchange (NSE) (To Be Exact - 1773 Companies). ')
st.markdown('##### -  Webapp have features like Fundamental Information, Screener, Pattern Recognition, Next-Day Forecasting (Machine Learning based).')
st.divider()
st.markdown('#### Details related to stock prices:')
st.markdown('#####  - All the historical prices for last 10 years are taken from Yahoo Finance.')
st.markdown('##### - Time period for stock prices is one day.')
st.divider()
st.markdown('#### Fundamental Information feature overview:')
st.markdown(' ##### -  It contains all the information related to company. ')
st.markdown(' ##### -  Historical prices of the company of last 10 years with candlestick and line chart.')
st.markdown(' ##### -  One can download historical prices too.')
st.markdown(' ##### - All quarterly and annually Financial Results, Balance Sheet, Cash Flow and Splits & Dividends')
st.divider()
st.markdown('####  Screener feature overview:')
st.markdown(' ##### -  It contains all the important parameters or metrics that are related to company.')
st.markdown(' ##### -  It also contains one more important feature, that is it give signals whether selected stock is breaking out or not. Traders do this manually by looking at candles.')
st.markdown(' ##### -  With breaking out it also gives signals for consolidating or not.')
st.divider()
st.markdown('#### Pattern Recognition feature overview:')
st.markdown(' ##### -  It is important feature of the webapp.')
st.markdown(' ##### -  Traders do this manually by looking at candles.')
st.markdown(' ##### - We automate this thing by scanning all the candlestick patterns for the selected stock, then it generates signals whether it is bullish or bearish')
st.divider()
st.markdown('#### Next-Day Forecasting feature overview:')
st.markdown(' ##### -  We have build the efficient Machine Learning model to predict the next day price.')
st.markdown(' ##### -  Our model trained on past 5 years of historical data and while predicting it looks for past 2 months to predict next-day price.')
st.divider()
st.markdown('#### News feature overview:')
