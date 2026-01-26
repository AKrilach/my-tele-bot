import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8544620393:AAHj5jjvm-2dZAd04kZAKnq-1mn-E9HEbs0"
GEMINI_API_KEY = "AIzaSyCWDl5W2ejV5O9o-MAxCgHAJMDalb9VHnM"

# Налаштування Gemini (використовуємо стабільний промпт)
genai.configure(api_key=GEMINI_API_KEY)
# Змінюємо модель на gemini-pro для кращої сумісності зі старими бібліотеками
model = genai.GenerativeModel('gemini-pro')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

ai_users = set()

# --- БАЗА ЗНАНЬ ---
ANSWERS = {
    "Р1": "👤 Розділ 1: Вид декларації та звітний період. Обирати 2025 рік. https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/",
    "Р2.1": "🪪 Розділ 2.1: Додаткова інформація. Код ЄДРПОУ: 40109110. Категорія: «НЕ ЗАСТОСОВУЄТЬСЯ».",
    "ПМ": "📒 1 ПМ (2025) = 3 028 грн. 100 ПМ = 302 800 грн.",
    # Додайте інші розділи сюди...
}

KNOWLEDGE_BASE = "\n".join([f"{k}: {v}" for k, v in ANSWERS.items()])

# --- КЛАВІАТУРИ ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📅 Терміни"), types.KeyboardButton(text="📂 Розділи декларації"))
    builder.row(types.KeyboardButton(text="📊 Прожитковий мінімум"), types.KeyboardButton(text="🤖 Запитати ШІ"))
    builder.row(types.KeyboardButton(text="📝 Автозаповнення декларації"))
    builder.row(types.KeyboardButton(text="📞 Адмін"))
    return builder.as_markup(resize_keyboard=True)

# --- ОБРОБНИКИ ---

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ Бот активний і готовий допомагати!", reply_markup=main_menu())

@dp.message(F.text == "📝 Автозаповнення декларації")
async def auto_fill(message: types.Message):
    await message.answer("🔗 [Файл для автозаповнення](https://drive.google.com/file/d/1sYUYtHR34JD07oPRl-lFI_cWeKRXZyoO/view?usp=sharing)", parse_mode="Markdown")

@dp.message(F.text == "🤖 Запитати ШІ")
async def ai_on(message: types.Message):
    ai_users.add(message.from_user.id)
    await message.answer("🤖 Режим ШІ увімкнено. Напишіть ваше питання...", 
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="⬅️ Назад")]], resize_keyboard=True))

@dp.message(F.text == "⬅️ Назад")
async def go_back(message: types.Message):
    ai_users.discard(message.from_user.id)
    await message.answer("Головне меню:", reply_markup=main_menu())

@dp.message()
async def handle_msg(message: types.Message):
    if not message.text: return

    if message.from_user.id in ai_users:
        status = await message.answer("⌛ Опрацьовую запит...")
        try:
            prompt = f"Ти асистент з декларацій. База знань:\n{KNOWLEDGE_BASE}\n\nПитання: {message.text}"
            # Використовуємо спрощений виклик для старих версій бібліотеки
            response = model.generate_content(prompt)
            await status.edit_text(response.text)
        except Exception as e:
            await status.edit_text(f"❌ Помилка: {str(e)[:100]}")
        return

    if message.text == "📊 Прожитковий мінімум":
        await message.answer(ANSWERS["ПМ"])
    elif message.text == "📅 Терміни":
        await message.answer("Термін: 01.01.2026 - 31.03.2026")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("--- ЗАПУСК БОТА ---")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
