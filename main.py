import asyncio
import logging
import random
from aiogram import Bot, Dispatcher
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters.command import Command
from aiogram.types import Message
from database import Database

BOT_TOKEN = ""

CHAT_ID = ''

bot = Bot(token=BOT_TOKEN)

db = Database("users.db")

dp = Dispatcher()

EMOJI = [DiceEmoji.BOWLING, DiceEmoji.BASKETBALL, DiceEmoji.FOOTBALL, DiceEmoji.SLOT_MACHINE, DiceEmoji.DICE,
         DiceEmoji.DART]


async def start_handler(message: Message):
    if not db.is_exists(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.full_name)
        await message.answer(f"Hello {message.from_user.full_name}!")
    else:
        await message.answer("User already exists")


async def random_game(message: Message, bot: Bot):
    await bot.send_dice(chat_id=CHAT_ID, emoji=random.choice(EMOJI))


dp.message.register(start_handler, Command("start"))
dp.message.register(random_game, Command("game"))


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
