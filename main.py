import asyncio
import logging
import random
from aiogram import Bot, Dispatcher
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters.command import Command
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message, ChatMemberUpdated
from database import Database

BOT_TOKEN = "8017197747:AAGWgdKyPq56Opk_BenpgNursjwGwHmJn_k"
CHAT_ID = "-1002237491983"
dp = Dispatcher()
db = Database("users.db")
# emoji list
EMOJI = [
    DiceEmoji.BOWLING, DiceEmoji.BASKETBALL, DiceEmoji.FOOTBALL,
    DiceEmoji.SLOT_MACHINE, DiceEmoji.DICE, DiceEmoji.DART
]

logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    if not db.is_exists(user_id):
        db.add_user(user_id, full_name)
        await message.answer(f"Hello {full_name}!")
    else:
        await message.answer("User already exists")


@dp.message(Command("game"))
async def random_game(message: Message, bot: Bot):
    await bot.send_dice(chat_id=CHAT_ID, emoji=random.choice(EMOJI))


async def user_joined(update: ChatMemberUpdated, bot: Bot):
    if update.new_chat_member.status == ChatMemberStatus.MEMBER:
        user_id = update.new_chat_member.user.id
        full_name = update.new_chat_member.user.full_name
        if not db.is_exists(user_id):
            db.add_user(user_id, full_name)
            await bot.send_message(chat_id=update.chat.id,
                                   text=f"Xush kelibsiz, {update.from_user.full_name}! 🎉")  # noqa


dp.chat_member.register(user_joined)


async def main():
    """ Asosiy funksiya """  # noqa
    bot = Bot(token=BOT_TOKEN)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()  # bot sessiyasini to‘g‘ri yopish # noqa


if __name__ == "__main__":
    asyncio.run(main())
