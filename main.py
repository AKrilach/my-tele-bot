import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# --- КОНФІГУРАЦІЯ ---
# Замініть цей токен на свій, якщо він зміниться
TELEGRAM_TOKEN = "8544620393:AAHj5jjvm-2dZAd04kZAKnq-1mn-E9HEbs0"

# Налаштування бота з підтримкою HTML за замовчуванням
bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# --- МАКСИМАЛЬНО РОЗШИРЕНА БАЗА ЗНАНЬ ---
ANSWERS = {
    "Р1": ("📋 <b>Розділ 1: Вид декларації</b>\n\n"
           "Обираємо тип «Щорічна». Звітний період — 2025 рік. "
           "Якщо ви подаєте декларацію вперше після призначення, обираєте 'Кандидата на посаду'. "
           "Якщо звільняєтесь — 'При звільненні'.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/'>Докладніше про види декларацій</a>"),

    "Р2": ("👤 <b>Розділ 2: Суб'єкт декларування</b>\n\n"
           "Це ваші дані. ПІБ, РНОКПП та <b>УНЗР</b> (13 цифр у вашій ID-картці або закордонному паспорті). "
           "Місце роботи: <b>Департамент поліції охорони</b>. Код ЄДРПОУ: <b>40109110</b>. "
           "Вказуйте посаду, яку обіймали станом на 31.12.2025.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ii-vidomosti-pro-sub-yekta-deklaruvannya/'>Докладніше про дані суб'єкта</a>"),

    "Р2.1": ("👥 <b>Розділ 2.1: Члени сім'ї</b>\n\n"
             "Сюди вписуємо: \n"
             "1. <b>Подружжя</b> (навіть якщо проживаєте окремо, але шлюб не розірвано).\n"
             "2. <b>Діти до 18 років</b> (навіть якщо проживають окремо).\n"
             "3. <b>Співмешканці</b> (цивільний шлюб, або спільне проживання > 183 дні).\n"
             "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/'>Докладніше про членів сім'ї</a>"),

    "Р3": ("🏠 <b>Розділ 3: Об'єкти нерухомості</b>\n\n"
           "Декларуємо майно <b>суб'єкта та ВСІХ членів сім'ї</b>. "
           "Обов'язково вказуйте об'єкт, де ви та сім'я були прописані або фактично проживали на 31.12.2025. "
           "Якщо житло не ваше — обирайте 'Інше право користування' або 'Оренда'.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/'>Докладніше про нерухомість</a>"),

    "Р4": ("🏗️ <b>Розділ 4: Об'єкти незавершеного будівництва</b>\n\n"
           "Сюди відносимо недобудовані будинки, а також нерухомість, яка вже збудована, але не прийнята в експлуатацію.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/'>Докладніше про недобудови</a>"),

    "Р6": ("🚗 <b>Розділ 6: Транспортні засоби</b>\n\n"
           "Вказуємо <b>ваші авто та авто сім'ї</b>. Навіть якщо ви користувалися машиною за довіреністю хоча б один день протягом року — її треба внести.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/'>Докладніше про транспорт</a>"),

    "Р11": ("💰 <b>Розділ 11: Доходи та подарунки</b>\n\n"
            "<b>Увага:</b> Вказуємо доходи ваші та УСІХ членів сім'ї. "
            "Зарплата (повна сума брутто), пенсія, допомога ВПО, відсотки по депозитах.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiii-dohody-u-tomu-chysli-podarunky/'>Докладніше про доходи</a>"),

    "Р12.1": ("💳 <b>Розділ 12.1: Рахунки в банках</b>\n\n"
              "Вказуємо всі номери IBAN (ваші та сім'ї), відкриті у звітному році. Навіть якщо на рахунку 0 грн.\n"
              "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>Докладніше про рахунки</a>"),
    
    "Р13": ("📉 <b>Розділ 13: Фінансові зобов’язання</b>\n\n"
            "Кредити, позики, ліміти по картках. Вказуємо тільки якщо залишок боргу на 31.12 перевищує 50 ПМ.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/'>Докладніше про кредити</a>")
}

# Дозаповнення порожніх розділів, щоб бот завжди відповідав
for i in range(1, 17):
    key = f"Р{i}"
    if key not in ANSWERS:
        ANSWERS[key] = f"ℹ️ <b>Розділ {i}</b>\n\nДетальна інструкція оновлюється. Будь ласка, зверніться до Wiki NAZK.\n🔗 <a href='https://wiki.nazk.gov.ua/'>Перейти до Wiki</a>"

