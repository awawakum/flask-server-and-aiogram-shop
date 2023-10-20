from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from filters import IsAdmin
from loader import dp, db, bot
from states import NotifyState

@dp.message_handler(IsAdmin(), text='/notify')
async def notify_users(message: Message):
    await message.answer('Введите текст рассылки:')
    await NotifyState.text.set()

@dp.message_handler(IsAdmin() ,state=NotifyState.text)
async def notify_text(message:Message, state: FSMContext):

    users = db.fetchall('SELECT * FROM users')

    for user in users:
        await bot.send_message(user[1], message.text)

    await state.finish()



