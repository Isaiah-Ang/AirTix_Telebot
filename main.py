import asyncio
from telegram import *
from telegram.ext import *
import Constants as keys
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CHOOSING, CHOSEN, TYPING_CHOICE = range(3)

details = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def new_flight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="Input your departure country"
    )

    return CHOOSING


async def arrival_loc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    details['departure'] = text
    await update.message.reply_text(
        text='Input your arrival country'
    )

    return CHOSEN


async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    details['arrival'] = text
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f'You have selected: \nDeparture: {details["departure"]} \nArrival: {details["arrival"]}'
    )


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Name Conversation cancelled by user. Bye. Send /new to start again')
    return ConversationHandler.END


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, I didn't understand what you are trying to say."
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(keys.API_KEY).build()

    application.add_handler(CommandHandler('start', start))
    # application.add_handler(ConversationHandler('new', new_flight))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new', new_flight)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    arrival_loc,
                )
            ],
            CHOSEN: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    confirmation,
                )
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    # LEAVE THIS AT THE LAST TO HANDLE UNKNOWN COMMANDS
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    application.run_polling()
