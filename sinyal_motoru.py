import time
import json
import asyncio
import websockets
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

BIST_SYMBOLS = {
    "THYAO": "https://tr.investing.com/equities/turk-hava-yollari",
    "ASELS": "https://tr.investing.com/equities/aselsan-elektronik",
    "SISE": "https://tr.investing.com/equities/sise-cam"
}

FILTER_CRITERIA = ["BUY", "SELL", "WATCH"]

async def fetch_price(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=100"
    response = requests.get(url)
    data = response.json()
    close_prices = [float(candle[4]) for candle in data]
    return close_prices

async def fetch_bist_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    price_tag = soup.find("span", {"data-test": "instrument-price-last"})
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"mesaj": "Sinyal API çalışıyor!"}
from fastapi import WebSocket
import json

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text(json.dumps({
        "signals": [
            {
                "symbol": "BTCUSDT",
                "type": "BUY",
                "exchange": "Binance",
                "price": 10000,
                "rsi": 35,
                "macd": 1.2,
                "ema_cross": True
            }
        ]
    }))
from fastapi import WebSocket
import asyncio

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(2)  # örnek için 2 saniyede bir
        await websocket.send_json({
            "signals": [
                {
                    "symbol": "ASELS",
                    "exchange": "BIST",
                    "type": "BUY",
                    "price": 45.30,
                    "rsi": 68,
                    "macd": 1.2,
                    "ema_cross": True
                }
            ]
        })

