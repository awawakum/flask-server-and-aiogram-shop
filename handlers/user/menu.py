
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from loader import dp
from filters import IsAdmin, IsUser

catalog = '🛍️ Каталог'
settings = '⚙️ Настройка каталога'
questions = '❓ Вопросы'
FAQ = '👥 Контакты'
askquestion = '❓ Обратная связь'

@dp.message_handler(IsAdmin(), commands='menu')
async def admin_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(settings)
    markup.add(questions)

    await message.answer('Меню', reply_markup=markup)

@dp.message_handler(IsUser(), commands='menu')
async def user_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(catalog)
    markup.add(FAQ)
    markup.add(askquestion)

    await message.answer('Меню', reply_markup=markup)
