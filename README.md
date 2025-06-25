# 📊 Hesabfa Telegram Accounting Bot

This project is a **Telegram bot for managing and recording accounting documents**. Users can interact with the bot through a simple Persian-language interface to submit financial records
, which are then sent to an admin for approval.

## 🚀 Key Features

- Record different types of accounting operations:
  - Income (Daryaft)
  - Expense (Hazine)
  - Bank Transfers
- Admin approval for submitted accounting records
- Supports **Jalali (Persian)** 
- Generates invoice images and sends them in Telegram
- Persian date selection using Telegram inline calendar buttons
- User authorization and role management (admin or regular user)
- Uses local storage (Pickle)
- an implementation of hesabfa api

## 🧠 Technical Overview

Main technologies and libraries used:

- `python-telegram-bot`: for Telegram bot interactions
- `persiantools`: for Jalali date conversion

🛠️ Setup & Usage

    Install dependencies:

pip install -r requirements.txt

Start the bot:

    python hesabfa.py
    
    Add your Telegram bot token and Hesabfa API credentials in a config file or as environment variables.
    you need token for generating sokhan.
    Also add admin and channel ids.

🔐 Access Control

    Only specific Telegram user IDs (e.g., 1234, 124) are treated as admins
    Regular users must be activated by an admin before they can use the bot

Feel free to fork this project, report issues, or submit pull requests.
