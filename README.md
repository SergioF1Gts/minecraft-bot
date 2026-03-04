# Minecraft Server Manager - Telegram Bot

A Telegram bot built with Python that allows you to manage Minecraft servers directly from a Telegram conversation. All data is stored in real time on Google Sheets and the bot runs in the cloud using Railway.

---

## Features

- Register servers with name, IP, version and type
- View the full list of registered servers
- Update the status of a server (Online, Offline, Maintenance)
- View general statistics by status and version
- Data synced in real time with Google Sheets

---

## Tech Stack

- Python 3.14
- python-telegram-bot v22
- gspread + google-auth
- python-dotenv
- Google Sheets API + Google Drive API
- Railway (cloud deployment)
- Git + GitHub

---

## Project Structure

```
minecraft-bot/
├── bot.py               # Main bot logic and commands
├── excel_manager.py     # Google Sheets connection and operations
├── Procfile             # Railway configuration
├── requirements.txt     # Project dependencies
├── .env                 # Environment variables (not uploaded to GitHub)
├── credentials.json     # Google Cloud credentials (not uploaded to GitHub)
└── .gitignore
```

---

## Bot Commands

| Command | Description |
|---|---|
| /start | Shows the welcome menu |
| /agregar | Register a new server |
| /ver | List all servers |
| /estado | Change the status of a server |
| /stats | Show general statistics |
| /cancelar | Cancel the current operation |

---

## Local Setup

1. Clone the repository:
```bash
git clone https://github.com/SergioF1Gts/minecraft-bot.git
cd minecraft-bot
```

2. Install dependencies:
```bash
pip install python-telegram-bot gspread google-auth python-dotenv
```

3. Create the `.env` file with your credentials:
```
BOT_TOKEN=your_telegram_bot_token
SHEET_ID=your_google_sheets_id
```

4. Place your Google Cloud `credentials.json` file in the project folder.

5. Run the bot:
```bash
python bot.py
```

---

## Railway Deployment

The bot is deployed on Railway with the following environment variables configured:

- `BOT_TOKEN` — Telegram bot token
- `SHEET_ID` — Google Sheet ID
- `GOOGLE_CREDENTIALS` — Contents of the Google Cloud credentials.json

---

## Branches

- `main` — Stable code ready for production
- `dev1` — Active development branch

---

## Author

**SergioF1Gts** — [github.com/SergioF1Gts](https://github.com/SergioF1Gts)
