import streamlit as st
import yfinance as yf
import datetime as dt
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="StockUP", layout="wide", page_icon=":chart_with_upwards_trend:")
st.title('Fundamental Information')
a = '''
<style>
[data-testid="StyledLinkIconContainer"]{
    text-align: center;
}
[id='fundamental-information']{
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

ticker = st.selectbox(
        'Enter or Choose NSE listed Stock Symbol',
        symbol,placeholder='Enter or Choose a NSE listed Stock Symbol',index=None,label_visibility='hidden')
if ticker is None :
    st.warning("Please select a stock to continue.")
else:
    stock = yf.Ticker(ticker)
    info = stock.info

    st.subheader(info['longName'])

    sector = info.get('sector')
    if sector:
        st.write(f"****Sector****: {sector}")
    else:
        st.write("****Sector****: Not available")
     
    industry = info.get('industry')
    if industry:
        st.write(f"****Industry****: {industry}")
    else:
        st.write("****Industry****: Not available")

    phone = info.get('phone')
    if phone:
        st.write(f"****Phone****: {phone}")
    else:
        st.write("****Phone****: Not available")

    address1 = info.get('address1') 
    city = info.get('city')
    zip_code = info.get('zip')
    country = info.get('country')
    if address1 and city and zip_code and country:
        address = f"{address1}, {city}, {zip_code}, {country}"
        st.write(f"****Address****: {address}")
    else:
        st.write("****Address****: Not available")
 
    website = info.get('website')
    if website:
        st.write(f"****Website****: {website}")
    else:
        st.write("****Website****: Not available")
    with st.expander('See detailed business summary'):
        summary = info.get('longBusinessSummary')
        if summary:
            st.write(info['longBusinessSummary'])
        else:
            st.write("Not available")

    min_value = dt.datetime.today() - dt.timedelta(10 * 365)
    max_value = dt.datetime.today()

    start_input = st.date_input(
                'Enter starting date',
                value=dt.datetime.today()- dt.timedelta(90),
                min_value=min_value, max_value=max_value, help='Enter the starting date from which you have to look the price'
            )

    end_input =  st.date_input(
                'Enter last date',
                value=dt.datetime.today(),
                min_value=min_value, max_value=max_value, help='Enter the last date till which you have to look the price'
    )

    hist_price = yf.download(ticker,start_input,end_input)
    hist_price = hist_price.reset_index()
    hist_price['Date'] = pd.to_datetime(hist_price['Date']).dt.date

    @st.cache_data
    def convert_data(df):
        return df.to_csv().encode('utf-8')
    historical_csv = convert_data(hist_price)
    
    st.download_button(
            label="Download historical data as CSV",
            data=historical_csv,
            file_name='historical_df.csv',
            mime='text/csv',
    )

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
        title = {
            'text': 'Stock Prices of ' + ticker,
            'x': 0.5,
            'xanchor': 'center',
            }, height = 600, template = 'gridon')
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
        title = {
                    'text': 'Stock Prices of ' + ticker,
                    'x': 0.5,
                    'xanchor': 'center',
                    }, height = 600, template = 'gridon')
        fig.update_yaxes(tickprefix='₹')
        st.plotly_chart(fig, use_container_width=True)

    tab1, tab2, tab3,tab4,tab5= st.tabs(["Quarterly Result  ", "Profit & Loss  ", "Balance sheet  ", "Cash Flow", "Splits & Dividends"])
    with tab1:
        st.subheader('Quarterly Result')
        st.write('A quarterly result is a summary or collection of unaudited financial statements, such as balance sheets, income statements, and cash flow statements, issued by companies every quarter (three months).')
        quarterly_results = stock.quarterly_financials
        quarterly_results.columns = quarterly_results.columns.date
        quarterly_results.dropna(axis=0, inplace=True)
        quarterly_results = quarterly_results.astype('int64')
        for i in quarterly_results.columns:
                quarterly_results[i] = quarterly_results.apply(lambda x: "{:,}".format(x[i]), axis=1)
        st.dataframe(quarterly_results.style.highlight_max(axis=1, color='lightgreen'),width=1000)


    with tab2:
        st.subheader('Profit & Loss')
        st.write("A profit and loss (P&L) statement is a annually financial report that provides a summary of a company's revenue, expenses and profit.")
        financials = stock.financials
        financials.columns = financials.columns.date
        financials.dropna(axis=0, inplace=True)
        financials = financials.astype('int64')
        for i in financials.columns:
            financials[i] = financials.apply(lambda x: "{:,}".format(x[i]), axis=1)
        st.dataframe(financials.style.highlight_max(axis=1,color='lightgreen'),width=1000)

    with tab3:
        st.subheader('Balance Sheet')
        st.write("A balance sheet is a financial statement that reports a company's assets, liabilities, and shareholder equity.")
        balance = stock.balance_sheet
        balance.columns = balance.columns.date
        balance.dropna(axis=0, inplace=True)
        balance = balance.astype('int64')
        for i in balance.columns:
            balance[i] = balance.apply(lambda x: "{:,}".format(x[i]), axis=1)
        st.dataframe(balance.style.highlight_max(axis=1,color='lightgreen'),width=1000)

    with tab4:
        st.subheader('Cash Flows')
        st.write("The term cash flow refers to the net amount of cash and cash equivalents being transferred in and out of a company.")
        cf = stock.cashflow
        cf.columns = cf.columns.date
        cf.dropna(axis=0, inplace=True)
        cf = cf.astype('int64')
        for i in cf.columns:
            cf[i] = cf.apply(lambda x: "{:,}".format(x[i]), axis=1)
        st.dataframe(cf.style.highlight_max(axis=1,color='lightgreen'),width=1000)

    with tab5:
        st.subheader('Splits & Dividends')
        st.write('')
        actions = stock.actions
        actions.index = actions.index.date
        st.dataframe(actions, width=1000)
        
