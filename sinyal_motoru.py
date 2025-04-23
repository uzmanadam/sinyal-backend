import time
import json
import asyncio
import websockets
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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
    return price_tag.text if price_tag else "N/A"

@app.get("/")
def read_root():
    return {"mesaj": "Sinyal API çalışıyor!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(2)
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
