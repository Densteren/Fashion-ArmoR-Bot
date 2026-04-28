import asyncio
from aiogram.filters import Command
from config import dp, bot, ADMIN_ID
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import ContentType, Message
from aiogram.exceptions import TelegramNetworkError

class BroadcastStates(StatesGroup):
    waiting_for_text = State()

@dp.message(Command("broadcast"))
async def start_broadcast(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_ID:
        await message.answer("У вас нет доступа к этой команде!")
        return

    await message.answer(
        "Напишите сообщение для рассылки. "
        "Вы можете использовать только форматирование HTML, "
        "а также прикрепить одно фото."
    )
    await state.set_state(BroadcastStates.waiting_for_text)

@dp.message(StateFilter(BroadcastStates.waiting_for_text))
async def broadcast_send(message: Message, state: FSMContext):
    global users

    if message.content_type == ContentType.TEXT:
        text = message.text
        photo = None
    elif message.content_type == ContentType.PHOTO:
        text = message.caption or ""
        photo = message.photo[-1].file_id  # берём лучшее качество
    else:
        await message.answer("Можно отправить только текст или фото")
        return

    if not users:
        await message.answer("Нет пользователей для рассылки!")
        await state.clear()
        return

    sent = 0
    failed = 0

    for user_id in users:
        try:
            if photo:
                await bot.send_photo(chat_id=user_id, photo=photo, caption=text, parse_mode="HTML")
            else:
                await bot.send_message(chat_id=user_id, text=text, parse_mode="HTML")
            await asyncio.sleep(0.1)
            sent += 1
        except TelegramNetworkError:
            await asyncio.sleep(2)
            failed += 1
        except Exception:
            failed += 1

    await message.answer(f"Рассылка завершена!\nОтправлено: {sent}\nНе удалось: {failed}")
    await state.clear()