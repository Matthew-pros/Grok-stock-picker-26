import yfinance as yf
from polygon import RESTClient
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self, polygon_key):
        self.client = RESTClient(api_key=polygon_key)
    
    def get_earnings_calendar(self, start_date, end_date):
        # Scrape Yahoo Earnings Calendar
        url = f"https://finance.yahoo.com/calendar/earnings?from={start_date}&to={end_date}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Parse tabulku – jednoduchá verze, rozšiřit pro robustnost
        tickers = []  # Extrahuj z <td> tags, např. NVDA, HD atd.
        # Simulace: Použij yfinance pro tickers
        universe = ['NVDA', 'HD', 'PDD', 'WMT', 'TGT', 'MDT', 'AMD', 'SMCI', 'APH', 'ADBE', 'PGR', 'EME', 'DOV', 'IREN', 'ARWR']
        df = pd.DataFrame({'ticker': universe, 'date': [start_date]*len(universe)})
        return df
    
    def get_beat_history(self, ticker, quarters=4):
        # Použij yfinance pro historická earnings
        stock = yf.Ticker(ticker)
        earnings = stock.earnings_dates.tail(quarters)
        if earnings.empty:
            return 0.5  # Default
        beats = (earnings['Reported EPS'] > earnings['EPS Estimate']).mean()
        return beats
    
    def get_momentum(self, ticker):
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1mo')
        if len(hist) < 5:
            return {'ret5d': 0, 'vol_spike': 1, 'rsi': 50}
        ret5d = (hist['Close'][-1] - hist['Close'][-5]) / hist['Close'][-5] * 100
        vol_spike = hist['Volume'][-1] / hist['Volume'][:-1].mean()
        # RSI calculation (zjednodušené)
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        return {'ret5d': ret5d, 'vol_spike': vol_spike, 'rsi': rsi}
    
    def get_sentiment(self, ticker):
        # Simulace X sentimentu přes textblob (v reálu integrovat API)
        # Předpokládej pozitivní pro top tickers
        return 0.2 if ticker in ['NVDA', 'AMD'] else 0.1  # Placeholder
