import time
import requests
from bs4 import BeautifulSoup
import streamlit as st
from bsedata.bse import BSE
from jugaad_data.nse import NSELive

st.set_page_config(page_title="StockUP", layout="wide", page_icon=":chart_with_upwards_trend:")

css = """
<style>
[data-testid="StyledLinkIconContainer"]{
    text-align: center;
}
[id='home-page']{
    padding:0px;
}
[data-testid="stAppViewBlockContainer"]{
    padding-top:60px;
}
footer{
    visibility: hidden;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

def get_nifty_price():
    n = NSELive()
    nifty_data = n.live_index("NIFTY 50")
    nifty = nifty_data['data'][0]
    price = nifty['lastPrice']
    return price
def get_nifty_delta():
    n = NSELive()
    nifty_data = n.live_index("NIFTY 50")
    nifty = nifty_data['data'][0]
    delta = nifty['pChange']
    return delta
    
def get_bank_nifty_price():
    n = NSELive()
    bank_data = n.live_index("NIFTY BANK")
    nifty = bank_data['data'][0]
    price = nifty['lastPrice']
    return price
def get_bank_delta():
    n = NSELive()
    BANK_data = n.live_index("NIFTY BANK")
    nifty = BANK_data['data'][0]
    delta = nifty['pChange']
    return delta

def get_nifty_it():
    n = NSELive()
    IT_data = n.live_index("NIFTY IT")
    nifty = IT_data['data'][0]
    price = nifty['lastPrice']
    return price
def get_IT_delta():
    n = NSELive()
    IT_data = n.live_index("NIFTY IT")
    nifty = IT_data['data'][0]
    delta = nifty['pChange']
    return delta

def get_sensex_price():
    url = "https://www.google.com/finance/quote/SENSEX:INDEXBOM?hl=en"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    class1 = 'YMlKec fxKbKc'
    sensex_price = round(float(soup.find(class_=class1).text.replace(",", "")), 2)
    return sensex_price
def get_sensex_delta():
    url = "https://www.google.com/finance/quote/SENSEX:INDEXBOM?hl=en"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    class1 = 'JwB6zf V7hZne'
    sensex_delta = soup.find(class_=class1)
    if sensex_delta:
        sensex_delta = sensex_delta.text
    else:
        sensex_delta = "N/A" 
    return sensex_delta

st.title("Home")

nifty_price = get_nifty_price()
nifty_delta = get_nifty_delta()
bank_nifty_price = get_bank_nifty_price()
bank_delta = get_bank_delta()
nifty_it_price = get_nifty_it()
it_delta = get_IT_delta()
sensex_price = get_sensex_price()
sensex_delta = get_sensex_delta()
price_placeholder = st.empty()

b = BSE()
tg = b.topGainers()
tl = b.topLosers()
tab1, tab2, tab3 = st.tabs(["Top Gainers", " ", "Top Losers"])
with tab1:
    st.subheader("Top Gainers")
    for item in tg:
        security_id = item['securityID']
        pchange = item['pChange']
        st.metric("",f"{security_id}",delta=f"{pchange}",label_visibility="collapsed")
with tab3:
    st.subheader("Top Losers")
    for item in tl:
        security_id = item['securityID']
        pchange = item['pChange']
        st.metric("",f"{security_id}",delta=f"{pchange}",delta_color="normal",label_visibility="collapsed")
    
while True:
    with price_placeholder:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('NIFTY 50', f"{nifty_price:.2f}",delta=f"{nifty_delta}")
        col2.metric('BANK NIFTY', f"{bank_nifty_price:.2f}",delta=f"{bank_delta}")
        col3.metric('NIFTY IT', f"{nifty_it_price:.2f}",delta=f"{it_delta}")
        col4.metric('SENSEX', f"{sensex_price:.2f}",delta=f"{sensex_delta}")

    nifty_price = get_nifty_price()
    nifty_delta = get_nifty_delta()
    bank_nifty_price = get_bank_nifty_price()
    bank_delta = get_bank_delta()
    nifty_it_price = get_nifty_it()
    it_delta = get_IT_delta()
    sensex_price = get_sensex_price()
    sensex_delta = get_sensex_delta()
    time.sleep(1)