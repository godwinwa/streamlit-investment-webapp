import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from stocksymbol import StockSymbol

class webscraper:
    
    def default_tickers(self):
        #Returns stock tickers
        api_key = '5e351c12-26b8-48af-84b3-91a4618d834d'
        ss = StockSymbol(api_key)
        symbol_list_us = ss.get_symbol_list(market="US")
        df = pd.DataFrame(symbol_list_us)
        return df
    
    def stock_price(self,ticker, time='20y'):
        #Returns stock prices
        ticker_object = yf.Ticker(ticker)
        hist = ticker_object.history(period=time)
        return hist
    
    def webscrape_site(self, url):
        #Returns scraped site
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    
    def get_amount_articles(self, soup):
        #Get the amount of news articles
        amount_articles = len(soup.findAll('h3', {'class': 'Mb(5px)'}))
        return amount_articles
    
    
    def get_stock_news(self, soup, amount_articles):
        #Returns stock news with header
        news_items = {}
        for i in range(amount_articles):
            news_class = str(soup.findAll('h3', {'class': 'Mb(5px)'})[i])
            news_header_start = news_class.find('-->') + 3
            news_header_end = news_class.find('<!-- /react-text -')
            news_header = news_class[news_header_start:news_header_end].strip()
            news_link_start = news_class.find('href="') + 6
            news_link_end = news_class.find('"><u class="StretchedBo')
            news_link = 'https://finance.yahoo.com' + news_class[news_link_start:news_link_end].strip()
            news_items[i] = news_header, news_link
        
        return news_items
         
        