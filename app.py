from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHANNEL_ID,
            "text": message
        },
        timeout=10
    )

    return response.json()


@app.route("/", methods=["GET"])
def home():
    return "TradingView Telegram Bot is running."


@app.route("/tradingview", methods=["POST"])
def tradingview():
    data = request.get_json(silent=True) or {}

    symbol = data.get("symbol", "Unknown")
    signal = data.get("signal", "Unknown")
    price = data.get("price", "Unknown")

    if signal == "RSI30":
        message = (
            f"🟢 {symbol}\n"
            f"RSI(21) reached 30\n"
            f"Timeframe: 1m\n"
            f"Price: {price}"
        )

    elif signal == "RSI70":
        message = (
            f"🔴 {symbol}\n"
            f"RSI(21) reached 70\n"
            f"Timeframe: 1m\n"
            f"Price: {price}"
        )

    else:
        return {"status": "ignored"}, 200

    telegram_result = send_telegram(message)

    return {
        "status": "ok",
        "telegram": telegram_result
    }, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
