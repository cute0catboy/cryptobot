from datetime import datetime
from aiogram.utils import markdown
from aiogram import types, html
import time
import requests
eu_flag = "\U0001F1EA\U0001F1FA" #колхозный метод получения флага ес

def coin_formating(coin: str) -> str:

    coin = "TON" if coin == "the-open-network" else coin 
    coin = "BTC" if coin == "bitcoin" else coin
    coin = "ETH" if coin == "ethereum" else coin

    return coin #возвращает коин именно в виде для написания в command_course

def get_time() -> tuple:
    now = datetime.now()
    time_day = now.strftime("%d.%m.%Y")
    time_hours = now.strftime("%H:%M:%S")

    return (time_day, time_hours) #("29.10.2026", "15:56:08")

def user_info(message: types.Message) -> str:

    text = markdown.text(
        f"id={message.from_user.id}",
        f"first_name={message.from_user.first_name}",
        f"username={message.from_user.username}",
        f"text={message.text}",
        sep="\n"
    )

    print(f"id={message.from_user.id}")
    print(f"first_name={message.from_user.first_name}")
    print(f"username={message.from_user.username}")
    print(f"text={message.text}")

    return text #возвращает все это чтобы потом скинуть в чат овнеру бота

def command_course(coin: str) -> str:

    price = get_price(coin)
    time.sleep(10)
    price_hour = get_price_inpast(coin, "h")
    time.sleep(10)
    price_day = get_price_inpast(coin, "d")
    time.sleep(10) #получает цены со слипом потому что там на апи лимит на бесплатные запросы

    change_h = round(price - price_hour, 4)
    change_d = round(price - price_day, 4) #округление цены до нормального вида

    change_h_str = f"+{change_h}" if change_h >= 0 else f"{change_h}"
    change_d_str = f"+{change_d}" if change_d >= 0 else f"{change_d}" #ставит плюс(или нет) к изменению цены, для внешнего вида

    coin = coin_formating(coin)  #коин в формате для пользователя

    coin_safe = html.quote(coin)
    price_safe = html.quote(str(price))
    price_hour_safe = html.quote(str(price_hour))
    price_day_safe = html.quote(str(price_day))
    change_h_safe = html.quote(change_h_str)
    change_d_safe = html.quote(change_d_str) #тут просто куоте всех переменных с припиской _safe

    now = get_time()
    formatted_date_time_day = html.quote(str(now[0]))
    formatted_date_time_time = html.quote(str(now[1])) #тоже прост форматирование но теперь времени

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
    ) #сам текст, ничего сложного
    
    return text

def get_price(coin: str):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {f"ids": {coin}, "vs_currencies": "usd"}

    try:
        response = requests.get(url, params=params, timeout=10) #запрос данных с коингеко апи, к сожалению блокировка для нищих есть
        response.raise_for_status() 
        data = response.json() #вся инфа в json экспортится. надо сделать чтобы она сохранялась, типо можно получить все свои предыдущие запросы.

        price = data[coin]["usd"] #отношение цены коин-юсд
        return price
    except Exception as e:
        print(f"Data request error: {e}") #ес че пошло не так
        return 0

def get_price_inpast(coin: str, time_offset: str): #функция хз как работает наполовину вайбкодил (closest_point)
    if time_offset == "h":
        days = "1"
        hours_ago = 1
    else:
        days = "2"
        hours_ago = 24 #конвертация, колхозно

    target_ms = (time.time() - (hours_ago * 3600)) * 1000
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": days} #к параметрам прибавляется колво дней за которые надо скачать данные
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json() #тоже самое что в обычном гет прайс
        
        def check_time(x):
            return abs(x[0] - target_ms) #better call gemini
            
        closest_point = min(data["prices"], key=check_time) #better call gemini

        price = round(closest_point[1], 2) #округление идет тут ну и ладно

        return price
        
    except Exception as e:
        print(f"Data request error: {e}")
        return 0