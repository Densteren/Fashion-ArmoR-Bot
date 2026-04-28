import asyncio
import time
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from storage.storage import save_users, load_users
from config import dp, bot
from images.images_url import START_PHOTO, LAUNCH_PHOTO, STAFF_PHOTO, PRODUCTION_PHOTO, COLLECTIONS_PHOTO, PACKS_PHOTO, EXCLUSIVE_PHOTO

RATE_LIMIT = 0.5
WARN_LIMIT = 3
WARN_TTL = 30 * 60
MUTE_TIME = 30 * 60
user_last_action = {}
user_warns = {}
user_mute_until = {}
NOT_WORK = True


def is_spam(user_id: int) -> tuple[bool, str | None]:
    now = time.time()

    mute_until = user_mute_until.get(user_id)
    if mute_until and now < mute_until:
        remaining = int((mute_until - now) / 60)
        return True, f"⛔ Вы в муте ещё {remaining} мин."

    last_time = user_last_action.get(user_id, 0)

    if now - last_time < RATE_LIMIT:
        warns, first_warn_time = user_warns.get(user_id, (0, now))

        if now - first_warn_time > WARN_TTL:
            warns = 0
            first_warn_time = now

        warns += 1
        user_warns[user_id] = (warns, first_warn_time)

        if warns >= WARN_LIMIT:
            user_mute_until[user_id] = now + MUTE_TIME
            user_warns.pop(user_id, None)
            return True, "🚫 Вы замучены на 30 минут за спам"

        return True, f"⚠️ Не спамьте! Предупреждение {warns}/{WARN_LIMIT}"

    user_last_action[user_id] = now
    return False, None

START_TEXT = ("<b><code>Приветствуем вас в магазине Fashion ArmoⓇ</code></b>\n\n&gt;<b> Чтобы запустить бота нажмите /launch</b>")

@dp.message(Command("start"))
async def start_handler(message: Message):
    spam, text = is_spam(message.from_user.id)
    if spam:
        if text:
            await message.answer(text)
        return
    
    if NOT_WORK:
        await message.answer(text="бот временно не работает :(")
    
    await message.answer_photo(photo=LAUNCH_PHOTO, caption=START_TEXT)
    users = load_users()
    if message.from_user.id not in users:
        users.add(message.from_user.id)
        save_users(users)


def start_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Наши сотрудники", callback_data="staff")
    kb.button(text="Наши продукты", callback_data="production")
    kb.adjust(1)
    return kb.as_markup()

def staff_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад", callback_data="back_start")
    kb.adjust(1)
    return kb.as_markup()

def production_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Коллекции", callback_data="collections")
    kb.button(text="Паки", callback_data="packs")
    kb.button(text="Эксклюзивы", callback_data="exclusive")
    kb.button(text="Назад", callback_data="back_start")
    kb.adjust(3,1)
    return kb.as_markup()

def collections_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="...", callback_data="1_collections")
    kb.button(text="Назад", callback_data="back_production")
    kb.adjust(1)
    return kb.as_markup()

def packs_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="...", callback_data="1_packs")
    kb.button(text="Назад", callback_data="back_production")
    kb.adjust(1)
    return kb.as_markup()

def exclusive_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="...", callback_data="1_exclusive")
    kb.button(text="Назад", callback_data="back_production")
    kb.adjust(1)
    return kb.as_markup()

def collections_produsts_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад", callback_data="back_collections")
    kb.adjust(1)
    return kb.as_markup()

def packs_products_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад", callback_data="back_packs")
    kb.adjust(1)
    return kb.as_markup()

def exclusive_products_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад", callback_data="back_exclusive")
    kb.adjust(1)
    return kb.as_markup()


LAUNCH_TEXT = ("<pre>Красивый и хороший текст</pre>")
STAFF_TEXT = ("<pre>Красивый и хороший текст</pre>")
PRODUCTION_TEXT = ("<pre>Красивый и хороший текст</pre>")
COLLECTIONS_TEXT = ("<pre>Красивый и хороший текст</pre>")
PACKS_TEXT = ("<pre>Красивый и хороший текст</pre>")
EXCLUSIVE_TEXT = ("<pre>Красивый и хороший текст</pre>")

SCREENS = {
    "1_collections": {
        "text": "<pre>Ничего не найдено</pre>",
        "photo": LAUNCH_PHOTO,
        "keyboard": collections_produsts_keyboard
    },
    "1_packs": {
        "text": "<pre>Ничего не найдено</pre>",
        "photo": LAUNCH_PHOTO,
        "keyboard": packs_products_keyboard
    },
    "1_exclusive": {
        "text": "<pre>Ничего не найдено</pre>",
        "photo": LAUNCH_PHOTO,
        "keyboard": exclusive_products_keyboard
    },
    "start": {
        "text": LAUNCH_TEXT,
        "photo": LAUNCH_PHOTO,
        "keyboard": start_keyboard
    },
    "staff": {
        "text": STAFF_TEXT,
        "photo": STAFF_PHOTO,
        "keyboard": staff_keyboard
    },
    "production": {
        "text": PRODUCTION_TEXT,
        "photo": LAUNCH_PHOTO,
        "keyboard": production_keyboard
    },
    "collections": {
        "text": COLLECTIONS_TEXT,
        "photo": LAUNCH_PHOTO,
        "keyboard": collections_keyboard
    },
    "packs": {
        "text": PACKS_TEXT,
        "photo": LAUNCH_PHOTO,
        "keyboard": packs_keyboard
    },
    "exclusive": {
        "text": EXCLUSIVE_TEXT,
        "photo": LAUNCH_PHOTO,
        "keyboard": exclusive_keyboard
    }
}


@dp.message(Command("launch"))
async def start_handler(message: Message):
    spam, text = is_spam(message.from_user.id)
    if spam:
        if text:
            await message.answer(text)
        return
    
    if NOT_WORK:
        await message.answer(text="бот временно не работает :(")
    else: 
        await message.answer_photo(photo=LAUNCH_PHOTO,
            caption=LAUNCH_TEXT,
            reply_markup=start_keyboard()
        )
    users = load_users()
    if message.from_user.id not in users:
        users.add(message.from_user.id)
        save_users(users)

@dp.callback_query()
async def universal_handler(call: CallbackQuery):
    spam, text = is_spam(call.from_user.id)
    if spam:
        await call.answer(text, show_alert=True)
        return
    
    if NOT_WORK:
        await call.answer(text="бот временно не работает :(")

    data = call.data
    if data.startswith("back_"):
        screen = data.replace("back_", "")
    else:
        screen = data

    if screen not in SCREENS:
        await call.answer("Неизвестное действие")
        return

    try:
        await call.message.delete()
    except:
        pass

    screen_data = SCREENS[screen]
    await call.message.answer_photo(
        photo=screen_data["photo"],
        caption=screen_data["text"],
        reply_markup=screen_data["keyboard"]()
    )

    users = load_users()
    if call.from_user.id not in users:
        users.add(call.from_user.id)
        save_users(users)

    await call.answer()


async def main():
    print("Bot started")
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())