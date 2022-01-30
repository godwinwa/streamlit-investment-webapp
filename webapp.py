import streamlit as st
from scraper import webscraper
from PIL import Image
from search_web import redit_post
import datetime
from stocksymbol import StockSymbol



#Page settings
image_icon = Image.open('icon.jpg')

st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
	page_title='Invest06',  # String or None. Strings get appended with "• Streamlit". 
	page_icon=image_icon ,  # String, anything supported by st.image, or None.
)

stock = webscraper()

@st.cache(suppress_st_warning=True)
def default_stock_ticker(class_name):
    #default stock tickers
    stock = class_name
    return stock.default_tickers()['symbol']

@st.cache(suppress_st_warning=True)
def get_stock_price(class_name, ticker, time='20y'):
    #Get stock price
    stock = class_name
    
    return stock.stock_price(ticker, time)


def news(class_name, add_selectbox):
    #show news
    stock = class_name
    yahoo_soup = stock.webscrape_site('https://finance.yahoo.com/topic/{}'.format(add_selectbox))
    amount_articles = stock.get_amount_articles(yahoo_soup)
    yahoo_get_headers = stock.get_stock_news(yahoo_soup, amount_articles)
    for i in range(amount_articles):
        st.write(yahoo_get_headers[i][0])
        link = yahoo_get_headers[i][1]
        st.caption("Read the article [link](%s)" % link)
        
    st.write(st.write(amount_articles, 'articles'))
    return None

#Sidebar
add_selectbox = st.sidebar.selectbox(
    "Investment type",
    ("stock-market-news", "crypto", 'redit')
)

#Header
st.markdown("<h1 style='text-align: center; color: white;'>Investment App</h1>", unsafe_allow_html=True)

#Page layout
col1, col2, col3 = st.columns(3)

def popular_funds_status():
    #Show percentage increase s&p500 And nasdaq

    sp_500 = get_stock_price(stock, '^GSPC', '1d')
    difference_sp_500 = round(float(sp_500['Close'] - sp_500['Open']) / sp_500['Open'] * 100, 2)
    col3.metric(label="S&P 500", value=float(sp_500['Open']), delta="{}%".format(float(difference_sp_500)))

    nasdaq = get_stock_price(stock, '^IXIC', '1d')
    difference_nasdaq = round(float(nasdaq['Close'] - nasdaq['Open']) / nasdaq['Open'] * 100, 2)
    col3.metric(label="NASDAQ", value=float(nasdaq['Open']), delta="{}%".format(float(difference_nasdaq)))

    return None

def popular_crypto_status():
    #Show percentage increase bitcoin and ethereum

    btc_usd = get_stock_price(stock, 'btc-usd', '1d')
    difference_btc_usd = round(float(btc_usd['Close'] - btc_usd['Open']) / btc_usd['Open'] * 100, 2)
    col3.metric(label="BTC (USD)", value=float(btc_usd ['Open']), delta="{}%".format(float(difference_btc_usd)))

    eth_usd = get_stock_price(stock, 'eth-usd', '1d')
    difference_eth_usd  = round(float(eth_usd ['Close'] - eth_usd['Open']) / eth_usd['Open'] * 100, 2)
    col3.metric(label="ETH (USD)", value=float(eth_usd ['Open']), delta="{}%".format(float(difference_eth_usd)))

    return None


#Pick stock
default_ticker_options = default_stock_ticker(stock)

if add_selectbox == 'stock-market-news': #stock page
    
    image = Image.open('buffet.jpg')
    col1.image(image)

    popular_funds_status()
   
    with col2:
        pick_ticker = st.selectbox('Pick a stock ticker', (default_stock_ticker(stock)))
        stock_ticker = st.text_input('Your stock ticker:')
        number = st.number_input('Years to go back:', min_value=1, step=1)
    

    if col2.button('Load data'):
        st.write(stock_ticker)
        try:
            if number != 0:
                years = str(number) + 'y'
                if stock_ticker != '': #Use input if typed in 
                    data = get_stock_price(stock, stock_ticker, years)
                    
                    st.line_chart(data[['Open']])
                
                    st.success('Data fetched succesfully')
                else: #Use default options when chosen
                    data = get_stock_price(stock, pick_ticker, years)
                    
                    st.line_chart(data[['Open']])
                
                    st.success('Data fetched succesfully')
        except:
            st.error('Stock ticker can not be found')
elif add_selectbox == 'crypto': #crypto page
    image = Image.open('crypto.jpg')
    col1.image(image)
    popular_crypto_status()

    with col2:
        pick_ticker = st.selectbox('Pick a stock ticker', ('BTC-USD', 'ETH-USD', 'BNB-USD'))
        stock_ticker = st.text_input('Your stock ticker:')
        number = st.number_input('Years to go back:', min_value=1, step=1)
    

    if col2.button('Load data'):
        st.write(stock_ticker)
        try:
            if number != 0:
                years = str(number) + 'y'
                if stock_ticker != '': #Use input if typed in 
                    data = get_stock_price(stock, stock_ticker, years)
                    
                    st.line_chart(data[['Open']])
                
                    st.success('Data fetched succesfully')
                else: #Use default options when chosen
                    data = get_stock_price(stock, pick_ticker, years)
                    
                    st.line_chart(data[['Open']])
                
                    st.success('Data fetched succesfully')
        except:
            st.error('Stock ticker can not be found')


@st.cache(suppress_st_warning=True)
def get_redit_news():
    redit = redit_post()
    df = redit.get_posts()
    return df

if add_selectbox == 'redit': #redit page
    
    df = get_redit_news()
    st.dataframe(df)
    col1, col2, col3 = st.columns(3)

    
if col1.checkbox('Click to see latest news'):
    news(stock, add_selectbox)


#Hide streamlit logo
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)