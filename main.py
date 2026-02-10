import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums import ParseMode

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8544620393:AAHj5jjvm-2dZAd04kZAKnq-1mn-E9HEbs0"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- ПОВНА БАЗА ЗНАНЬ ---
ANSWERS = {
    "Р1": "👤 **Розділ 1: Вид декларації**\n\nОбираємо «я продовжую виконувати функції держави...» та звітний період **2025 рік**.\n\n🔗 [Докладніше на Wiki НАЗК](https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/)",
    
    "Р2": "👥 **Розділ 2: Суб’єкт декларування**\n\n• Місце роботи: **Департамент поліції охорони**\n• Код ЄДРПОУ: **40109110**\n• Посада: вказуйте ту, яку займали станом на 31.12.2025.\n\n🔗 [Докладніше](https://wiki.nazk.gov.ua/category/deklaruvannya/ii-vidomosti-pro-sub-yekta-deklaruvannya/)",
    
    "Р2.1": "👨‍👩‍👧‍👦 **Розділ 2.1: Члени сім’ї**\n\nДружина/чоловік, діти до 18 років та всі, з ким спільно проживаєте понад 183 дні.\n\n🔗 [Докладніше](https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/)",
    
    "Р3": "🏠 **Розділ 3: Нерухомість**\n\nВласність, оренда, проживання. Обов'язково вкажіть об'єкт, де ви жили на кінець року.\n\n🔗 [Докладніше](https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/)",
    
    "Р6": "🚗 **Розділ 6: Транспорт**\n\nУсі авто (власні, дружини, оренда, техпаспорт).\n\n🔗 [Докладніше](https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/)",
    
    "Р11": "💰 **Розділ 11: Доходи**\n\nЗарплата (повна сума з податками), пенсія, допомога ВПО.\n\n🔗 [Докладніше](https://wiki.nazk.gov.ua/category/deklaruvannya/xiii-dohody-u-tomu-chysli-podarunky/)",
    
    "Р12.1": "💳 **Розділ 12.1: Рахунки**\n\nУсі рахунки IBAN, що були відкриті у 2025 році.\n\n🔗 [Докладніше](https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/)",

    "АВТОПЕРЕВІРКА": "🔍 **Автоперевірка:**\nФункція в кабінеті НАЗК, яка порівнює ваші дані з реєстрами перед подачею.\n🔗 [Як працює автоперевірка](https://wiki.nazk.gov.ua/category/deklaruvannya/avtoperevirka-deklaratsiyi/)"
}

# --- КЛАВІАТУРИ ---

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📅 Терміни подання"))
    builder.row(types.KeyboardButton(text="📞 Адмін"), types.KeyboardButton(text="⚖️ Відповідальність"))
    builder.row(types.KeyboardButton(text="📂 Розділи декларування"))
    builder.row(types.KeyboardButton(text="📝 Автозаповнення декларації"))
    builder.row(types.KeyboardButton(text="🔍 Автоперевірка своєї декларації"))
    return builder.as_markup(resize_keyboard=True)

def sections_menu():
    builder = ReplyKeyboardBuilder()
    btns = ["Розділ 1", "Розділ 2", "Розділ 2.1", "Розділ 3", "Розділ 4", "Розділ 5", 
            "Розділ 6", "Розділ 7-10", "Розділ 11", "Розділ 12", "Розділ 12.1", 
            "Розділ 13", "Розділ 14", "Розділ 15", "Розділ 16"]
    for b in btns:
        builder.add(types.KeyboardButton(text=b))
    builder.adjust(3)
    builder.row(types.KeyboardButton(text="⬅️ Назад"))
    return builder.as_markup(resize_keyboard=True)

# --- ОБРОБНИКИ ---

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ Назад")
async def start(message: types.Message):
    await message.answer("📋 **Головне меню**. Оберіть пункт:", reply_markup=main_menu(), parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "📞 Адмін")
async def contact(message: types.Message):
    await message.answer("👤 **Адміністратор Христина:**\n📞 +380932177380", parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "📅 Терміни подання")
async def terms(message: types.Message):
    await message.answer("📅 **Щорічна декларація за 2025 рік** подається до **31 березня 2026 року включно**.", parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "⚖️ Відповідальність")
async def resp(message: types.Message):
    await message.answer("⚖️ **Відповідальність:**\n\n• Адміністративна (штрафи)\n• Дисциплінарна (звільнення)\n• Кримінальна (за недостовірні дані)", parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "📂 Розділи декларування")
async def show_sections(message: types.Message):
    await message.answer("📝 Оберіть номер розділу:", reply_markup=sections_menu())

@dp.message(F.text == "📝 Автозаповнення декларації")
async def auto_fill(message: types.Message):
    # Пряме посилання на перегляд файлу
    link = "https://drive.google.com/file/d/1sYUYtHR34JD07oPRl-lFI_cWeKRXZyoO/view"
    await message.answer(
        f"📝 **Інструкція з автозаповнення:**\n\nСкопіюйте посилання та відкрийте у браузері:\n{link}",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False
    )

@dp.message(F.text == "🔍 Автоперевірка своєї декларації")
async def auto_check(message: types.Message):
    await message.answer(ANSWERS["АВТОПЕРЕВІРКА"], parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text.startswith("Розділ "))
async def handle_section(message: types.Message):
    key_map = {
        "Розділ 1": "Р1", "Розділ 2": "Р2", "Розділ 2.1": "Р2.1", "Розділ 3": "Р3",
        "Розділ 6": "Р6", "Розділ 11": "Р11", "Розділ 12.1": "Р12.1"
    }
    key = key_map.get(message.text)
    # Якщо тексту немає в мапінгу, даємо загальне посилання на базу знань
    text = ANSWERS.get(key, f"Детальна інформація по {message.text} доступна в [Базі знань НАЗК](https://wiki.nazk.gov.ua/category/deklaruvannya/)")
    await message.answer(text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
