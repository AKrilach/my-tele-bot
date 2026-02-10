import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8544620393:AAHj5jjvm-2dZAd04kZAKnq-1mn-E9HEbs0"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- МАКСИМАЛЬНО РОЗШИРЕНА БАЗА ЗНАНЬ (18 РОЗДІЛІВ) ---
ANSWERS = {
    "Р1": ("📋 <b>Розділ 1: Вид декларації</b>\n\n"
           "Обираємо тип «Щорічна». Звітний період — 2025 рік. "
           "Якщо ви подаєте декларацію вперше після призначення, обираєте 'Кандидата на посаду'. "
           "Якщо звільняєтесь — 'При звільненні'.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/'>Докладніше про види декларацій</a>"),

    "Р2": ("👤 <b>Розділ 2: Суб'єкт декларування</b>\n\n"
           "Це ваші дані. ПІБ, РНОКПП та <b>УНЗР</b> (13 цифр у вашій ID-картці або закордонному паспорті). "
           "Місце роботи: <b>Управління поліції охорони в Полтавській області</b>. Код ЄДРПОУ: <b>40109042</b>. "
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
           "Сюди відносимо недобудовані будинки, а також нерухомість, яка вже збудована, але не прийнята в експлуатацію "
           "або не зареєстрована в реєстрі на вас чи члена сім'ї.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/'>Докладніше про недобудови</a>"),

    "Р5": ("💎 <b>Розділ 5: Цінне рухоме майно</b>\n\n"
           "Ювелірні вироби, техніка, антикваріат, якщо вартість <b>одного предмета</b> перевищує 100 ПМ "
           "(для 2025 року це понад 302 800 грн). Авто сюди НЕ входить.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/'>Докладніше про цінне майно</a>"),

    "Р6": ("🚗 <b>Розділ 6: Транспортні засоби</b>\n\n"
           "Вказуємо <b>ваші авто та авто сім'ї</b>. Навіть якщо ви користувалися машиною за довіреністю "
           "або техпаспортом хоча б один день протягом року — її треба внести.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/'>Докладніше про транспорт</a>"),

    "Р7": ("📈 <b>Розділ 7: Цінні папери</b>\n\n"
           "Акції, облігації, сертифікати, що належать суб'єкту або родичам.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ih-tsinni-papery/'>Докладніше про цінні папери</a>"),

    "Р8": ("🏢 <b>Розділ 8: Корпоративні права</b>\n\n"
           "Ваша частка або частка сім'ї у статутному капіталі товариств (ТОВ), підприємств, організацій.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/h-korporatyvni-prava/'>Докладніше про корп. права</a>"),

    "Р9": ("👥 <b>Розділ 9: Бенефіціарна власність</b>\n\n"
           "Юридичні особи, над якими ви або сім'я здійснюєте фактичний контроль (навіть якщо ви не власник у реєстрі).\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hi-yurydychni-osoby-trasty-abo-inshi-podibni-pravovi-utvorennya-kintsevym-benefitsiarnym-vlasnykom-kontrolerom-yakyh-ye-sub-yekt-deklaruvannya-abo-chleny-jogo-sim-yi/'>Докладніше про бенефіціарів</a>"),

    "Р10": ("💡 <b>Розділ 10: Нематеріальні активи</b>\n\n"
            "Криптовалюти (вказуємо кількість та тип), авторське право, патенти.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hii-nematerialni-aktyvy/'>Докладніше про активи</a>"),

    "Р11": ("💰 <b>Розділ 11: Доходи та подарунки</b>\n\n"
            "<b>Увага:</b> Вказуємо доходи <b>ваші та УСІХ членів сім'ї</b>. "
            "Зарплата (повна сума брутто), пенсія, допомога ВПО, відсотки по депозитах, подарунки понад 5 ПМ.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiii-dohody-u-tomu-chysli-podarunky/'>Докладніше про доходи</a>"),

    "Р12": ("💵 <b>Розділ 12: Грошові активи</b>\n\n"
            "Готівка, гроші на картках (ваші + сім'ї). Декларується, якщо загальна сума перевищує 50 ПМ.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiv-groshovi-aktyvy/'>Докладніше про гроші</a>"),

    "Р12.1": ("💳 <b>Розділ 12.1: Рахунки в банках</b>\n\n"
              "Вказуємо всі номери IBAN (ваші та сім'ї), відкриті у звітному році. Навіть якщо на рахунку 0 грн або він був закритий у кінці року.\n"
              "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>Докладніше про рахунки</a>"),

    "Р13": ("📉 <b>Розділ 13: Фінансові зобов’язання</b>\n\n"
            "Кредити, позики, ліміти по картках (ваші та сім'ї). Вказуємо тільки якщо залишок боргу на 31.12 перевищує 50 ПМ.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/'>Докладніше про кредити</a>"),

    "Р14": ("🧾 <b>Розділ 14: Видатки та правочини</b>\n\n"
            "Разові витрати <b>ТІЛЬКИ СУБ'ЄКТА</b> (поліцейського) понад 50 ПМ (наприклад, покупка авто або нерухомості одним платежем).\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/'>Докладніше про видатки</a>"),

    "Р15": ("⚠️ <b>Розділ 15: Робота за сумісництвом</b>\n\n"
            "🚫 Поліцейським заборонено іншу оплачувану діяльність, крім викладацької, наукової, творчої чи медичної.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/'>Докладніше про сумісництво</a>"),

    "Р16": ("🏛️ <b>Розділ 16: Членство в організаціях</b>\n\n"
            "Участь у керівних органах ГО, фондів, профспілок. Членство в профспілці поліції охорони вказувати НЕ потрібно, якщо ви не входите до її правління.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xix-vhodzhennya-do-kerivnyh-revizijnyh-chy-naglyadovyh-organiv/'>Докладніше про організації</a>")
}

# --- КЛАВІАТУРИ ---

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📅 Терміни подання"))
    builder.row(types.KeyboardButton(text="👤 Адмін"), types.KeyboardButton(text="⚖️ Відповідальність"))
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
    await message.answer("📋 <b>Головне меню</b>. Оберіть пункт:", reply_markup=main_menu(), parse_mode="HTML")

@dp.message(F.text == "📅 Терміни подання")
async def terms(message: types.Message):
    await message.answer("📅 <b>Щорічна декларація за 2025 рік</b> подається до <b>31 березня 2026 року включно</b>.", parse_mode="HTML")

@dp.message(F.text == "👤 Адмін")
async def contact(message: types.Message):
    await message.answer("👤 <b>Адміністратор Альона</b>\n📞 <code>0660787241</code>", parse_mode="HTML")

@dp.message(F.text == "⚖️ Відповідальність")
async def resp(message: types.Message):
    await message.answer("⚖️ <b>Відповідальність:</b>\n\n• <b>Адміністративна:</b> штрафи за помилки або несвоєчасність.\n• <b>Дисциплінарна:</b> звільнення з НПУ.\n• <b>Кримінальна:</b> за брехню в декларації на великі суми.", parse_mode="HTML")

@dp.message(F.text == "📂 Розділи декларування")
async def show_sections(message: types.Message):
    await message.answer("📝 Оберіть номер розділу для отримання детальної інструкції:", reply_markup=sections_menu(), parse_mode="HTML")

@dp.message(F.text.startswith("Розділ "))
async def handle_section(message: types.Message):
    num = message.text.replace("Розділ ", "Р")
    if num in ANSWERS:
        await message.answer(ANSWERS[num], parse_mode="HTML", disable_web_page_preview=True)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
