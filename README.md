<b>CRYPTOBOT<b>

итак, ты решил стать криптотрейдером

main.py(только действия бота):

базовые команды:
/start
/help

крипто стафф:
/btc
/eth
/ton

core.py(всякие бизнес функции):
coin_formating(coin: str) -> str: форматирует коин в подходящее для вывода имя
get_time() -> tuple: получает текущае время(дата, часы)
user_info(message: types.Message) -> str: пишет инфу о сообщении в бот, возвращает ее как стринг
command_course(coin: str) -> str: возвращает текст для команды о курсе валюты
get_price(coin: str): получает текущую цену
get_price_inpast(coin: str, time_offset: str): получает цену час; день назад
более полное описание в комментах в самом файле core.py

чтобы запустить своего бота нужно создать в папке .env файл и в нем написать
TOKEN=токен тг бота
OWNER_ID=ид аккаунта для логов

все айди крипты тут:

# =====================================================================
# СПРАВОЧНИК ИДЕНТИФИКАТОРОВ (ids) ДЛЯ ЗАПРОСОВ К COINGECKO API
# Передавайте эти значения в params={"ids": "ИДЕНТИФИКАТОР", ...}
# =====================================================================
#
# --- МЕЙНСТРИМ / КРУПНЕЙШИЕ МОНЕТЫ ---
# "bitcoin"                   - Bitcoin (BTC)
# "ethereum"                  - Ethereum (ETH)
# "ripple"                    - Ripple (XRP)
# "solana"                    - Solana (SOL)
# "cardano"                   - Cardano (ADA)
# "polkadot"                  - Polkadot (DOT)
# "litecoin"                  - Litecoin (LTC)
# "chainlink"                 - Chainlink (LINK)
#
# --- ЭКОСИСТЕМА TON И TELEGRAM ---
# "the-open-network"          - Toncoin (TON)
# "notcoin"                   - Notcoin (NOT)
# "dogs-2"                    - Dogs (DOGS)
#
# --- БИРЖЕВЫЕ ТОКЕНЫ ---
# "binancecoin"               - BNB (Binance Coin)
#
# --- СТЕЙБЛКОИНЫ (Курс всегда ~1 USD) ---
# "tether"                    - Tether (USDT)
# "usd-coin"                  - USDC
# "first-digital-usd"         - FDUSD
#
# --- ПОПУЛЯРНЫЕ МЕМ-КОИНЫ ---
# "dogecoin"                  - Dogecoin (DOGE)
# "shiba-inu"                 - Shiba Inu (SHIB)
# "pepe"                      - Pepe (PEPE)
#
# =====================================================================

