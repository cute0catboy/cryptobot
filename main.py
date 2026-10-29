from aiogram import Bot, Dispatcher, types
import asyncio
import logging
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode
import config 
import core

dp = Dispatcher()
eu_flag = "\U0001F1EA\U0001F1FA"
owner_id = config.Owner_id

@dp.message(CommandStart())
async def command_start(message: types.Message):

    text = f"Hi, {markdown.hbold(message.from_user.username)}! /help to know more"
        
    await message.answer(
        text=text,
        parse_mode=ParseMode.HTML)

    log_text = core.user_info(message)

    await message.bot.send_message(chat_id=owner_id,
                                   text=log_text)

@dp.message(Command("help"))
async def command_help(message: types.Message):

    text = markdown.text(
        markdown.markdown_decoration.italic(markdown.markdown_decoration.quote(f"Crypto-helper(especially for euroteam{eu_flag}{eu_flag})")),
        markdown.markdown_decoration.quote("/btc to get bitcoin-usdt course"),
        markdown.markdown_decoration.quote("/eth to get ethereum-usdt course"),
        markdown.markdown_decoration.quote("/ton to get ton-usdt course"),
        sep="\n"
    )
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)

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