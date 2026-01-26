import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from google import genai  # Нова бібліотека

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8544620393:AAHj5jjvm-2dZAd04kZAKnq-1mn-E9HEbs0"
GEMINI_API_KEY = "AIzaSyCWDl5W2ejV5O9o-MAxCgHAJMDalb9VHnM"

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Новий клієнт Gemini
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-1.5-flash"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
ai_users = set()

# База знань (додай сюди всі свої розділи)
ANSWERS = {
    "Р1": "👤 Розділ 1: Вид декларації... https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/",
    "ПМ": "📒 1 ПМ (2025) = 3 028 грн."
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
    await message.answer("✅ Бот активований з новим ядром ШІ!", reply_markup=main_menu())

@dp.message(F.text == "🤖 Запитати ШІ")
async def ai_on(message: types.Message):
    ai_users.add(message.from_user.id)
    await message.answer("🤖 Режим ШІ увімкнено. Я використовую нову бібліотеку google-genai.", 
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
        status = await message.answer("⌛ ШІ опрацьовує ваш запит...")
        try:
            # Використання нового методу генерації
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=f"Ти асистент НАЗК. База: {KNOWLEDGE_BASE}. Питання: {message.text}"
            )
            await status.edit_text(response.text)
        except Exception as e:
            await status.edit_text(f"❌ Помилка: {str(e)[:100]}")
        return

    if message.text == "📊 ПМ":
        await message.answer(ANSWERS["ПМ"])

async def main():
    print("--- ЗАПУСК БОТА НА НОВОМУ ЯДРІ ---")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
