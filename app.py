import streamlit as st
from src.screener import Screener
from src.rl_agent import QLearningAgent
from src.backtester import backtest_portfolio
from src.data_fetcher import DataFetcher
from datetime import datetime, timedelta
import os

st.title("QuantValueBetTrader Dashboard")

# Config
POLYGON_KEY = os.getenv('POLYGON_API_KEY', 'demo')  # Default demo

# Inicializace
fetcher = DataFetcher(POLYGON_KEY)
screener = Screener(POLYGON_KEY)
agent = QLearningAgent()

# Týdenní data
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

if st.button("Run Weekly Screen & Rebalance"):
    screened = screener.screen(start_date, end_date)
    st.write("Screened Results:")
    st.dataframe(screened)
    
    # RL Rebalance
    picks = agent.rebalance(screened)
    st.write("RL-Rebalanced Portfolio:")
    st.json(picks)
    
    # Learn from past
    agent.learn_from_past()
    
    # Backtest
    bt = backtest_portfolio(picks, start_date, end_date)
    st.write(f"Avg Return: {bt['avg_return']:.2%}")

# Vizualizace historie
try:
    history = agent.load_history()
    st.write("Portfolio History:", history)
except:
    st.write("No history yet.")

# Automatický scheduling (lokálně – pro cloud použij Actions)
import schedule
import time

def job():
    # Spusť screening (simulace v app)
    st.rerun()

schedule.every().monday.at("09:00").do(job)

if st.checkbox("Run Scheduler (Local)"):
    while True:
        schedule.run_pending()
        time.sleep(60)
