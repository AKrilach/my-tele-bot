import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8544620393:AAHj5jjvm-2dZAd04kZAKnq-1mn-E9HEbs0"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- ПОВНА БАЗА ЗНАНЬ ---
ANSWERS = {
    "Р1": ("📋 <b>Розділ 1: Вид декларації</b>\n\n"
           "Оберіть тип «Щорічна» та звітний період «2025 рік».\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/'>Інструкція НАЗК</a>"),

    "Р2": ("👤 <b>Розділ 2: Суб'єкт декларування</b>\n\n"
           "Ваші дані: ПІБ, РНОКПП, УНЗР. Код ЄДРПОУ Департаменту поліції охорони: <b>40109110</b>.\n"
           "⚠️ <b>ВАЖЛИВО:</b> У полі 'Категорія посади' обов'язково обирайте — <b>НЕ ЗАСТОСОВУЄТЬСЯ</b>.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ii-vidomosti-pro-sub-yekta-deklaruvannya/'>Інструкція НАЗК</a>"),

    "Р2.1": ("👥 <b>Розділ 2.1: Члени сім'ї</b>\n\n"
             "Вказуємо подружжя, дітей до 18 років та осіб, що спільно проживали > 183 дні.\n"
             "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/'>Інструкція НАЗК</a>"),

    "Р3": ("🏠 <b>Розділ 3: Нерухомість</b>\n\n"
           "⚠️ <b>Вказуємо майно суб'єкта ТА сім'ї.</b> Власність, оренда, право користування (прописка).\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/'>Інструкція НАЗК</a>"),

    "Р4": ("🏗️ <b>Розділ 4: Незавершене будівництво</b>\n\n"
           "Об'єкти, не прийняті в експлуатацію. Включаємо майно сім'ї.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/'>Інструкція НАЗК</a>"),

    "Р5": ("💎 <b>Розділ 5: Цінне майно</b>\n\n"
           "Речі дорожче 100 ПМ (крім авто).\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/'>Інструкція НАЗК</a>"),

    "Р6": ("🚗 <b>Розділ 6: Транспортні засоби</b>\n\n"
           "⚠️ <b>Ваші авто та авто сім'ї.</b> Власність, техпаспорт, довіреність.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/'>Інструкція НАЗК</a>"),

    "Р7": ("📈 <b>Розділ 7: Цінні папери</b>\n\n"
           "Акції, облігації ваші та сім'ї.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ih-tsinni-papery/'>Інструкція НАЗК</a>"),

    "Р8": ("🏢 <b>Розділ 8: Корпоративні права</b>\n\n"
           "⚠️ <b>ДЛЯ ПОЛІЦЕЙСЬКИХ:</b> Заборонено мати частки в прибуткових фірмах (ст. 25 Закону). Права мали бути передані в управління. Члени сім'ї вказують бізнес без обмежень.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/h-korporatyvni-prava/'>Інструкція НАЗК</a>"),

    "Р9": ("🏢 <b>Розділ 9: Бенефіціарна власність</b>\n\n"
           "Контроль над фірмами через посередників.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hi-yurydychni-osoby-trasty-abo-inshi-podibni-pravovi-utvorennya-kintsevym-benefitsiarnym-vlasnykom-kontrolerom-yakyh-ye-sub-yekt-deklaruvannya-abo-chleny-jogo-sim-yi/'>Інструкція НАЗК</a>"),

    "Р10": ("💡 <b>Розділ 10: Нематеріальні активи</b>\n\n"
            "🟡 <b>Криптовалюти:</b> Назва, кількість, дата, біржа/гаманець. Також авторські права.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hii-nematerialni-aktyvy/'>Інструкція НАЗК</a>"),

    "Р11": ("💰 <b>Розділ 11: Доходи та подарунки</b>\n\n"
            "⚠️ <b>Обов'язково доходи УСІЄЇ СІМ'Ї.</b> Зарплата (брутто), пенсія, допомога ВПО.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiii-dohody-u-tomu-chysli-podarunky/'>Інструкція НАЗК</a>"),

    "Р12": ("💵 <b>Розділ 12: Грошові активи</b>\n\n"
            "Готівка та картки ваші + сім'ї, якщо сукупно > 50 ПМ.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiv-groshovi-aktyvy/'>Інструкція НАЗК</a>"),

    "Р12.1": ("💳 <b>Розділ 12.1: Банківські установи</b>\n\n"
              "⚠️ <b>ТІЛЬКИ НАЗВИ БАНКІВ:</b> Обираємо зі списку банки (Приват, Ощад тощо), де відкрито рахунки у вас або сім'ї. IBAN писати не треба.\n"
              "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>Інструкція НАЗК</a>"),

    "Р13": ("📉 <b>Розділ 13: Фінансові зобов’язання</b>\n\n"
            "Кредити, борги по лімітах ваші та сім'ї.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/'>Інструкція НАЗК</a>"),

    "Р14": ("🧾 <b>Розділ 14: Видатки та правочини</b>\n\n"
            "Разові витрати СУБ'ЄКТА понад 50 ПМ за чек.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/'>Інструкція НАЗК</a>"),

    "Р15": ("⚠️ <b>Розділ 15: Сумісництво</b>\n\n"
            "Дозволено лише викладання, науку, творчість, медицину.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/'>Інструкція НАЗК</a>"),

    "Р16": ("🏛️ <b>Розділ 16: Організації</b>\n\n"
            "Керівні органи ГО, фондів ваші або сім'ї.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xix-vhodzhennya-do-kerivnyh-revizijnyh-chy-naglyadovyh-organiv/'>Інструкція НАЗК</a>")
}

