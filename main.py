import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8544620393:AAHj5jjvm-2dZAd04kZAKnq-1mn-E9HEbs0"
GEMINI_API_KEY = "AIzaSyCWDl5W2ejV5O9o-MAxCgHAJMDalb9VHnM"

# Налаштування логування (щоб бачити помилки в консолі)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Налаштування Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Режим ШІ
ai_users = set()

# --- БАЗА ЗНАНЬ ---
ANSWERS = {
    "Р1": "👤 Розділ 1: Вид декларації... https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/",
    "Р2": "👥 Розділ 2: Члени сім’ї... https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/",
    "Р2.1": "🪪 Розділ 2.1: Додаткова інформація. Код ЄДРПОУ: 40109110. Категорія: «НЕ ЗАСТОСОВУЄТЬСЯ».",
    "Р3": "🏠 Розділ 3: Об’єкти нерухомості... https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/",
    "Р6": "🚗 Розділ 6: Транспортні засоби... https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/",
    "Р11": "💰 Розділ 11: Доходи та подарунки... https://wiki.nazk.gov.ua/category/deklaruvannya/hiii-dohody-u-tomu-chysli-podarunky/",
    "Р16": "⚠️ Розділ 16: Обмеження сумісництва... https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/",
    "ПМ": "📒 1 ПМ (2025) = 3 028 грн. 100 ПМ = 302 800 грн."
}
# Додайте інші розділи за аналогією (Р4, Р5, Р7-Р15)

KNOWLEDGE_BASE = "\n".join([f"{k}: {v}" for k, v in ANSWERS.items()])

# --- КЛАВІАТУРИ ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📅 Терміни"), types.KeyboardButton(text="📂 Розділи декларації"))
    builder.row(types.KeyboardButton(text="📊 Прожитковий мінімум"), types.KeyboardButton(text="🤖 Запитати ШІ"))
    builder.row(types.KeyboardButton(text="📝 Автозаповнення декларації"))
    builder.row(types.KeyboardButton(text="📞 Адмін"))
    return builder.as_markup(resize_keyboard=True)

def sections_menu():
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17): builder.add(types.KeyboardButton(text=f"Розділ {i}"))
    builder.add(types.KeyboardButton(text="Розділ 2.1"))
    builder.adjust(4)
    builder.row(types.KeyboardButton(text="⬅️ Назад"))
    return builder.as_markup(resize_keyboard=True)

# --- ОБРОБНИКИ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("✅ Бот активований!", reply_markup=main_menu())

@dp.message(F.text == "📝 Автозаповнення декларації")
async def auto_fill(message: types.Message):
    await message.answer("🔗 [Файл для автозаповнення](https://drive.google.com/file/d/1sYUYtHR34JD07oPRl-lFI_cWeKRXZyoO/view?usp=sharing)", parse_mode="Markdown")

@dp.message(F.text == "🤖 Запитати ШІ")
async def ai_on(message: types.Message):
    ai_users.add(message.from_user.id)
    await message.answer("🤖 Режим ШІ увімкнено. Чекаю на питання...", 
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="⬅️ Назад")]], resize_keyboard=True))

@dp.message(F.text == "⬅️ Назад")
async def go_back(message: types.Message):
    ai_users.discard(message.from_user.id)
    await message.answer("Головне меню:", reply_markup=main_menu())

@dp.message()
async def handle_msg(message: types.Message):
    if not message.text: return

    # Режим ШІ
    if message.from_user.id in ai_users:
        tmp = await message.answer("⌛ Думаю...")
        try:
            prompt = f"Ти асистент з декларацій. База знань:\n{KNOWLEDGE_BASE}\n\nПитання: {message.text}"
            response = model.generate_content(prompt)
            await tmp.edit_text(response.text)
        except Exception as e:
            await tmp.edit_text(f"❌ Помилка Gemini: {e}")
        return

    # Звичайні кнопки
    if message.text.startswith("Розділ "):
        key = message.text.replace("Розділ ", "Р")
        await message.answer(ANSWERS.get(key, "Інформація відсутня"))
    elif message.text == "📅 Терміни":
        await message.answer("Термін: 01.01.2026 - 31.03.2026")
    elif message.text == "📊 Прожитковий мінімум":
        await message.answer(ANSWERS["ПМ"])
    elif message.text == "📂 Розділи декларації":
        await message.answer("Оберіть розділ:", reply_markup=sections_menu())

# --- ЗАПУСК ТА ПЕРЕВІРКА ---
async def main():
    print("--- ПЕРЕВІРКА ПІДКЛЮЧЕННЯ ---")
    try:
        me = await bot.get_me()
        print(f"1. Telegram: OK (@{me.username})")
        # Тестовий запит до ШІ
        model.generate_content("test")
        print("2. Gemini API: OK")
    except Exception as e:
        print(f"ПОМИЛКА ПРИ ЗАПУСКУ: {e}")
        return

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

