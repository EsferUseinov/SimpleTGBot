import os

import requests
import telebot
from dotenv import load_dotenv
from telebot import types

load_dotenv()

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b")
TELEGRAM_MESSAGE_LIMIT = 4096

BTN_STUDENT = "Студент"
BTN_TECH = "IT-технології"
BTN_CONTACTS = "Контакти"
BTN_AI = "Prompt AI"

STATIC_REPLIES = {
    BTN_STUDENT: "ст. Усеінов Е.В., гр. ІП-31",
    BTN_TECH: (
        "Сучасна ІТ-сфера охоплює Python, JavaScript та Java для розробки, "
        "хмарні платформи AWS та Azure, контейнеризацію з Docker і Kubernetes, "
        "бази даних PostgreSQL та MongoDB, а також штучний інтелект "
        "і машинне навчання."
    ),
    BTN_CONTACTS: "Тел.: +380 00 000 00 00\nE-mail: example@example.com",
}

bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_TOKEN"], threaded=False)
ai_chats = set()


def build_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    menu.add(BTN_STUDENT, BTN_TECH, BTN_CONTACTS, BTN_AI)
    return menu


def ask_ai(prompt):
    response = requests.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
        json={
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "Answer concisely in the language of the user's message.",
                },
                {"role": "user", "content": prompt},
            ],
            "max_completion_tokens": 1500,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


@bot.message_handler(commands=["start"])
def handle_start(message):
    ai_chats.discard(message.chat.id)
    bot.send_message(message.chat.id, "Оберіть пункт меню.", reply_markup=build_menu())


@bot.message_handler(func=lambda message: message.text in STATIC_REPLIES)
def handle_static(message):
    ai_chats.discard(message.chat.id)
    bot.send_message(message.chat.id, STATIC_REPLIES[message.text])


@bot.message_handler(func=lambda message: message.text == BTN_AI)
def handle_ai_start(message):
    ai_chats.add(message.chat.id)
    bot.send_message(
        message.chat.id,
        "Надішліть свій промпт, і я передам його ШІ. "
        "Щоб вийти з цього режиму, оберіть інший пункт меню.",
    )


@bot.message_handler(func=lambda message: message.chat.id in ai_chats and message.text)
def handle_ai_prompt(message):
    bot.send_chat_action(message.chat.id, "typing")
    try:
        answer = ask_ai(message.text)
    except requests.RequestException:
        answer = "Не вдалося отримати відповідь від ШІ. Спробуйте пізніше."
    bot.send_message(message.chat.id, answer[:TELEGRAM_MESSAGE_LIMIT])


@bot.message_handler(func=lambda message: True)
def handle_other(message):
    bot.send_message(message.chat.id, "Скористайтеся меню.", reply_markup=build_menu())
