from aiogram import types, html
import time
import requests
import time_module, io_module
eu_flag = "\U0001F1EA\U0001F1FA" #колхозный метод получения флага ес

def get_change(price1: float, price2: float):
    change = round(price1 - price2, 2)
    return f"+{change}$" if change >= 0 else f"{change}$"

def coin_formating(coin: str, r: int) -> str:

    if r == 0:
        coin = "TON" if coin == "the-open-network" else coin 
        coin = "BTC" if coin == "bitcoin" else coin
        coin = "ETH" if coin == "ethereum" else coin
    else:
        coin = "the-open-network" if coin.lower() == "ton" else coin 
        coin = "bitcoin" if coin.lower() == "btc"else coin
        coin = "ethereum" if coin.lower() == "eth" else coin

    return coin

def user_info(message: types.Message) -> str:

    text = (
        f"message_id={message.message_id}\n"
        f"user_id={message.from_user.id}\n"
        f"first_name={message.from_user.first_name}\n"
        f"username={message.from_user.username}\n"
        f"text={message.text}"
    )

    html.quote(text)

    print(text)

    return text #возвращает все это чтобы потом скинуть в чат овнеру бота

def command_course(message: types.Message, coin: str, times: list) -> str:

    time_get = time_module.TimeGet()
    prices = get_price_inpast(coin, times)
    coin_user = coin_formating(coin, 0)  #коин в формате для пользователя 
    time_out = []
    text = (
        f"{html.quote(f"{coin_user} to USDT course{eu_flag}: ")}"
        f"\n"
        f"<blockquote>"
    )
    for hour, price in zip(times, prices): #цикловый сборщик текста
        time_string = "current price" if hour == 0 else f"{hour} hour(s) ago"
        only_time = time_get.get_time(hour)
        time_out.append(only_time)
        text = text + (
            f"<b>{html.quote(f"price: {price}$")}</b>"
            f"\n"
            f"<b>{html.quote(time_string)}</b>"
            f"\n"
            f"<i>{html.quote(f"time: {only_time.time}\ndate: {only_time.date}\n")}</i>"
            f"\n\n"
        )
    text = text + (f"</blockquote>")
        
    data = io_module.OneRequestStorage(
        coin_user,
        message.from_user.id,

        prices,
        time_out
    )

    io_module.write_data(data)
    return text #короче я вторую часть обновления доделал, но мне капец как кажется что тут баг на баге

def get_price_json(url, params):
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Data request error: {e}")
        return None

def get_price_inpast(coin: str, hours_ago: list): # я эту функцию полностью переработал, я раньше изза того что ее навайбкодил не понимал как она работает и хуячил по 3 реквеста на команду
    target_ms = [(time.time() - (h * 3600)) * 1000 for h in hours_ago] 
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": "2"} #к параметрам прибавляется колво дней за которые надо скачать данные
    result = []
    
    data = get_price_json(url, params)
    if data == None:
        return [0]*len(hours_ago)
    
    for ms in target_ms:
        closest_point = min(data["prices"], key=lambda x: abs(x[0] - ms)) #better call gemini птмш я хз как этот джсон устроен потом разберусь
        price = round(closest_point[1], 2) 
        result.append(price)

    return result
        
