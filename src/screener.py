import pandas as pd
from .data_fetcher import DataFetcher

class Screener:
    def __init__(self, polygon_key):
        self.fetcher = DataFetcher(polygon_key)
    
    def calculate_edge(self, ticker, beat_rate, momentum, sentiment):
        implied_prob = 0.5
        my_prob_beat = beat_rate * (1 + sentiment)
        avg_gain = 8
        avg_loss = -4
        er = (my_prob_beat * avg_gain) + ((1 - my_prob_beat) * avg_loss)
        edge = er - (implied_prob * avg_gain + (1 - implied_prob) * avg_loss)
        if momentum['ret5d'] > 3 and momentum['vol_spike'] > 1.5 and sentiment > 0.1:
            return max(edge, 0) / 100  # Jako procento
        return 0
    
    def screen(self, start_date, end_date):
        earnings = self.fetcher.get_earnings_calendar(start_date, end_date)
        scores = []
        for ticker in earnings['ticker']:
            beat = self.fetcher.get_beat_history(ticker)
            if beat > 0.7:
                mom = self.fetcher.get_momentum(ticker)
                sent = self.fetcher.get_sentiment(ticker)
                edge = self.calculate_edge(ticker, beat, mom, sent)
                er = (beat * 8) + ((1 - beat) * -4)  # Simplified ER
                scores.append({'ticker': ticker, 'edge': edge, 'er': er})
        df = pd.DataFrame(scores).sort_values('edge', ascending=False)
        return df.head(20)  # Top 20
