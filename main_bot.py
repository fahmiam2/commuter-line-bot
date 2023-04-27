import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from main import Krl, Fare

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def start(update: Update, _: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Schedule Info", callback_data='schedule_info'),
            InlineKeyboardButton("Fare Info", callback_data='fare_info')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'schedule_info':
        query.edit_message_text(text="Please enter the station name:")
        return 'schedule_info'
    elif query.data == 'fare_info':
        query.edit_message_text(text="Please enter the origin station name:")
        return 'fare_info'

def schedule_info(update: Update, _: CallbackContext) -> None:
    station_name = update.message.text
    krl = Krl(station_name=station_name)
    schedule = krl.get_schedule()

    if schedule:
        update.message.reply_text(str(schedule))
    else:
        update.message.reply_text('No schedule found.')

def fare_info(update: Update, _: CallbackContext) -> None:
    origin_station = update.message.text
    update.message.reply_text('Please enter the destination station name:')
    return origin_station

def fare_info_dest(update: Update, context: CallbackContext) -> None:
    dest_station = update.message.text
    origin_station = context.user_data['origin_station']
    fare = Fare(station_name=origin_station, dest_station_name=dest_station)
    fare_result = fare.get_fare()

    if fare_result:
        update.message.reply_text(str(fare_result))
    else:
        update.message.reply_text('No fare information found.')

def main() -> None:
    updater = Updater("YOUR_BOT_TOKEN")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, schedule_info))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, fare_info))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()