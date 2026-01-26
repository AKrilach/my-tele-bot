import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8544620393:AAHj5jjvm-2dZAd04kZAKnq-1mn-E9HEbs0"
GEMINI_API_KEY = "AIzaSyCWDl5W2ejV5O9o-MAxCgHAJMDalb9VHnM"

# Налаштування Gemini з обробкою версії
genai.configure(api_key=GEMINI_API_KEY)
# Використовуємо flash модель (найшвидша для чат-ботів)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Список користувачів у режимі ШІ
ai_users = set()

# --- ПОВНА БАЗА ЗНАНЬ (Контекст для ШІ) ---
ANSWERS = {
    "Р1": "👤 Розділ 1: Вид декларації та звітний період. Обирати «я продовжую виконувати функції держави...» та 2025 рік. https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/",
    "Р2": "👥 Розділ 2: Члени сім’ї. Чоловік/дружина, діти до 18 років, особи при спільному проживанні 183+ дні. https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/",
    "Р2.1": "🪪 Розділ 2.1: Додаткова інформація. Код ЄДРПОУ: 40109110. Категорія: «НЕ ЗАСТОСОВУЄТЬСЯ». Номер ЄДДР з ID-картки.",
    "Р3": "🏠 Розділ 3: Об’єкти нерухомості. Власність, оренда, прописка (Інше право користування). https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/",
    "Р4": "🏗️ Розділ 4: Об’єкти незавершеного будівництва. https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/",
    "Р5": "💎 Розділ 5: Цінне рухоме майно (крім авто) > 100 ПМ. https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/",
    "Р6": "🚗 Розділ 6: Транспортні засоби (власні та в користуванні). https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/",
    "Р7": "📈 Розділ 7: Цінні папери. https://wiki.nazk.gov.ua/category/deklaruvannya/ih-tsinni-papery/",
    "Р8": "🏢 Розділ 8: Корпоративні права. Поліцейським заборонено! https://wiki.nazk.gov.ua/category/deklaruvannya/h-korporatyvni-prava/",
    "Р9": "👤 Розділ 9: Юридичні особи (бенефіціарство заборонено). https://wiki.nazk.gov.ua/category/deklaruvannya/hi-yurydychni-osoby-trasty-abo-inshi-podibni-pravovi-utvorennya-kintsevym-benefitsiarnym-vlasnykom-kontrolerom-yakyh-ye-sub-yekt-deklaruvannya-abo-chleny-jogo-sim-yi/",
    "Р10": "💡 Розділ 10: Нематеріальні активи. https://wiki.nazk.gov.ua/category/deklaruvannya/hii-nematerialni-aktyvy/",
    "Р11": "💰 Розділ 11: Доходи та подарунки. https://wiki.nazk.gov.ua/category/deklaruvannya/hiii-dohody-u-tomu-chysli-podarunky/",
    "Р12": "💵 Розділ 12: Грошові активи (готівка, банки). https://wiki.nazk.gov.ua/category/deklaruvannya/hiv-groshovi-aktyvy/",
    "Р13": "🏦 Розділ 13: Банківські рахунки (IBAN). https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/",
    "Р14": "📉 Розділ 14: Фінансові зобов’язання (кредити). https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/",
    "Р15": "🧾 Розділ 15: Видатки та правочини > 50 ПМ. https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/",
    "Р16": "⚠️ Розділ 16: Обмеження сумісництва. https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/",
    "ПМ": "📒 1 ПМ (2025) = 3 028 грн. 50 ПМ = 151 400 грн. 100 ПМ = 302 800 грн."
}

KNOWLEDGE_BASE_TEXT = "\n".join([f"{k}: {v}" for k, v in ANSWERS.items()])

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
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=f"Розділ {i}"))
    builder.add(types.KeyboardButton(text="Розділ 2.1"))
    builder.adjust(4)
    builder.row(types.KeyboardButton(text="⬅️ Назад"))
    return builder.as_markup(resize_keyboard=True)

# --- ОБРОБНИКИ ---

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ Бот-помічник Департаменту поліції охорони готовий до роботи!", reply_markup=main_menu())

@dp.message(F.text == "📝 Автозаповнення декларації")
async def auto_fill(message: types.Message):
    await message.answer(
        "📂 **Посилання на файл для автозаповнення:**\n\n"
        "🔗 [Відкрити Google Drive](https://drive.google.com/file/d/1sYUYtHR34JD07oPRl-lFI_cWeKRXZyoO/view?usp=sharing)",
        parse_mode="Markdown"
    )

@dp.message(F.text == "🤖 Запитати ШІ")
async def ai_mode(message: types.Message):
    ai_users.add(message.from_user.id)
    await message.answer("🤖 **Режим ШІ активовано.**\nЯ відповідаю на основі ваших розділів Р1-Р16. Що вас цікавить?\n\nДля виходу натисніть **⬅️ Назад**.", 
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="⬅️ Назад")]], resize_keyboard=True))

@dp.message(F.text == "⬅️ Назад")
async def go_back(message: types.Message):
    if message.from_user.id in ai_users:
        ai_users.remove(message.from_user.id)
    await message.answer("Повернення до меню:", reply_markup=main_menu())

@dp.message()
async def handle_all(message: types.Message):
    # Логіка ШІ
    if message.from_user.id in ai_users and message.text:
        msg = await message.answer("⌛️ *Запит до Gemini...*")
        try:
            full_prompt = (
                f"Ти — асистент з декларування НАЗК. База знань:\n{KNOWLEDGE_BASE_TEXT}\n\n"
                f"Питання користувача: {message.text}\n
