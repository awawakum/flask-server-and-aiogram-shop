from aiogram.types import Message, CallbackQuery
from loader import dp, bot

from filters import IsUser, IsAdmin


@dp.message_handler(IsUser() and IsAdmin(), text='👥 Контакты')
async def faq(message: Message):
    await message.answer('''
<b>Номер телефона:</b> +79619460616 
<b>ТГ:</b> @Zakaryan_V
<b>Комната:</b> 249
<b>Номер банковской карты:</b> 4584432823149274

<b>Перевести можно по Системе Быстрых Платежей на Альфа Банк по указанному выше номеру</b>''')