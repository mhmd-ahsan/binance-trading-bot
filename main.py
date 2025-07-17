from telethon.sync import TelegramClient, events
from binance.client import Client
import asyncio
import re

# === TELEGRAM CREDENTIALS ===
api_id = 25507216  # ✅ Your Telegram API ID
api_hash = '8477a4c8985553313ef956725f3999ee'  # ✅ Your Telegram API Hash
phone = '+923116620121'  # 🔁 Replace with your actual Telegram number

# === BINANCE CREDENTIALS ===
api_key = 'uxMwErj7ltG22INXH8fqtigawmmoGOI wasVxnvcudQ4MvqmFp4iMa4gColLu GbF6'  # ⛔ Do NOT share
api_secret = 'dgFFHweH4JACIIto9U1CtbERbkl2mJ8 Q2BqFB6FPYOQYMuLn5dswydMEIUfd 5TpC'  # ⛔ Do NOT share

# === TRADE SETTINGS ===
TRADE_USDT_AMOUNT = 5
DEFAULT_LEVERAGE = 10

# === INIT BINANCE CLIENT ===
client = Client(api_key, api_secret)
client.FUTURES_BASE_URL = 'https://fapi.binance.com'

# === GET VALID USDT-PAIR SYMBOLS ===
exchange_info = client.futures_exchange_info()
valid_symbols = set()
symbol_map = {}

for s in exchange_info['symbols']:
    if s['quoteAsset'] == 'USDT' and s['contractType'] == 'PERPETUAL':
        symbol = s['symbol']
        base = s['baseAsset']
        valid_symbols.add(base)
        symbol_map[base] = symbol

# === INIT TELEGRAM CLIENT ===
tg_client = TelegramClient('session_name', api_id, api_hash)

# === BOT LOGIC ===
async def main():
    await tg_client.start(phone=phone)

    @tg_client.on(events.NewMessage)
    async def handler(event):
        msg = event.message.message.upper().strip()

        if "BULLISH" not in msg:
            print("🔕 No 'bullish' keyword — ignoring")
            return

        for coin in valid_symbols:
            if re.search(rf'\b{coin}\b', msg):
                symbol = symbol_map[coin]
                print(f"✅ Bullish signal for {symbol}")

                try:
                    # Set leverage
                    client.futures_change_leverage(symbol=symbol, leverage=DEFAULT_LEVERAGE)

                    # Place a $5 market BUY order
                    order = client.futures_create_order(
                        symbol=symbol,
                        side='BUY',
                        type='MARKET',
                        quoteOrderQty=TRADE_USDT_AMOUNT
                    )
                    print("✅ Order placed:", order)
                except Exception as e:
                    print(f"❌ Error placing trade: {e}")
                break

    print("🚀 Bot is running... Waiting for bullish signals")
    await tg_client.run_until_disconnected()

asyncio.run(main())
