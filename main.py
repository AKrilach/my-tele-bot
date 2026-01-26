import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8544620393:AAHj5jjvm-2dZAd04kZAKnq-1mn-E9HEbs0"
GEMINI_API_KEY = "AIzaSyCWDl5W2ejV5O9o-MAxCgHAJMDalb9VHnM"

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Явне налаштування Google AI
genai.configure(api_key=GEMINI_API_KEY)

# Створюємо модель з явним зазначенням версії
# Використовуємо 'gemini-1.5-flash', але через стабільний метод
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash'
)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
ai_users = set()

# --- БАЗА ЗНАНЬ (Тільки основне для тесту) ---
ANSWERS = {
    "Р1": "👤 Розділ 1: Вид декларації... https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/",
    "ПМ": "📒 1 ПМ (2025) = 3 028 грн.",
}

KNOWLEDGE_BASE = "\n".join([f"{k}: {v}" for k, v in ANSWERS.items()])

# --- КЛАВІАТУРИ ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📅 Терміни"), types.KeyboardButton(text="📂 Розділи"))
    builder.row(types.KeyboardButton(text="📊 ПМ"), types.KeyboardButton(text="🤖 Запитати ШІ"))
    builder.row(types.KeyboardButton(text="📝 Автозаповнення"))
    return builder.as_markup(resize_keyboard=True)

# --- ОБРОБНИКИ ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ Бот запущений. Оберіть дію:", reply_markup=main_menu())

@dp.message(F.text == "🤖 Запитати ШІ")
async def ai_on(message: types.Message):
    ai_users.add(message.from_user.id)
    await message.answer("🤖 Режим ШІ активовано. Напишіть питання (або натисніть 'Назад')", 
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="⬅️ Назад")]], resize_keyboard=True))

@dp.message(F.text == "⬅️ Назад")
async def go_back(message: types.Message):
    ai_users.discard(message.from_user.id)
    await message.answer("Меню:", reply_markup=main_menu())

@dp.message(F.text == "📝 Автозаповнення")
async def auto_fill(message: types.Message):
    await message.answer("🔗 [Посилання на файл](https://drive.google.com/file/d/1sYUYtHR34JD07oPRl-lFI_cWeKRXZyoO/view?usp=sharing)")

@dp.message()
async def handle_msg(message: types.Message):
    if not message.text: return
    
    if message.from_user.id in ai_users:
        status = await message.answer("⌛ Опрацьовую...")
        try:
            # Використовуємо спрощений виклик
            response = await asyncio.to_thread(model.generate_content, f"Ти асистент НАЗК. База: {KNOWLEDGE_BASE}. Питання: {message.text}")
            await status.edit_text(response.text)
        except Exception as e:
            await status.edit_text(f"❌ Помилка API: Оновіть бібліотеки в requirements.txt. ({str(e)[:50]})")
        return

    if message.text == "📅 Терміни":
        await message.answer("Термін: 01.01.2026 - 31.03.2026")
    elif message.text == "📊 ПМ":
        await message.answer(ANSWERS["ПМ"])

async def main():
    print("--- ПЕРЕВІРКА ЗАПУСКУ ---")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
