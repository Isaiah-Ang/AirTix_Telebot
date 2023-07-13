import asyncio
from telegram import *
# from telegram.ext import ApplicationBuilder, CallbackContext, filters, ConversationHandler, CommandHandler, MessageHandler
from telegram.ext import *
import logging
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ARRIVAL_COUNTRY, ARRIVAL_CITY, DEPARTURE_COUNTRY, DEPARTURE_CITY = range(4)

details = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def depart_country(update: Update, context: CallbackContext):
    await update.message.reply_text(
        text="Input your departure country"
    )

    return DEPARTURE_COUNTRY


async def depart_city(update: Update, context: CallbackContext):
    text = update.message.text
    details['departure_country'] = text
    await update.message.reply_text(
        text="Input your departure city"
    )

    return DEPARTURE_CITY


async def arrival_country(update: Update, context: CallbackContext):
    text = update.message.text
    details['departure_city'] = text
    # Add an API call here to retrieve airports within the country
    await update.message.reply_text(
        text='Input your arrival country'
    )

    return ARRIVAL_COUNTRY


async def arrival_city(update: Update, context: CallbackContext):
    text = update.message.text
    details['arrival_country'] = text
    await update.message.reply_text(
        text="Input your arrival city"
    )

    return ARRIVAL_CITY


async def confirmation(update: Update, context: CallbackContext):
    text = update.message.text
    details['arrival_city'] = text
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f'You have selected: \nDeparture: {details["departure_city"]}, {details["departure_country"]} \nArrival: {details["arrival_city"], {details["arrival_country"]}}'
    )


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Name Conversation cancelled by user. Bye. Send /new to start again')
    return ConversationHandler.END


async def unknown(update: Update, context: CallbackContext):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, I didn't understand what you are trying to say."
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.GETENV("API_KEY")).build()

    application.add_handler(CommandHandler('start', start))
    # application.add_handler(ConversationHandler('new', new_flight))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new', depart_country)],
        states={
            DEPARTURE_COUNTRY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    depart_city,
                )
            ],
            DEPARTURE_CITY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    arrival_country,
                )
            ],
            ARRIVAL_COUNTRY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    arrival_city,
                )
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    # LEAVE THIS AT THE LAST TO HANDLE UNKNOWN COMMANDS
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    application.run_polling()
