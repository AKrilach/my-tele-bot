import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8544620393:AAHj5jjvm-2dZAd04kZAKnq-1mn-E9HEbs0"
GEMINI_API_KEY = "AIzaSyCWDl5W2ejV5O9o-MAxCgHAJMDalb9VHnM"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

ai_users = set()

# --- ПОВНА БАЗА ЗНАНЬ ---
ANSWERS = {
    "Р1": "👤 Розділ 1: Вид декларації та звітний період. Обирати «я продовжую виконувати функції держави...» та 2025 рік. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/",
    "Р2": "👥 Розділ 2: Члени сім’ї. Чоловік/дружина, неповнолітні діти, та особи, що спільно проживають понад 183 дні. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/",
    "Р2.1": "🪪 Розділ 2.1: Додаткова інформація. Код ЄДРПОУ: 40109110 (ОБОВ’ЯЗКОВО). Категорія: «НЕ ЗАСТОСОВУЄТЬСЯ».",
    "Р3": "🏠 Розділ 3: Об’єкти нерухомості. Власність, оренда або право користування. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/",
    "Р4": "🏗️ Розділ 4: Об’єкти незавершеного будівництва. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/",
    "Р5": "💎 Розділ 5: Цінне рухоме майно. Понад 100 ПМ. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/",
    "Р6": "🚗 Розділ 6: Транспортні засоби. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/",
    "Р7": "📈 Розділ 7: Цінні папери. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/ih-tsinni-papery/",
    "Р8": "🏢 Розділ 8: Корпоративні права. Поліцейським заборонено мати корпоративні права. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/h-korporatyvni-prava/",
    "Р9": "👤 Розділ 9: Юридичні особи. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/hi-yurydychni-osoby-trasty-abo-inshi-podibni-pravovi-utvorennya-kintsevym-benefitsiarnym-vlasnykom-kontrolerom-yakyh-ye-sub-yekt-deklaruvannya-abo-chleny-jogo-sim-yi/",
    "Р10": "💡 Розділ 10: Нематеріальні активи. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/hii-nematerialni-aktyvy/",
    "Р11": "💰 Розділ 11: Доходи та подарунки. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/hiii-dohody-u-tomu-chysli-podarunky/",
    "Р12": "💵 Розділ 12: Грошові активи. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/hiv-groshovi-aktyvy/",
    "Р13": "🏦 Розділ 13: Банківські рахунки. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/",
    "Р14": "📉 Розділ 14: Фінансові зобов’язання. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/",
    "Р15": "🧾 Розділ 15: Видатки та правочини. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/",
    "Р16": "⚠️ Розділ 16: Обмеження для поліцейських. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/",
    "ПМ": "📒 Показники 2025: 1 ПМ = 3 028 грн. 50 ПМ = 151 400 грн. 100 ПМ = 302 800 грн. Посилання: https://wiki.nazk.gov.ua/category/deklaruvannya/preambula/"
}

KNOWLEDGE_BASE_TEXT = "\n".join([f"{k}: {v}" for k, v in ANSWERS.items()])

# --- КЛАВІАТУРИ ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📅 Терміни"), types.KeyboardButton(text="📂 Розділи декларації"))
    builder.row(types.KeyboardButton(text="📊 Прожитковий мінімум"), types.KeyboardButton(text="🤖 Запитати ШІ"))
    # НОВА КНОПКА
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
    await message.answer("✅ Вітаю! Я бот-помічник Департаменту поліції охорони.\nОберіть потрібний пункт меню:", reply_markup=main_menu())

@dp.message(F.text == "📝 Автозаповнення декларації")
async def auto_fill(message: types.Message):
    await message.answer(
        "📂 **Інструкція з автозаповнення декларації:**\n\n"
        "Ви можете завантажити необхідний файл за посиланням нижче:\n"
        "🔗 [Завантажити файл](https://drive.google.com/file/d/1sYUYtHR34JD07oPRl-lFI_cWeKRXZyoO/view?usp=sharing)",
        disable_web_page_preview=False,
        parse_mode="Markdown"
    )

@dp.message(F.text == "🤖 Запитати ШІ")
async def ai_mode(message: types.Message):
    ai_users.add(message.from_user.id)
    await message.answer("🤖 **Режим ШІ активовано.**\nЗапитуйте що завгодно! Для виходу натисніть **⬅️ Назад**.", 
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="⬅️ Назад")]], resize_keyboard=True))

@dp.message(F.text == "📅 Терміни")
async def terms(message: types.Message):
    await message.answer("📅 **Термін подачі щорічної декларації за 2025 рік:**\nЗ 1 січня по 31 березня 2026 року.")

@dp.message(F.text == "📂 Розділи декларації")
async def show_sections(message: types.Message):
    await message.answer("📝 Оберіть номер розділу:", reply_markup=sections_menu())

@dp.message(F.text == "📊 Прожитковий мінімум")
async def show_pm(message: types.Message):
    await message.answer(ANSWERS["ПМ"])

@dp.message(F.text == "📞 Адмін")
async def contact(message: types.Message):
    await message.answer("👤 **Адміністратор Христина:**\n📞 +380932177380")

@dp.message(F.text == "⬅️ Назад")
async def go_back(message: types.Message):
    if message.from_user.id in ai_users:
        ai_users.remove(message.from_user.id)
    await message.answer("Головне меню:", reply_markup=main_menu())

@dp.message()
async def handle_all(message: types.Message):
    if message.from_user.id in ai_users and message.text:
        msg = await message.answer("⌛️ *Думаю...*")
        try:
            full_prompt = (
                f"Ти — асистент з декларування для поліцейських. Твоя база знань:\n{KNOWLEDGE_BASE_TEXT}\n\n"
                f"Питання: {message.text}\n"
                f"Відповідай коротко, використовуючи ці дані."
            )
            response = model.generate_content(full_prompt)
            await msg.edit_text(response.text)
        except Exception as e:
            await msg.edit_text(f"Помилка ШІ: {e}")
        return

    if message.text.startswith("Розділ "):
        key = message.text.replace("Розділ ", "Р")
        if key in ANSWERS:
            await message.answer(ANSWERS[key])

# --- ЗАПУСК ---
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
