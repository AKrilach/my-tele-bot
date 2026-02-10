import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode

TOKEN = "8532773844:AAF0I0Mpp6k_wPeoTXtoAlrlcaGXpTs8Qt4"
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_keyboard():
    kb = [
        [KeyboardButton(text="🏠 Нерухомість (Р3)"), KeyboardButton(text="🚗 Транспорт (Р6)")],
        [KeyboardButton(text="💰 Доходи (Р11)"), KeyboardButton(text="💵 Гроші (Р12)")],
        [KeyboardButton(text="💳 Рахунки (Р12.1)"), KeyboardButton(text="📉 Кредити (Р13)")],
        [KeyboardButton(text="👤 Сім'я (Р2)"), KeyboardButton(text="🏗 Будова (Р5)")],
        [KeyboardButton(text="💎 Цінні речі (Р4)"), KeyboardButton(text="📈 Активи (Р7-10)")],
        [KeyboardButton(text="💸 Видатки (Р14)"), KeyboardButton(text="🚫 Сумісництво (Р15)")],
        [KeyboardButton(text="🏛 Органи (Р16)"), KeyboardButton(text="ℹ️ Допомога")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 <b>Вітаю у системі допомоги декларування!</b>\n\n"
        "Оберіть розділ декларації нижче, щоб отримати розгорнуту інформацію.\n"
        "Всі дані актуальні на 2026 рік.",
        reply_markup=get_keyboard(),
        parse_mode=ParseMode.HTML
    )

@dp.message()
async def handle_docs(message: types.Message):
    t = message.text
    res = ""

    if t == "🏠 Нерухомість (Р3)":
        res = ("<b>Розділ 3. Об'єкти нерухомості</b>\n\n"
               "• <b>Що вказуємо:</b> Квартири, будинки, кімнати, гуртожитки, гаражі, земельні ділянки.\n"
               "• <b>Тип права:</b> Власність, оренда, право користування (навіть безоплатне), реєстрація місця проживання.\n"
               "• <b>Важливо:</b> Обов'язково вказуйте об'єкт, у якому ви проживали на 31.12, навіть якщо він не ваш.\n"
               "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/'>Детально на НАЗК</a>")

    elif t == "🚗 Транспорт (Р6)":
        res = ("<b>Розділ 6. Транспортні засоби</b>\n\n"
               "• <b>Що вказуємо:</b> Авто, мотоцикли, причепи, водні та повітряні засоби.\n"
               "• <b>Оренда/Довіреність:</b> Якщо ви користуєтесь авто за довіреністю — це теж вказується.\n"
               "• <b>Ціна:</b> Вказується вартість на дату набуття права.\n"
               "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-tsinne-ruhome-majno-transportni-zasoby/'>Детально на НАЗК</a>")

    elif t == "💰 Доходи (Р11)":
        res = ("<b>Розділ 11. Доходи та подарунки</b>\n\n"
               "• <b>Види:</b> Зарплата (БРУТТО, тобто до вирахування податків), пенсія, соцвиплати (ВПО, лікарняні), гонорари, дивіденди.\n"
               "• <b>Подарунки:</b> Декларуються, якщо разово сума > 5 ПМ або сукупно від однієї особи > 10 ПМ.\n"
               "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xiii-dohody-u-tomu-chysli-podarunky/'>Детально на НАЗК</a>")

    elif t == "💵 Гроші (Р12)":
        res = ("<b>Розділ 12. Грошові активи</b>\n\n"
               "• <b>Що входить:</b> Готівка (вдома), кошти на банківських рахунках, внески до кредитних спілок.\n"
               "• <b>Поріг:</b> Декларується, якщо сумарно (ви + сім'я) у вас більше 50 прожиткових мінімумів.\n"
               "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xiv-groshovi-aktyvy/'>Детально на НАЗК</a>")

    elif t == "💳 Рахунки (Р12.1)":
        res = ("<b>Розділ 12.1. Банківські рахунки</b>\n\n"
               "• <b>Важливо:</b> Тут вказуються номери IBAN рахунків, а не суми.\n"
               "• <b>Що вносити:</b> Усі рахунки, які були відкриті протягом звітного року, навіть якщо вони вже закриті.\n"
               "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>Детально на НАЗК</a>")

    elif t == "📉 Кредити (Р13)":
        res = ("<b>Розділ 13. Фінансові зобов’язання</b>\n\n"
               "• <b>Що вносити:</b> Отримані кредити, позики, залишки за лімітами на кредитних картках.\n"
               "• <b>Умова:</b> Якщо залишок боргу на 31.12 перевищує 50 ПМ.\n"
               "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/'>Детально на НАЗК</a>")

    elif t == "🚫 Сумісництво (Р15)":
        res = ("<b>Розділ 15. Робота за сумісництвом</b>\n\n"
               "• <b>Для НПУ:</b> Згідно зі ст. 25 Закону 'Про запобігання корупції', поліцейським ЗАБОРОНЕНО займатися іншою оплачуваною діяльністю.\n"
               "• <b>Винятки:</b> Викладацька, наукова, творча діяльність, медична практика, інструкторська та суддівська практика із спорту.\n"
               "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/'>До Бази знань</a>")

    elif t == "👤 Сім'я (Р2)":
        res = ("<b>Розділ 2. Члени сім'ї</b>\n\n"
               "• <b>Хто це:</b> Чоловік/дружина, діти до 18 років (незалежно від проживання).\n"
               "• <b>Інші:</b> Особи, які спільно проживають, пов’язані спільним побутом більше 183 днів на рік.\n"
               "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iv-sub-yekt-deklaruvannya-ta-chleny-jogo-sim-yi/'>Детально на НАЗК</a>")

    elif t == "🏗 Будова (Р5)":
        res = ("<b>Розділ 5. Незавершене будівництво</b>\n\n"
               "Об'єкти, які не прийняті в експлуатацію, або право власності на які не зареєстроване, але фактично вони існують.\n"
               "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ob-yekty-nezavershenogo-budivnytstva/'>Детально на НАЗК</a>")

    elif t == "💸 Видатки (Р14)":
        res = ("<b>Розділ 14. Видатки та правочини</b>\n\n"
               "• Вказуються разові видатки СУБ'ЄКТА декларування (не членів сім'ї).\n"
               "• Поріг: якщо разовий видаток > 50 ПМ.\n"
               "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/'>Детально на НАЗК</a>")

    if res:
        await message.answer(res, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        await message.answer("Оберіть розділ з меню нижче 👇", reply_markup=get_keyboard())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