# --- КЛАВІАТУРИ ---

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📅 Терміни подання"))
    builder.row(types.KeyboardButton(text="✍️ Автозаповнення"), 
                types.KeyboardButton(text="🔍 Автоперевірка"))
    builder.row(types.KeyboardButton(text="👤 Адмін"), 
                types.KeyboardButton(text="⚖️ Відповідальність"))
    builder.row(types.KeyboardButton(text="📂 Розділи декларування"))
    return builder.as_markup(resize_keyboard=True)

def sections_menu():
    builder = ReplyKeyboardBuilder()
    btns = ["Розділ 1", "Розділ 2", "Розділ 2.1", "Розділ 3", "Розділ 4", "Розділ 5", 
            "Розділ 6", "Розділ 7", "Розділ 8", "Розділ 9", "Розділ 10", "Розділ 11", 
            "Розділ 12", "Розділ 12.1", "Розділ 13", "Розділ 14", "Розділ 15", "Розділ 16"]
    for b in btns:
        builder.add(types.KeyboardButton(text=b))
    builder.adjust(3)
    builder.row(types.KeyboardButton(text="⬅️ Назад"))
    return builder.as_markup(resize_keyboard=True)

# --- ОБРОБНИКИ ---

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ Назад")
async def start(message: types.Message):
    await message.answer("📋 <b>Головне меню</b>. Оберіть пункт:", reply_markup=main_menu())

@dp.message(F.text == "📅 Терміни подання")
async def terms(message: types.Message):
    await message.answer("📅 <b>Щорічна декларація за 2025 рік</b> подається до <b>31 березня 2026 року включно</b>.")

@dp.message(F.text == "👤 Адмін")
async def contact(message: types.Message):
    await message.answer("👤 <b>Адміністратор Христина</b>\n📞 <code>0932177380</code>")

@dp.message(F.text == "⚖️ Відповідальність")
async def resp(message: types.Message):
    text = ("⚖️ <b>Відповідальність:</b>\n\n"
            "• <b>Адміністративна:</b> штрафи за помилки або несвоєчасність.\n"
            "• <b>Дисциплінарна:</b> звільнення з НПУ.\n"
            "• <b>Кримінальна:</b> за брехню в декларації на великі суми.")
    await message.answer(text)

@dp.message(F.text == "📂 Розділи декларування")
async def show_sections(message: types.Message):
    await message.answer("📝 Оберіть номер розділу для отримання детальної інструкції:", reply_markup=sections_menu())

@dp.message(F.text == "✍️ Автозаповнення")
async def auto_fill(message: types.Message):
    text = (
        "✍️ <b>Автозаповнення декларації</b>\n\n"
        "Ви можете скористатися файлом для спрощення процесу заповнення.\n"
        "Перейдіть за посиланням нижче:\n\n"
        "🔗 <a href='https://drive.google.com/file/d/1sYUYtHR34JD07oPRl-lFI_cWeKRXZyoO/view?usp=sharing'>Відкрити файл інструкції/шаблону</a>"
    )
    await message.answer(text, disable_web_page_preview=False)

@dp.message(F.text == "🔍 Автоперевірка")
async def auto_check(message: types.Message):
    text = (
        "<b>Автоперевірка своєї декларації</b>\n\n"
        "Шановний користувач!\n\n"
        "Скористайся «Автоперевіркою своєї декларації».\n\n"
        "1️⃣ Зайди за посиланням та авторизуйся: <a href='https://www.integrity-police.pp.ua/Perevirka-deklaratsiyi'>https://www.integrity-police.pp.ua/Perevirka-deklaratsiyi</a>\n"
        "📍 «Ваш підрозділ/орган – обирай <b>ДЕПАРТАМЕНТ ПОЛІЦІЇ ОХОРОНИ</b>»\n\n"
        "2️⃣ За посиланням <a href='https://public.nazk.gov.ua/'>https://public.nazk.gov.ua/</a> в пошуку заповни свої ПІБ, після чого скопіюй посилання на власну Декларацію.\n\n"
        "3️⃣ Встав його у поле перевірки попереднього ресурсу, далі натисни «Згенеруй Декларацію», після чого натисни на «Звіт по декларації».\n\n"
        "📊 В результаті буде сформований звіт Правильності поданої декларації з можливими помилками, які будуть виділені <b>червоним кольором</b>."
    )
    await message.answer(text, disable_web_page_preview=True)

@dp.message(F.text.startswith("Розділ "))
async def handle_section(message: types.Message):
    num = message.text.replace("Розділ ", "Р")
    if num in ANSWERS:
        await message.answer(ANSWERS[num], disable_web_page_preview=True)

# --- ЗАПУСК ---

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот зупинений!")
