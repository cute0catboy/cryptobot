from aiogram import Bot, Dispatcher, types, html, F
import asyncio
import logging
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
import config 
import core

dp = Dispatcher()
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
        
    await message.answer(
        text=text,
        parse_mode=ParseMode.HTML)

    log_text = core.user_info(message)

    await message.bot.send_message(chat_id=owner_id,
                                   text=log_text)

@dp.message(Command("help", prefix="!%/")) #префикс потому что прикольно
async def command_help(message: types.Message):

    text = (
        f"<i>{html.quote(f"Crypto-helper(especially for euroteam{eu_flag})")}</i>\n"
        f"<blockquote>"
        f"{html.quote("/btc to get bitcoin-usdt course")}\n"
        f"{html.quote("/eth to get ethereum-usdt course")}\n"
        f"{html.quote("/ton to get ton-usdt course")}\n"
        f"</blockquote>"
    )
    await message.answer(text=text, parse_mode=ParseMode.HTML)

    log_text = core.user_info(message)

    await message.bot.send_message(chat_id=owner_id,
                                   text=log_text)

@dp.message(Command("ton"))
async def command_ton(message: types.Message):

    await message.reply(text="Wait up to 30 seconds...")

    text = core.command_course("the-open-network")

    await message.answer(text=text,
                         parse_mode=ParseMode.HTML)

    log_text = core.user_info(message)

    await message.bot.send_message(chat_id=owner_id,
                                   text=log_text)

@dp.message(Command("btc"))
async def command_ton(message: types.Message):

    await message.reply(text="Wait up to 30 seconds...")

    text = core.command_course("bitcoin")

    await message.answer(text=text,
                         parse_mode=ParseMode.HTML)

    log_text = core.user_info(message)

    await message.bot.send_message(chat_id=owner_id,
                                   text=log_text)

@dp.message(Command("eth"))
async def command_ton(message: types.Message):

    await message.reply(text="Wait up to 30 seconds...")

    text = core.command_course("ethereum")

    await message.answer(text=text,
                         parse_mode=ParseMode.HTML)

    log_text = core.user_info(message)

    await message.bot.send_message(chat_id=owner_id,
                                   text=log_text)

@dp.message(F.photo | F.video | F.document)
async def media_logging(message: types.Message): #просто потому что я могу и мне никто не запретит
    await message.bot.forward_message(chat_id=owner_id,
                                      from_chat_id=message.chat.id,
                                      message_id=message.message_id)
    
@dp.message()
async def echo(message: types.Message):
    log_text = core.user_info(message)

    await message.bot.send_message(chat_id=owner_id,
                                   text=log_text)

async def main():
    bot = Bot(token=config.Token)
    logging.basicConfig(level=logging.INFO) 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())