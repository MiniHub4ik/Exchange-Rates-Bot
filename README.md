

# 💱 Telegram Bot for Currency Exchange

A Telegram bot that helps users convert currencies using real-time exchange rates from [apilayer](https://apilayer.com/). Built with Python and `pyTelegramBotAPI`. Supports English, Russian, and Uzbek languages.

---

## 📌 Features

- Multilingual support: 🇬🇧 English, 🇷🇺 Russian, 🇺🇿 Uzbek  
- Real-time exchange rates  
- Inline button navigation  
- Supports popular currencies: USD, EUR, UZS, RUB, GBP, JPY  
- Simple and clean UX flow

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Install dependencies:

```bash
pip install pyTelegramBotAPI requests
````

---

### 🔧 Configuration

Create the following file in the project root:

#### `main.py`

Replace the API keys:

```python
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
API_KEY = 'YOUR_APILAYER_API_KEY'
```

You can get the `TOKEN` from [@BotFather](https://t.me/BotFather), and the `API_KEY` from [apilayer](https://apilayer.com/).

Make sure your API plan supports currency conversion endpoints.

---

## ▶️ Run the Bot

```bash
python main.py
```

---

## 💬 Usage Flow

1. User sends `/start`
2. Chooses a language
3. Selects a base currency (e.g. USD)
4. Selects a target currency (e.g. UZS)
5. Bot shows the current exchange rate

---

## 🧾 Project Structure

```
exchange_rates_tg_bot/
├── main.py           # Main bot logic
├── README.md         # This file
├── .idea/            # IDE configs (optional)
```

---

## 🛡 Notes

* The bot uses inline keyboards for easy navigation.
* Simple error handling is implemented (e.g., retry if API fails).
* All currency selections are step-by-step to reduce user error.

---



## 📃 License

This project is free to use and modify for personal and educational purposes. No warranty provided. Contributions welcome!

---

## 🤝 Author

Made with ❤️ by Nematilla.\
Telegram: https://t.me/nematilla \
GitHub: https://github.com/MiniHub4ik

