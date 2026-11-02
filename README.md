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

<blockquote>
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
</blockquote>
все крутится вокруг этого датакласса

<blockquote>
    df = pd.DataFrame(columns=[
        "price",
        "time",
        "date",
        "ns"
        ])
</blockquote>
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

заметки на будущее:
1. переделать command_course и все вот это разветвление на день - час - текущий момент. (возможно просто создать датакласс которым буду как из пулемета ебашить)
2. распилить command_course
3. большое обновление, уже после 1 и 2 ну и еще мб какой рефактор. добавить генерацию курса как фотку (перед этим pillow или чо там надо)