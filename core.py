from aiogram import types, html
import time
import requests
import time_module, io_module
eu_flag = "\U0001F1EA\U0001F1FA" #колхозный метод получения флага ес

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

def command_course(message: types.Message, coin: str) -> str:

    time_get = time_module.TimeGet()

    prices = get_price_inpast(coin, [0,1,24])
    price = prices[0]
    price_hour = prices[1]
    price_day = prices[2]

    change_h = round(price - price_hour, 4)
    change_d = round(price - price_day, 4) #округление цены до нормального вида

    change_h_str = f"+{change_h}" if change_h >= 0 else f"{change_h}"
    change_d_str = f"+{change_d}" if change_d >= 0 else f"{change_d}" #ставит плюс(или нет) к изменению цены, для внешнего вида

    coin_user = coin_formating(coin)  #коин в формате для пользователя

    coin_safe = html.quote(coin_user)
    price_safe = html.quote(str(price))
    price_hour_safe = html.quote(str(price_hour))
    price_day_safe = html.quote(str(price_day))
    change_h_safe = html.quote(change_h_str)
    change_d_safe = html.quote(change_d_str) #тут просто куоте всех переменных с припиской _safe

    ns_time = time_get.ns_time
    ns_time_hour = time_get.ns_time_hour
    ns_time_day = time_get.ns_time_day

    current = time_get.current
    hour_ago = time_get.hour
    day_ago = time_get.day

    data = io_module.OneRequestStorage(
        coin_user,
        message.from_user.id,

        price_safe,
        current,
        ns_time,

        price_hour_safe,
        hour_ago,
        ns_time_hour,

        price_day_safe,
        day_ago,
        ns_time_day

    )

    io_module.write_data(data)

    formatted_current_day = html.quote(str(current[0]))
    formatted_current_time = html.quote(str(current[1])) #тоже прост форматирование но теперь времени

    text = (
        f"Current {coin_safe} to USDT course{eu_flag}: \n"
        f"<b>{price_safe}$</b>\n"
        f"<i>day: {formatted_current_day}</i>\n"
        f"<i>time: {formatted_current_time}</i>\n\n"
        f"<blockquote>"
        f"Hour ago: \n"
        f" <b>{price_hour_safe}$</b>\n"
        f" Difference: {change_h_safe}$\n\n"
        f"Day ago: \n"
        f" <b>{price_day_safe}$</b>\n"
        f" Difference: {change_d_safe}$\n"
        f"</blockquote>"
    ) #сам текст, ничего сложного
    
    return text

def get_price_json(url, params):
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Data request error: {e}")
        return None

def get_price_inpast(coin: str, hours_ago: list):
    target_ms = [(time.time() - (h * 3600)) * 1000 for h in hours_ago]
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": "2"} #к параметрам прибавляется колво дней за которые надо скачать данные
    result = []
    
    data = get_price_json(url, params)
    if data == None:
        return [0,0,0]
    
    for ms in target_ms:
        closest_point = min(data["prices"], key=lambda x: abs(x[0] - ms)) #better call gemini
        price = round(closest_point[1], 2) #округление идет тут ну и ладно
        result.append(price)

    return result
        
