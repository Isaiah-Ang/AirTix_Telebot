import asyncio
from telegram import *
from telegram.ext import *
import logging
import os
from dotenv import load_dotenv, dotenv_values
from api import flight_api, codes
from functions import flight_response

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

START, DESTINATION_COUNTRY, DESTINATION_CITY, SELECT_ORIGIN_AIRPORT, ORIGIN_COUNTRY, ORIGIN_CITY, SELECT_DESTINATION_AIRPORT, END, CONFIRM, RETRY, WAIT, OUTBOUND_DATE, INBOUND_DATE = range(
    13)

details = {}
user_details = {}

# Start file


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_chat.id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me! type /new to use this bot"
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

    await query.message.reply_text(
        text="Input your origin country"
    )

    return ORIGIN_COUNTRY


async def origin_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print("origin city", text)
    details['origin_country'] = text
    await update.message.reply_text(
        text="Input your origin city"
    )

    return ORIGIN_CITY


async def origin_airport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    details['origin_city'] = text
    try:
        airport = codes.convert_country_code(
            details['origin_city'], details['origin_country'])

        buttons = [[InlineKeyboardButton(
            f"{x['name']} ({x['code']})", callback_data=f"{x['code']}/{SELECT_ORIGIN_AIRPORT}")] for x in airport]

        await update.message.reply_text(
            text=f'Please choose your airport',
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        return SELECT_ORIGIN_AIRPORT
    except:

        buttons = [
            [
                InlineKeyboardButton("Retry", callback_data=str(RETRY))
            ]
        ]
        await update.message.reply_text(
            text="No city or country found, try again",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return END


async def destination_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()
    # Split the callback data to retrieve the 3 digit airport code
    details['origin_airport'] = (query.data).split('/')[0]

    await update.callback_query.edit_message_text(
        text=f"Input your destination country"
    )

    return DESTINATION_COUNTRY


async def destination_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    buttons = [[InlineKeyboardButton(
        f"{x['name']} ({x['code']})", callback_data=f"{x['code']}/{SELECT_DESTINATION_AIRPORT}")] for x in airport]

    await update.message.reply_text(
        text=f'Please choose your airport',
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    return SELECT_DESTINATION_AIRPORT


async def get_outbound_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    details['destination_airport'] = (query.data).split('/')[0]
    await update.callback_query.edit_message_text(
        text="Input your departure date in YYYY-MM-DD"
    )

    return OUTBOUND_DATE


async def get_inbound_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    details["outbound_date"] = text

    await update.message.reply_text(
        text=f'Input your returning date in YYYY-MM-DD'
    )

    return INBOUND_DATE


async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    details['inbound_date'] = text

    buttons = [
        [
            InlineKeyboardButton("Yes", callback_data=str(CONFIRM))
        ],
        [
            InlineKeyboardButton("Retry", callback_data=str(RETRY))
        ]
    ]
    await update.message.reply_text(
        text=f'You have selected: \nFrom\n{details["origin_city"]}, {details["origin_country"]} ({details["origin_airport"]})\n\nTo\n{details["destination_city"]}, {details["destination_country"]} ({details["destination_airport"]}) on ({details["outbound_date"]}) to ({details["inbound_date"]})\nIs that correct?',
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    return END
# cancel


async def get_flights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    # Store chat ID together with details list
    user_details[update.effective_chat.id] = details

    print(user_details)

    response = flight_api.skyscan_tickets(
        details['origin_airport'], details['destination_airport'])

    flight_info = flight_response.format(response)

    buttons = [
        [
            InlineKeyboardButton(
                "Book Flight", url=flight_info['pricingOptions'][0]['items'][0]['deepLink']),
            InlineKeyboardButton("Wait", callback_data=str(WAIT))
        ]
    ]

    outbound_text = ""

    for i in flight_info['outbound'].values():
        delta = i['arrivalDateTime']['time'] - \
            i['departureDateTime']['time']
        sec = delta.total_seconds()
        min = (sec / 60) / 10
        hours = sec / (60 * 60)

        outbound_text += f"{i['flightNo']}\n{i['departureDateTime']['time'].strftime('%H:%M')}\t{i['originAirport']['iata']} {i['originAirport']['name']}\n{int(hours)}h{int(min)}\tLayover\n{i['arrivalDateTime']['time'].strftime('%H:%M')}\t{i['destinationAirport']['iata']} {i['destinationAirport']['name']}\n\n"

    inbound_text = ""

    for i in flight_info['inbound'].values():
        delta = i['arrivalDateTime']['time'] - \
            i['departureDateTime']['time']
        sec = delta.total_seconds()
        min = (sec / 60) / 10
        hours = sec / (60 * 60)

        inbound_text += f"{i['flightNo']}\n{i['departureDateTime']['time'].strftime('%H:%M')}\t{i['originAirport']['iata']} {i['originAirport']['name']}\n{abs(int(hours))}h{abs(int(min))}\tLayover\n{i['arrivalDateTime']['time'].strftime('%H:%M')}\t{i['destinationAirport']['iata']} {i['destinationAirport']['name']}\n\n"

    await update.callback_query.edit_message_text(text=f"Outbound\n{outbound_text}\n\nInbound\n{inbound_text}", reply_markup=InlineKeyboardMarkup(buttons))

    return WAIT


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
                    get_outbound_date, pattern="^[a-zA-Z]{3}\/" +
                    str(SELECT_DESTINATION_AIRPORT) + "$"
                )
            ],
            OUTBOUND_DATE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    get_inbound_date
                )
            ],
            INBOUND_DATE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    confirmation
                )
            ],
            END: [
                CallbackQueryHandler(
                    get_flights, pattern="^" + str(CONFIRM) + "$"),
                CallbackQueryHandler(
                    start_over_origin, pattern="^" + str(RETRY) + "$")
            ],
            WAIT: [
                # Function to get code to check price every few days
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    # LEAVE THIS AT THE LAST TO HANDLE UNKNOWN COMMANDS
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    application.run_polling()
