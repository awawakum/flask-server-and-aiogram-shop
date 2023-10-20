import os
import handlers
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import config
from loader import dp, db, bot
import filters
import logging
from background import keep_alive  #импорт функции для поддержки работоспособности

filters.setup(dp)

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 8000))
user_message = 'Пользователь'
admin_message = 'Админ'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):

  user = db.fetchall(
      f'SELECT * FROM users WHERE telegram_id={message.chat.id}')
  if not user:
    db.query(
        f'INSERT INTO users (cid, telegram_id) VALUES (NULL, {message.chat.id})'
    )

  markup = ReplyKeyboardMarkup(resize_keyboard=True)

  if message.from_user.id in config.ADMINS:
    markup.row(user_message, admin_message)

  await message.answer('''Добро пожаловать! 
Я бот по продаже импортных напитков 🤖 
Мы предлагаем широкий выбор качественных и уникальных газировок из разных стран мира. Весь наш ассортимент отобран с особым вниманием к качеству и вкусу, чтобы вы могли наслаждаться настоящим гастрономическим путешествием. Берите у нас и наслаждайтесь! 🤗

🛒 Чтобы перейти в каталог и выбрать приглянувшиеся товары воспользуйтесь командой /menu.
    ''',
                       reply_markup=markup)


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
  await handlers.user.menu.user_menu(message)
  await message.answer('Включен пользовательский режим.')


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
  cid = message.chat.id
  if cid in config.ADMINS:
    await handlers.user.menu.admin_menu(message)
    await message.answer('Включен админский режим.')


async def on_startup(dp):
  logging.basicConfig(level=logging.INFO)
  db.create_tables()

  await bot.delete_webhook()
  await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown():
  logging.warning("Shutting down..")
  await bot.delete_webhook()
  await dp.storage.close()
  await dp.storage.wait_closed()
  logging.warning("Bot down")


keep_alive()
if __name__ == '__main__':

  if "HEROKU" in list(os.environ.keys()):

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

  else:

    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
