# QuantValueBetTrader

Automatizovaný quant tool pro screening value bet akcií s RL učením. Běží na Streamlit, rebalancuje týdně.

## Instalace
1. Clone repo: `git clone https://github.com/yourusername/QuantValueBetTrader.git`
2. `pip install -r requirements.txt`
3. Nastav env vars: `export POLYGON_API_KEY=your_key`
4. Spusť: `streamlit run app.py`

## Automatizace
- Týdenní rebalance: GitHub Actions (pondělí 9:00 UTC).
- RL: Učí se z historických returnů pro lepší výběry.

## Použití
Otevři v prohlížeči: localhost:8501. Zobrazí top 20 akcií, historický výkon, RL stavy.

## RL Logika
- Environment: Trading gym – stavy = features (edge, momentum), akce = vybrat/nesvybrat akcii.
- Reward: Return - riziko (volatilita).
- Trénink: Q-Learning, aktualizováno po každém rebalance.

NFA – pro vzdělávací účely.
