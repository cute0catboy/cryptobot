from aiogram import Bot, Dispatcher, types, html, F
import asyncio
import logging
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.enums import ParseMode, ChatAction
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InputMediaDocument, FSInputFile
import config, core, io_module
from pathlib import Path

DATA = Path(__file__).parent.resolve() / "data"

dp = Dispatcher()
up_arrow = "\u2B06\uFE0F"
eu_flag = "\U0001F1EA\U0001F1FA"
owner_id = config.Owner_id

@dp.message(CommandStart())
async def command_start(message: types.Message):

    text = (
        f"Hi, <b>{message.from_user.username}</b>!\n"
        f"<blockquote>"
        f"{html.quote("/help to know more")}"
        f"</blockquote>"
    )
        
    await message.reply(text=text)

    log_text = core.user_info(message)

    await message.bot.send_message(
        chat_id=owner_id,
        text=log_text
        )

@dp.message(Command("help"))
async def command_help(message: types.Message):

    text = (
        f"<i>{html.quote(f"Crypto-helper(especially for euroteam{eu_flag})")}</i>\n"
        f"<blockquote>"
        f"{html.quote("/btc to get bitcoin-usdt course")}\n"
        f"{html.quote("/eth to get ethereum-usdt course")}\n"
        f"{html.quote("/ton to get ton-usdt course")}\n"
        f"{html.quote("/story to get your requests story")}\n"
        f"</blockquote>"
    )
    await message.reply(text=text)

    log_text = core.user_info(message)

    await message.bot.send_message(
        chat_id=owner_id,
        text=log_text
        )

@dp.message(Command(commands=["eth", "btc", "ton"]))
async def command_eth(message: types.Message, command: CommandObject):

    await message.bot.send_chat_action(chat_id=message.chat.id,
                                       action=ChatAction.TYPING)

    coin = core.coin_formating(command.command, 1)
    text = core.command_course(message, coin, [0,1,24])
    await message.reply(text=text)

    log_text = core.user_info(message)
    await message.bot.send_message(
        chat_id=owner_id,
        text=log_text
        )

@dp.message(Command("story")) #потом добавлю формат истории типо в хлсх или текстом
async def command_story(message: types.Message):

    await message.bot.send_chat_action(chat_id=message.chat.id,
                                       action=ChatAction.TYPING)

    USER_DIR = DATA / f"user_{message.from_user.id}"
    if not USER_DIR.is_dir():
        await message.reply(
            text=html.quote("You have no history yet :(")
        )
        return

    files = [f for f in USER_DIR.iterdir() if f.is_file() and f.name.endswith("_DATA.xlsx")] #все нужные хлсх файлы из директории юзера
    files = io_module.parse(files) #меняет название и убирает наносекунды
    files = [FSInputFile(path=f, filename=f.name) for f in files] #превращает их в InputFile
    media = [InputMediaDocument(media=f) for f in files] #собирает медиа


    if len(media) < 2:
        await message.reply_document(document=files[0])
    else:
        await message.reply_media_group(
            media=media
        )

    await message.answer(
        text=html.quote(f"Your request history {up_arrow}")
    )

    log_text = core.user_info(message)
    await message.bot.send_message(
        chat_id=owner_id,
        text=log_text
        )

@dp.message(Command("cat", prefix="!")) #хэллоуинский апдейт я добавил кота
async def command_secret_cat(message: types.Message):
    url = "https://img.magnific.com/free-vector/flat-halloween-cat-illustration_23-2149067298.jpg?semt=ais_hybrid&w=740&q=80"
    await message.reply_photo(
        photo=url,
        caption=f"<b>{html.quote("Happy Halloween!!!")}</b>"
        )
    
    log_text = core.user_info(message)

    await message.bot.send_message(
        chat_id=owner_id,
        text=log_text
        )


    photo_cat = DATA / "97110_50709.jpg"
    await message.reply_photo(
        photo=types.FSInputFile(
            path = photo_cat
        )
        )
    
    log_text = core.user_info(message)

    await message.bot.send_message(
        chat_id=owner_id,
        text=log_text
        )

@dp.message(F.photo | F.video | F.document)
async def media_logging(message: types.Message): #просто потому что я могу и мне никто не запретит
    
    await message.bot.forward_message(
        chat_id=owner_id,
        from_chat_id=message.chat.id,
        message_id=message.message_id
        )
    
@dp.message()
async def echo(message: types.Message):
    log_text = core.user_info(message)

    await message.bot.send_message(
        chat_id=owner_id,
        text=log_text
        )

    if not message.text:
        await message.bot.forward_message(
            chat_id=owner_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id
            )

async def main():
    bot = Bot(
        token=config.Token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
    logging.basicConfig(level=logging.INFO) 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())