# --- КЛАВІАТУРИ ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📅 Терміни подання"))
    builder.row(types.KeyboardButton(text="🤖 Автозаповнення декларації"))
    builder.row(types.KeyboardButton(text="🔍 Автоперевірка своєї декларації"))
    builder.row(types.KeyboardButton(text="📂 Розділи декларування"))
    builder.row(types.KeyboardButton(text="⚖️ Відповідальність"), types.KeyboardButton(text="👤 Адміністратор"))
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
    await message.answer("📋 <b>Головне меню</b>. Оберіть пункт:", reply_markup=main_menu(), parse_mode="HTML")

@dp.message(F.text == "🤖 Автозаповнення декларації")
async def auto_fill(message: types.Message):
    await message.answer("🔗 <b>Посилання на файл автозаповнення:</b>\nhttps://drive.google.com/file/d/1sYUYtHR34JD07oPRl-lFI_cWeKRXZyoO/view?usp=sharing", parse_mode="HTML")

@dp.message(F.text == "🔍 Автоперевірка своєї декларації")
async def auto_check(message: types.Message):
    text = (
        "🔍 <b>Автоперевірка своєї декларації</b>\n\n"
        "Шановний користувач! \n\n"
        "Скористайся «Автоперевіркою своєї декларації».\n\n"
        "1️⃣ Зайди за посиланням та авторизуйся:\n"
        "https://www.integrity-police.pp.ua/Perevirka-deklaratsiyi\n"
        "📍 «Ваш підрозділ/орган – обирай <b>ДЕПАРТАМЕНТ ПОЛІЦІЇ ОХОРОНИ</b>»\n\n"
        "2️⃣ За посиланням https://public.nazk.gov.ua/ в пошуку заповни свої ПІБ, після чого скопіюй посилання на власну Декларацію.\n\n"
        "3️⃣ Встав його у поле перевірки попереднього ресурсу, далі натисни «Згенеруй Декларацію», після чого натисни на «Звіт по декларації».\n\n"
        "📊 В результаті буде сформований звіт Правильності поданої декларації з можливими помилками, які будуть виділені <b>червоним кольором</b>."
    )
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

@dp.message(F.text == "📂 Розділи декларування")
async def show_sections(message: types.Message):
    await message.answer("📝 Оберіть номер розділу:", reply_markup=sections_menu(), parse_mode="HTML")

@dp.message(F.text.startswith("Розділ "))
async def handle_section(message: types.Message):
    num = message.text.replace("Розділ ", "Р")
    if num in ANSWERS:
        await message.answer(ANSWERS[num], parse_mode="HTML", disable_web_page_preview=True)

@dp.message(F.text == "📅 Терміни подання")
async def terms(message: types.Message):
    await message.answer("📅 <b>Щорічна декларація за 2025 рік</b> подається до 31 березня 2026 року включно.", parse_mode="HTML")

@dp.message(F.text == "👤 Адміністратор")
async def contact(message: types.Message):
    await message.answer("👤 <b>Адміністратор Христина</b>\n📞 <code>0932177380</code>", parse_mode="HTML")

@dp.message(F.text == "⚖️ Відповідальність")
async def resp(message: types.Message):
    text = (
        "⚖️ <b>Відповідальність за завідомо недостовірні відомості в декларації:</b>\n\n"
        "🔸 <b>Кримінальна:</b> понад 750 ПМ* (понад 2 271 000 грн у 2025 році; понад 2 496 000 грн у 2026 році).\n\n"
        "🔸 <b>Адміністративна:</b> від 150 до 750 ПМ* (від 454 200 грн до 2 271 000 грн у 2025 році; від 499 200 грн до 2 496 000 грн у 2026 році).\n\n"
        "🔸 <b>Дисциплінарна (догана, сувора догана, звільнення тощо):</b> до 150 ПМ* (до 454 200 грн у 2025 році; до 499 200 грн у 2026 році).\n\n"
        "<i>* 1 ПМ у 2025 році = 3028 грн</i>\n"
        "<i>  1 ПМ у 2026 році = 3328 грн</i>"
    )
    await message.answer(text, parse_mode="HTML")

async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
