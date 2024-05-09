## logistic tracker bot
## May 03/2024

import os
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# here is line 1

from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())                  # read local .env file
openai_api_key  = os.getenv('OPENAI_API_KEY')
token = os.getenv('TELEGRAM_BOT_TOKEN')

# SQL database
from langchain_community.utilities.sql_database import SQLDatabase
db = SQLDatabase.from_uri("sqlite:///database\chinook.db")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools")

# here is line 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and introduces itself."""

    await context.bot.send_message(chat_id=update.effective_chat.id,
        text="""Hi! Welcome to XYZ Consultants. How can I help you?\n
        Send /cancel to end the conversation.\n\n""")

async def bot_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns the reply to user after getting reply from server."""
    user = update.message.from_user
    logger.info("Question from User: %s", update.message.text)
    if update.message.text != '':
        llm_reply = agent_executor.invoke(update.message.text)
    else:
        return 

    await update.message.reply_text(llm_reply["output"])


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "It was a pleasure taking to you today. Have a great day."
    )

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,bot_reply))
    application.add_handler(CommandHandler("cancel", cancel))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()