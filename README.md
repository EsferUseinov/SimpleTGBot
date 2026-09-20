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
