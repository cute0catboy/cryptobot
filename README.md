CRYPTOBOT

итак, ты решил стать криптотрейдером

main.py(только действия бота):

базовые команды:
/start
/help

крипто стафф:
/btc
/eth
/ton
/story - скидывает хлсх файл со всеми твоими предыдущими запросами

команды с котами???
!cat

core.py(всякие бизнес функции):
coin_formating(coin: str) -> str: форматирует коин в подходящее для вывода имя
user_info(message: types.Message) -> str: пишет инфу о сообщении в бот, возвращает ее как стринг
def command_course(message: types.Message, coin: str) -> str: возвращает текст для команды о курсе валюты, кидает инфу для записи в io_module, достает все цены и тд короче пиздец нагруженный класс ч его потом распилю на части я скорее всего даже отдельный модуль сделаю
get_price_inpast(coin: str, time_offset: list) -> list: получает цену за прошлое, в списке указать сколько часов назад (0-47, там ток 2 дня грузится но 48 мб тоже я не проверял)
более полное описание в комментах в самом файле core.py
def get_price_json(url, params): просто возвращает данные о цене в формате джсон

time_module.py:
class TimeGet и там все эти значения временные для текущего времени час назад денб назад (потом переделаю под неопределенное время)

io_module.py
@dataclass
class OneRequestStorage:
    coin: str
    id: int

    price: str
    time: tuple
    ns_time: int

    price_hour: str
    time_hour: tuple
    ns_time_hour: int

    price_day: str
    time_day: tuple
    ns_time_day: int

все крутится вокруг этого датакласса

df = pd.DataFrame(columns=[
    "price",
    "time",
    "date",
    "ns"
    ])

и вокруг этого датафрейма, там легко разобраться

чтобы запустить своего бота нужно создать в папке .env файл и в нем написать
TOKEN=токен тг бота
OWNER_ID=ид аккаунта для логов

все айди крипты тут:

СПРАВОЧНИК ИДЕНТИФИКАТОРОВ (ids) ДЛЯ ЗАПРОСОВ К COINGECKO API
Передавайте эти значения в params={"ids": "ИДЕНТИФИКАТОР", ...}

--- МЕЙНСТРИМ / КРУПНЕЙШИЕ МОНЕТЫ ---
 "bitcoin"                   - Bitcoin (BTC)
 "ethereum"                  - Ethereum (ETH)
 "ripple"                    - Ripple (XRP)
 "solana"                    - Solana (SOL)
 "cardano"                   - Cardano (ADA)
 "polkadot"                  - Polkadot (DOT)
 "litecoin"                  - Litecoin (LTC)
 "chainlink"                 - Chainlink (LINK)

 --- ЭКОСИСТЕМА TON И TELEGRAM ---
 "the-open-network"          - Toncoin (TON)
 "notcoin"                   - Notcoin (NOT)
 "dogs-2"                    - Dogs (DOGS)

 --- БИРЖЕВЫЕ ТОКЕНЫ ---
 "binancecoin"               - BNB (Binance Coin)

 --- СТЕЙБЛКОИНЫ (Курс всегда ~1 USD) ---
 "tether"                    - Tether (USDT)
 "usd-coin"                  - USDC
 "first-digital-usd"         - FDUSD

 --- ПОПУЛЯРНЫЕ МЕМ-КОИНЫ ---
 "dogecoin"                  - Dogecoin (DOGE)
 "shiba-inu"                 - Shiba Inu (SHIB)
 "pepe"                      - Pepe (PEPE)
