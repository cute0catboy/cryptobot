from aiogram import Bot, Dispatcher, types
import asyncio
import logging
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode
import config 
import requests
from datetime import datetime

dp = Dispatcher()
eu_flag = "\U0001F1EA\U0001F1FA"

def user_info(message: types.Message):

    print(f"id={message.from_user.id}")
    print(f"first_name={message.from_user.first_name}")
    print(f"username={message.from_user.username}")
    print(f"text={message.text}")

@dp.message(CommandStart())
async def command_start(message: types.Message):

    user_info(message)
    
    text = f"Hi, {markdown.hbold(message.from_user.username)}! /help to know more"
        
    await message.answer(
        text=text,
        parse_mode=ParseMode.HTML)

@dp.message(Command("help"))
async def handle_help(message: types.Message):

    user_info(message)

    text = markdown.text(
        markdown.markdown_decoration.italic(markdown.markdown_decoration.quote(f"Crypto-helper(especially for euroteam{eu_flag}{eu_flag})")),
        markdown.markdown_decoration.quote("/btc to get bitcoin-usdt course"),
        markdown.markdown_decoration.quote("/eth to get ethereum-usdt course"),
        markdown.markdown_decoration.quote("/ton to get ton-usdt course"),
        sep="\n"
    )
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)

@dp.message(Command("ton"))
async def command_btc(message: types.Message):

    user_info(message)

    price = get_price("the-open-network")
    safe_price = str(price).replace(".", r"\.")

    now = datetime.now()
    formatted_date_time_day = now.strftime("%d.%m.%Y")
    formatted_date_time_time = now.strftime("%H:%M:%S")

    text = markdown.text(
        f"Current TON to USDT course{eu_flag}: \n",
        markdown.text(
            f" *{safe_price}$*\n",
            markdown.markdown_decoration.italic(markdown.markdown_decoration.quote(f"day: {formatted_date_time_day}\n")),
            markdown.markdown_decoration.italic(markdown.markdown_decoration.quote(f"time: {formatted_date_time_time}\n"))
            ),
        sep = ""
    )
    await message.answer(text=text,
                         parse_mode=ParseMode.MARKDOWN_V2)

@dp.message(Command("btc"))
async def command_btc(message: types.Message):

    user_info(message)

    price = get_price("bitcoin")
    safe_price = str(price).replace(".", r"\.")

    now = datetime.now()
    formatted_date_time_day = now.strftime("%d.%m.%Y")
    formatted_date_time_time = now.strftime("%H:%M:%S")

    text = markdown.text(
        f"Current BTC to USDT course{eu_flag}: \n",
        markdown.text(
            f" *{safe_price}$*\n",
            markdown.markdown_decoration.italic(markdown.markdown_decoration.quote(f"day: {formatted_date_time_day}\n")),
            markdown.markdown_decoration.italic(markdown.markdown_decoration.quote(f"time: {formatted_date_time_time}\n"))
            ),
        sep = ""
    )
    await message.answer(text=text,
                         parse_mode=ParseMode.MARKDOWN_V2)

@dp.message(Command("eth"))
async def command_btc(message: types.Message):

    user_info(message)

    price = get_price("ethereum")
    safe_price = str(price).replace(".", r"\.")

    now = datetime.now()
    formatted_date_time_day = now.strftime("%d.%m.%Y")
    formatted_date_time_time = now.strftime("%H:%M:%S")

    text = markdown.text(
        f"Current ETH to USDT course{eu_flag}: \n",
        markdown.text(
            f" *{safe_price}$*\n",
            markdown.markdown_decoration.italic(markdown.markdown_decoration.quote(f"day: {formatted_date_time_day}\n")),
            markdown.markdown_decoration.italic(markdown.markdown_decoration.quote(f"time: {formatted_date_time_time}\n"))
            ),
        sep = ""
    )
    await message.answer(text=text,
                         parse_mode=ParseMode.MARKDOWN_V2)

@dp.message()
async def echo(message: types.Message):

    user_info(message)

    try:
      await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="smth new")

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

def get_price(coin: str):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {f"ids": {coin}, "vs_currencies": "usd"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() 
        data = response.json()

        price = data[coin]["usd"]
        return f"{price}"
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return "Nan"

async def main():
    bot = Bot(token=config.Token)
    logging.basicConfig(level=logging.INFO) 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())