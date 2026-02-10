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
    "Р1": "👤 **Розділ 1: Вид декларації та звітний період**\n\nУ розділі І «Вид декларації та звітний період» слід обрати позначку «я продовжую виконувати функції держави або органу місцевого самоврядування» та вибрати 2025 рік.\n\n🔗 **Докладніше:** https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/",
    
    "Р2": "👥 **Розділ 2: Суб’єкт декларування**\n\n• Місце роботи: **Департамент поліції охорони**.\n• Код ЄДРПОУ: **40109110**.\n• Ваші дані: ПІБ, РНОКПП та УНЗР (номер з ID-картки або закордонного паспорта).\n\n🔗 **Докладніше:** https://wiki.nazk.gov.ua/category/deklaruvannya/ii-vidomosti-pro-sub-yekta-deklaruvannya/",
    
    "Р2.1": "👨‍👩‍👧‍👦 **Розділ 2.1: Члени сім’ї**\n\nЧленами сім’ї є: подружжя, діти до 18 років, а також особи, які спільно проживають понад 183 дні на рік.\n\n🔗 **Докладніше:** https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/",
    
    "Р3": "🏠 **Розділ 3: Об’єкти нерухомості**\n\nВласність, оренда чи користування (наприклад, реєстрація місця проживання). Обов'язково вкажіть житло, де ви фактично проживали на 31.12.2025.\n\n🔗 **Докладніше:** https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/",
    
    "Р4": "💎 **Розділ 4: Цінне рухоме майно**\n\nМайно (крім авто) вартістю понад 100 ПМ (302 800 грн).\n\n🔗 **Докладніше:** https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/",
    
    "Р5": "🏗️ **Розділ 5: Об’єкти незавершеного будівництва**\n\n🔗 https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/",
    
    "Р6": "🚗 **Розділ 6: Транспортні засоби**\n\nВсі авто, що належать вам або членам сім'ї (власність, оренда, довіреність).\n\n🔗 **Докладніше:** https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/",
    
    "Р7": "📊 **Розділ 7-10: Цінні папери та активи**\n\nАкції, корпоративні права, криптовалюта, патенти.\n🔗 https://wiki.nazk.gov.ua/category/deklaruvannya/xii-nematerialni-aktyvy/",
    
    "Р11": "💰 **Розділ 11: Доходи, у тому числі подарунки**\n\nЗарплата (повна сума до вирахування податків), пенсія, соцвиплати, відсотки.\n\n🔗 **Докладніше:** https://wiki.nazk.gov.ua/category/deklaruvannya/xiii-dohody-u-tomu-chysli-podarunky/",
    
    "Р12": "💵 **Розділ 12: Грошові активи**\n\nГотівка та кошти на рахунках, якщо сукупно більше 50 ПМ.\n🔗 https://wiki.nazk.gov.ua/category/deklaruvannya/xiv-groshovi-aktyvy/",
    
    "Р12.1": "💳 **Розділ 12.1: Банківські рахунки**\n\nВказуються всі активні IBAN-рахунки суб'єкта та сім'ї.\n🔗 https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/",
    
    "Р13": "📉 **Розділ 13: Фінансові зобов’язання**\n\nКредити, позики (якщо борг > 50 ПМ).\n🔗 https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/",
    
    "Р14": "💸 **Розділ 14: Видатки та правочини**\n\nТільки разові видатки суб'єкта > 50 ПМ.\n🔗 https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/",
    
    "Р15": "👨‍🏫 **Розділ 15: Робота за сумісництвом**\n\nПоліцейським заборонено! (крім викладацької, наукової, творчої).\n🔗 https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/",
    
    "Р16": "🏛️ **Розділ 16: Членство в органах**\n\n🔗 https://wiki.nazk.gov.ua/category/deklaruvannya/xix-vhodzhennya-do-kerivnyh-revizijnyh-chy-naglyadovyh-organiv/",
    
    "АВТОПЕРЕВІРКА": "🔍 **Функція «Автоперевірка»:**\nДопомагає виявити помилки перед поданням декларації.\n🔗 https://wiki.nazk.gov.ua/category/deklaruvannya/avtoperevirka-deklaratsiyi/"
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
    final_btns = ["Розділ 1", "Розділ 2", "Розділ 2.1", "Розділ 3", "Розділ 4", "Розділ 5", 
                  "Розділ 6", "Розділ 7-10", "Розділ 11", "Розділ 12", "Розділ 12.1", 
                  "Розділ 13", "Розділ 14", "Розділ 15", "Розділ 16"]
    for b in final_btns:
        builder.add(types.KeyboardButton(text=b))
    builder.adjust(3)
    builder.row(types.KeyboardButton(text="⬅️ Назад"))
    return builder.as_markup(resize_keyboard=True)

# --- ОБРОБНИКИ ---

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ Назад")
async def start(message: types.Message):
    await message.answer("📋 **Головне меню**. Оберіть пункт:", reply_markup=main_menu(), parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "📅 Терміни подання")
async def terms(message: types.Message):
    await message.answer("📅 **Щорічна декларація за 2025 рік** подається до **31 березня 2026 року включно**.", parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "📞 Адмін")
async def contact(message: types.Message):
    await message.answer("👤 **Адміністратор Христина:**\n📞 +380932177380", parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "⚖️ Відповідальність")
async def resp(message: types.Message):
    await message.answer("⚖️ **Відповідальність:**\n\n• Адміністративна (штрафи).\n• Дисциплінарна (звільнення).\n• Кримінальна (за недостовірні дані).", parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "📂 Розділи декларування")
async def show_sections(message: types.Message):
    await message.answer("📝 Оберіть номер розділу:", reply_markup=sections_menu())

@dp.message(F.text == "📝 Автозаповнення декларації")
async def auto_fill(message: types.Message):
    await message.answer(
        "📝 **Файл для автозаповнення:**\n🔗 https://drive.google.com/file/d/1sYUYtHR34JD07oPRl-lFI_cWeKRXZyoO/view?usp=sharing",
        parse_mode=ParseMode.MARKDOWN
    )

@dp.message(F.text == "🔍 Автоперевірка своєї декларації")
async def auto_check(message: types.Message):
    await message.answer(ANSWERS["АВТОПЕРЕВІРКА"], parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text.startswith("Розділ "))
async def handle_section(message: types.Message):
    key_map = {
        "Розділ 1": "Р1", "Розділ 2": "Р2", "Розділ 2.1": "Р2.1", "Розділ 3": "Р3",
        "Розділ 4": "Р4", "Розділ 5": "Р5", "Розділ 6": "Р6", "Розділ 7-10": "Р7",
        "Розділ 11": "Р11", "Розділ 12": "Р12", "Розділ 12.1": "Р12.1", "Розділ 13": "Р13",
        "Розділ 14": "Р14", "Розділ 15": "Р15", "Розділ 16": "Р16"
    }
    key = key_map.get(message.text)
    if key:
        await message.answer(ANSWERS[key], parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
