from aiogram import types, html
import time
import requests
import time_module, io_module
eu_flag = "\U0001F1EA\U0001F1FA" #колхозный метод получения флага ес

def get_change(price1: float, price2: float):
    change = round(price1 - price2, 2)
    return f"+{change}$" if change >= 0 else f"{change}$"

def coin_formating(coin: str) -> str:

    coin = "TON" if coin == "the-open-network" else coin 
    coin = "BTC" if coin == "bitcoin" else coin
    coin = "ETH" if coin == "ethereum" else coin

    return coin #возвращает коин именно в виде для написания в command_course

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
    coin_user = coin_formating(coin)  #коин в формате для пользователя 
    text = (
        f"{html.quote(f"{coin_user} to USDT course{eu_flag}: ")}"
        f"\n"
        f"<blockquote>"
    )
    for hour, price in zip(times, prices):
        time_string = "current price" if hour == 0 else f"{hour} hour(s) ago"
        only_time = time_get.get_time(h=hour)
        text = text + (
            f"<b>{html.quote(f"price: {price}$")}</b>"
            f"\n"
            f"<b>{html.quote(time_string)}</b>"
            f"\n"
            f"<i>{html.quote(f"time: {only_time[1][1]}\ndate: {only_time[1][0]}\n")}</i>"
            f"\n\n"
        )
    text = text + (f"</blockquote>")

    #---------------------------------- выше этого коммента новая структура, потом полностью заменю старую но щас она еще нужна
        

    ns_time = time_get.ns_time
    ns_time_hour = time_get.ns_time_hour
    ns_time_day = time_get.ns_time_day

    current = time_get.current
    hour_ago = time_get.hour
    day_ago = time_get.day

    data = io_module.OneRequestStorage(
        coin_user,
        message.from_user.id,

        prices[0],
        current,
        ns_time,

        prices[1],
        hour_ago,
        ns_time_hour,

        prices[2],
        day_ago,
        ns_time_day

    )

    io_module.write_data(data)
    return text

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
        
