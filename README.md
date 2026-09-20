# SimpleTGBot

A simple Telegram bot with a reply-keyboard menu and a free AI assistant.

## Menu

- **Student** - returns the student name and group.
- **IT-technologies** - a short plain-text overview of IT technologies.
- **Contacts** - placeholder phone number and e-mail.
- **Prompt AI** - sends the user's prompt to a free LLM on Groq (`openai/gpt-oss-20b` by default) and returns the answer. The mode stays active until another menu item is chosen.

## Stack

- Python 3.13
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- Groq OpenAI-compatible API (free tier)
- Flask (webhook endpoint for hosting on PythonAnywhere)

## Project structure

- `bot.py` - bot instance, menu and handlers
- `app.py` - Flask webhook app used in production
- `polling.py` - long polling runner for local development
- `.env.example` - required environment variables

## Configuration

Copy `.env.example` to `.env` and fill in the values:

- `TELEGRAM_BOT_TOKEN` - token from [@BotFather](https://t.me/BotFather)
- `GROQ_API_KEY` - key from [console.groq.com](https://console.groq.com/keys)
- `WEBHOOK_SECRET` - any random string (A-Z, a-z, 0-9, `_`, `-`), used to verify that webhook requests come from Telegram
- `GROQ_MODEL` - optional, defaults to `openai/gpt-oss-20b`

## Run locally

```
pip install -r requirements.txt
python polling.py
```

## Deploy on PythonAnywhere (free plan)

1. Create a free account and open a Bash console.
2. Clone the repository and create a virtual environment:
   ```
   git clone <repository-url> SimpleTGBot
   cd SimpleTGBot
   python3.13 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Create `.env` in the project directory with the variables listed above.
4. On the **Web** tab, add a new web app with **Manual configuration** and the same Python version.
5. Set the virtualenv path to `/home/<username>/SimpleTGBot/venv`.
6. Edit the WSGI configuration file so that it contains only:
   ```python
   import sys

   project_home = "/home/<username>/SimpleTGBot"
   if project_home not in sys.path:
       sys.path.insert(0, project_home)

   from app import app as application
   ```
7. Click **Reload**.
8. Register the webhook by opening this URL in a browser once:
   ```
   https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook?url=https://<username>.pythonanywhere.com/webhook&secret_token=<WEBHOOK_SECRET>
   ```

Free PythonAnywhere web apps must be renewed by pressing the extension button on the **Web** tab roughly once a month.
