import streamlit as st
import requests
from bs4 import BeautifulSoup
from dateutil import parser

st.set_page_config(page_title="StockUP", layout="wide", page_icon=":chart_with_upwards_trend:",)

css = """
<style>
[data-testid="StyledLinkIconContainer"]{
text-align: center;
}
[id="news"]{
padding:0px;
}
[data-testid="stAppViewBlockContainer"]{
padding-top:60px;
}
[class="st-emotion-cache-1kyxreq e115fcil2"]{
    justify-content: center;
    align-items: center;  
}
[class="st-emotion-cache-10trblm e1nzilvr1"]{
    text-align: left;
    height: 100%;
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)
st.header("News")
st.divider()

news = requests.get('https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms')
soup = BeautifulSoup(news.text, "xml")

titles = soup.findAll("title")
descriptions = soup.findAll("description")
links = soup.findAll("link")
image_urls = [enclosure.get('url') for enclosure in soup.findAll("enclosure")]
dates = soup.findAll("pubDate")
col1,col2 = st.columns(2)   
with col1:
        for image_url, date_str in zip( image_urls, dates):
            date = parser.parse(date_str.text)
            if image_url:
                st.image(image_url,width=350)
            else:
                st.write(f"Date: {date_str.text}")
                st.divider()
with col2:
    with st.container():
        for title, description, link,date_str in zip(titles[2:], descriptions[1:], links[2:],dates):
            date = parser.parse(date_str.text)
            st.subheader(title.text)
            st.write(description.text)
            st.link_button("Read More", link.text)
            st.write(f"{date.strftime('%Y-%m-%d %H:%M:%S')}")
            st.divider()