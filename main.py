from aiogram import Bot, Dispatcher, types, html
import asyncio
import logging
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode
import config 
import requests
from datetime import datetime
import time

dp = Dispatcher()
eu_flag = "\U0001F1EA\U0001F1FA"

def coin_formating(coin: str) -> str:

    coin = "TON" if coin == "the-open-network" else coin
    coin = "BTC" if coin == "bitcoin" else coin
    coin = "ETH" if coin == "ethereum" else coin

    return coin

def get_time() -> tuple:
    now = datetime.now()
    time_day = now.strftime("%d.%m.%Y")
    time_hours = now.strftime("%H:%M:%S")

    return (time_day, time_hours)

def user_info(message: types.Message):

    print(f"id={message.from_user.id}")
    print(f"first_name={message.from_user.first_name}")
    print(f"username={message.from_user.username}")
    print(f"text={message.text}")

def command_course(message: types.Message, coin: str) -> str:
    user_info(message)

    price = get_price(coin)
    time.sleep(10)
    price_hour = get_price_inpast(coin, "h")
    time.sleep(10)
    price_day = get_price_inpast(coin, "d")

    change_h = round(price - price_hour, 4)
    change_d = round(price - price_day, 4)

    change_h_str = f"+{change_h}" if change_h >= 0 else f"{change_h}"
    change_d_str = f"+{change_d}" if change_d >= 0 else f"{change_d}"

    coin = coin_formating(coin)

    coin_safe = html.quote(coin)
    price_safe = html.quote(str(price))
    price_hour_safe = html.quote(str(price_hour))
    price_day_safe = html.quote(str(price_day))
    change_h_safe = html.quote(change_h_str)
    change_d_safe = html.quote(change_d_str)

    now = get_time()
    formatted_date_time_day = html.quote(str(now[0]))
    formatted_date_time_time = html.quote(str(now[1]))

    text = (
        f"Current {coin_safe} to USDT course{eu_flag}: \n"
        f"<b>{price_safe}$</b>\n"
        f"<blockquote>"
        f"<i>day: {formatted_date_time_day}</i>\n"
        f"<i>time: {formatted_date_time_time}</i>\n\n"
        f"Hour ago: \n"
        f" <b>{price_hour_safe}$</b>\n"
        f" Difference: {change_h_safe}$\n\n"
        f"Day ago: \n"
        f" <b>{price_day_safe}$</b>\n"
        f" Difference: {change_d_safe}$\n"
        f"</blockquote>"
    )
    
    return text

@dp.message(CommandStart())
async def command_start(message: types.Message):

    user_info(message)
    
    text = f"Hi, {markdown.hbold(message.from_user.username)}! /help to know more"
        
    await message.answer(
        text=text,
        parse_mode=ParseMode.HTML)

@dp.message(Command("help"))
async def command_help(message: types.Message):

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
async def command_ton(message: types.Message):

    await message.reply(text="Wait up to 30 seconds...")

    text = command_course(message, "the-open-network")

    await message.answer(text=text,
                         parse_mode=ParseMode.HTML)

@dp.message(Command("btc"))
async def command_ton(message: types.Message):

    await message.reply(text="Wait up to 30 seconds...")

    text = command_course(message, "bitcoin")

    await message.answer(text=text,
                         parse_mode=ParseMode.HTML)

@dp.message(Command("eth"))
async def command_ton(message: types.Message):

    await message.reply(text="Wait up to 30 seconds...")

    text = command_course(message, "ethereum")

    await message.answer(text=text,
                         parse_mode=ParseMode.HTML)

@dp.message()
async def echo(message: types.Message):

    user_info(message)

    try:
      await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="smth new")

def get_price(coin: str):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {f"ids": {coin}, "vs_currencies": "usd"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() 
        data = response.json()

        price = data[coin]["usd"]
        return price
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return 0

def get_price_inpast(coin: str, time_offset: str): #функция хз как работает наполовину вайбкодил (closest_point)
    if time_offset == "h":
        days = "1"
        hours_ago = 1
    else:
        days = "2"
        hours_ago = 24

    target_ms = (time.time() - (hours_ago * 3600)) * 1000
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        def check_time(x):
            return abs(x[0] - target_ms)
            
        closest_point = min(data["prices"], key=check_time)
        
        price = round(closest_point[1], 2)

        return price
        
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return 0

async def main():
    bot = Bot(token=config.Token)
    logging.basicConfig(level=logging.INFO) 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())