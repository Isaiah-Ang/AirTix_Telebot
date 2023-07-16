import asyncio
from telegram import *
from telegram.ext import *
import logging
import os
from dotenv import load_dotenv, dotenv_values
from api import flight_api, codes

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

START, DESTINATION_COUNTRY, DESTINATION_CITY, SELECT_ORIGIN_AIRPORT, ORIGIN_COUNTRY, ORIGIN_CITY, SELECT_DESTINATION_AIRPORT, END, CONFIRM, RETRY = range(
    10)

details = {}

# Start file


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )

# country_select


async def origin_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="Input your origin country"
    )

    return ORIGIN_COUNTRY


async def start_over_origin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        text="Input your origin country"
    )

    return ORIGIN_COUNTRY


async def origin_city(update: Update, context: CallbackContext):
    text = update.message.text
    details['origin_country'] = text
    await update.message.reply_text(
        text="Input your origin city"
    )

    return ORIGIN_CITY


async def origin_airport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    details['origin_city'] = text

    airport = codes.convert_country_code(
        details['origin_city'], details['origin_country'])

    buttons = [[InlineKeyboardButton(f"{x['name']} ({x['code']})", callback_data=f"{x['code']}")] for x in airport]

    await update.message.reply_text(
        text=f'Please choose your airport',
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    return SELECT_ORIGIN_AIRPORT

# async def origin_airport_button(update: Update, context: ContextTypes.DEFAULT_TYPE):


async def destination_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()
    #Split the callback data to retrieve the 3 digit airport code
    details['origin_airport'] = (query.data).split('/')[0]

    await update.callback_query.edit_message_text(
        text=f"Input your destination country"
    )

    return DESTINATION_COUNTRY


async def destination_city(update: Update, context: CallbackContext):
    text = update.message.text
    details['destination_country'] = text
    await update.message.reply_text(
        text="Input your destination city"
    )

    return DESTINATION_CITY


async def destination_airport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    details['destination_city'] = text

    airport = codes.convert_country_code(
        details['destination_city'], details['destination_country'])

    buttons = [[InlineKeyboardButton(f"{x['name']} ({x['code']})", callback_data=f"{x['code']}")] for x in airport]

    await update.message.reply_text(
        text=f'Please choose your airport',
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    return SELECT_DESTINATION_AIRPORT


async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()
    #Split the callback data to retrieve the 3 digit airport code
    details['destination_airport'] = (query.data).split('/')[0]

    buttons = [
        [
            InlineKeyboardButton("Yes", callback_data=str(CONFIRM))
        ],
        [
            InlineKeyboardButton("Retry", callback_data=str(RETRY))
        ]
    ]
    await update.callback_query.edit_message_text(
        text=f'You have selected: \nFrom\n{details["origin_city"]}, {details["origin_country"]} ({details["origin_airport"]})\n\nTo\n{details["destination_city"]}, {details["destination_country"]} ({details["destination_airport"]})\nIs that correct?',
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    return END
# cancel


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Name Conversation cancelled by user. Bye. Send /new to start again')
    return ConversationHandler.END

# unknown


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, I didn't understand what you are trying to say."
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("API_KEY")).build()

    application.add_handler(CommandHandler('start', start))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new', origin_country)],
        states={
            ORIGIN_COUNTRY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    origin_city,
                )
            ],
            ORIGIN_CITY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    origin_airport,
                )
            ],
            SELECT_ORIGIN_AIRPORT: [
                CallbackQueryHandler(
                    destination_country, pattern="^[a-zA-Z]{3}\/" + str(SELECT_ORIGIN_AIRPORT) + "$")
            ],
            DESTINATION_COUNTRY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    destination_city,
                )
            ],
            DESTINATION_CITY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    destination_airport
                )
            ],
            SELECT_DESTINATION_AIRPORT: [
                CallbackQueryHandler(
                    confirmation, pattern="^[a-zA-Z]{3}\/" +
                    str(SELECT_DESTINATION_AIRPORT) + "$"
                )
            ],
            END: [
                # CallbackQueryHandler(get_prices), pattern="^" + str(CONFIRM) + "$"
                CallbackQueryHandler(
                    start_over_origin, pattern="^" + str(RETRY) + "$")
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    # LEAVE THIS AT THE LAST TO HANDLE UNKNOWN COMMANDS
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    application.run_polling()
