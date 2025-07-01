import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import requests

TOKEN = 'YOUR TELEGRAM TOKEN'  # Вставьте сюда токен вашего Telegram-бота
API_KEY = 'YOUR API KEY'  # Ваш API ключ apilayer

bot = telebot.TeleBot(TOKEN)

currencies = {
    'USD': '🇺🇸 USD',
    'EUR': '🇪🇺 EUR',
    'UZS': '🇺🇿 UZS',
    'RUB': '🇷🇺 RUB',
    'GBP': '🇬🇧 GBP',
    'JPY': '🇯🇵 JPY'
}

users = {}

texts = {
    'choose_language': {
        'ru': "Выберите язык 🇷🇺 / 🇬🇧 English / 🇺🇿 O'zbek:",
        'en': "Choose language 🇷🇺 Русский / 🇬🇧 English / 🇺🇿 Uzbek:",
        'uz': "Tilni tanlang 🇷🇺 Ruscha / 🇬🇧 Inglizcha / 🇺🇿 O'zbekcha:"
    },
    'select_base': {
        'ru': "Выберите первую валюту (откуда меняем):",
        'en': "Select base currency (from):",
        'uz': "Asosiy valyutani tanlang (qayerdan):"
    },
    'select_target': {
        'ru': "Выберите валюту для сравнения:",
        'en': "Select target currency:",
        'uz': "Qiyoslash uchun valyutani tanlang:"
    },
    'base_selected': {
        'ru': "Выбрана базовая валюта: {}",
        'en': "Base currency selected: {}",
        'uz': "Asosiy valyuta tanlandi: {}"
    },
    'different_currency': {
        'ru': "Пожалуйста, выберите другую валюту.",
        'en': "Please select a different currency.",
        'uz': "Iltimos, boshqa valyutani tanlang."
    },
    'failed_rate': {
        'ru': "❌ Не удалось получить курс валют. Попробуйте позже.",
        'en': "❌ Failed to get exchange rate. Please try later.",
        'uz': "❌ Valyuta kursini olishda xatolik. Keyinroq urinib ko'ring."
    },
    'conversion': {
        'ru': "💱 *Конвертация валюты*\n\n1 {} = *{:.4f}* {}\n\nОтлично! Вы можете сделать новый запрос.",
        'en': "💱 *Currency Conversion*\n\n1 {} = *{:.4f}* {}\n\nGreat! You can make a new conversion.",
        'uz': "💱 *Valyuta konvertatsiyasi*\n\n1 {} = *{:.4f}* {}\n\nAjoyib! Yangi so'rov yuborishingiz mumkin."
    },
    'new_request': {
        'ru': "🔄 Новый запрос",
        'en': "🔄 New conversion",
        'uz': "🔄 Yangi so'rov"
    },
    'start_info': {
        'ru': "Выберите язык:",
        'en': "Choose language:",
        'uz': "Tilni tanlang:"
    },
    'already_selected': {
        'ru': "Нажмите 🔄 Новый запрос, чтобы начать заново.",
        'en': "Press 🔄 New conversion to start over.",
        'uz': "Boshlash uchun 🔄 Yangi so'rov tugmasini bosing."
    }
}

def language_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz")
    )
    return markup

def currencies_keyboard(exclude=None, lang='en'):
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = []
    for code, label in currencies.items():
        if code != exclude:
            buttons.append(InlineKeyboardButton(label, callback_data=f"cur_{code}"))
    for i in range(0, len(buttons), 3):
        markup.row(*buttons[i:i+3])
    # Кнопка сброса убрана из валютного меню по вашему запросу
    return markup

def conversion_result_keyboard(lang='en'):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(texts['new_request'][lang], callback_data="reset"))
    return markup

def get_rate(base, target):
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={base}&symbols={target}"
    headers = {"apikey": API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        if 'rates' in data and target in data['rates']:
            return data['rates'][target]
        else:
            return None
    except Exception as e:
        print("API error:", e)
        return None

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    users[chat_id] = {'lang': None, 'base': None, 'target': None}
    bot.send_message(chat_id, texts['choose_language']['en'], reply_markup=language_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call: CallbackQuery):
    chat_id = call.message.chat.id
    lang = call.data.split('_')[1]
    users[chat_id]['lang'] = lang
    users[chat_id]['base'] = None
    users[chat_id]['target'] = None

    bot.edit_message_text(texts['select_base'][lang], chat_id, call.message.message_id,
                          reply_markup=currencies_keyboard(lang=lang))

@bot.callback_query_handler(func=lambda call: call.data.startswith('cur_'))
def choose_currency(call: CallbackQuery):
    chat_id = call.message.chat.id
    code = call.data.split('_')[1]
    lang = users[chat_id]['lang']
    base = users[chat_id]['base']
    target = users[chat_id]['target']

    if base is None:
        users[chat_id]['base'] = code
        text = f"{texts['base_selected'][lang].format(currencies[code])}\n\n{texts['select_target'][lang]}"
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=currencies_keyboard(exclude=code, lang=lang))
    elif target is None:
        if code == base:
            bot.answer_callback_query(call.id, texts['different_currency'][lang])
            return
        users[chat_id]['target'] = code
        rate = get_rate(base, code)
        if rate is None:
            text = texts['failed_rate'][lang]
            markup = currencies_keyboard(lang=lang)
        else:
            text = texts['conversion'][lang].format(currencies[base], rate, currencies[code])
            markup = conversion_result_keyboard(lang=lang)

        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')
    else:
        bot.answer_callback_query(call.id, texts['already_selected'][lang])

@bot.callback_query_handler(func=lambda call: call.data == 'reset')
def reset_selection(call: CallbackQuery):
    chat_id = call.message.chat.id
    lang = users[chat_id]['lang']
    users[chat_id]['base'] = None
    users[chat_id]['target'] = None
    bot.edit_message_text(texts['select_base'][lang], chat_id, call.message.message_id,
                          reply_markup=currencies_keyboard(lang=lang))

bot.polling(none_stop=True)
