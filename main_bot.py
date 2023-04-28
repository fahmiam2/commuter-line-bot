import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
from main import Krl, Fare
from main_route import Route

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

SCHEDULE_INFO, SCHEDULE_INFO_START_TIME, SCHEDULE_INFO_END_TIME, FARE_INFO, FARE_INFO_DEST, MENU, ROUTE_INFO, ROUTE_MAP_DOWNLOADED = range(8)

def get_config() -> dict:
    try:
        with open("config.json", 'r') as f:
            cfg: dict = json.load(f)
        return cfg
    except FileNotFoundError:
        logger.error("Config file not found.")
    except json.JSONDecodeError as e:
        logger.error(f"Error while decoding config file: {e}")

def start(update: Update, _: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Check Schedule", callback_data='schedule_info'),
            InlineKeyboardButton("Check Fare", callback_data='fare_info'),
            InlineKeyboardButton("Route Map", callback_data='route_info')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Hi there! What would you like to do?', reply_markup=reply_markup)

def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("Back to main menu", callback_data='back_to_menu')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'schedule_info':
        query.edit_message_text(text="Please enter the station name:")
        return SCHEDULE_INFO
    elif query.data == 'fare_info':
        query.edit_message_text(text="Please enter the origin station name:")
        return FARE_INFO
    elif query.data == 'route_info':
        query.edit_message_text(text="Please type the area of the route map you want to download (Jabodetabek, Bandung Raya, Yogyakarta, or Surabaya):")
        return ROUTE_INFO
    elif query.data == 'back_to_menu':
        query.edit_message_text(text='Hi there! What would you like to do?', reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Check Schedule", callback_data='schedule_info'),
                InlineKeyboardButton("Check Fare", callback_data='fare_info'),
                InlineKeyboardButton("Route Map", callback_data='route_info')
                ]
            ])
        )
        return ConversationHandler.END

def schedule_info(update: Update, context: CallbackContext) -> int:
    station_name = update.message.text
    context.user_data['station_name'] = station_name
    update.message.reply_text('Please enter the start time (HH:00) or just type `NOW`:')
    return SCHEDULE_INFO_START_TIME

def schedule_info_start_time(update: Update, context: CallbackContext) -> int:
    start_time = update.message.text
    station_name = context.user_data['station_name']
    if start_time.lower() == "now":
        start_time = None
        end_time = None
        krl = Krl(station_name=station_name, start_time=start_time, end_time=end_time)
        schedule_data = krl.get_schedule()
        if schedule_data:
            formatted_schedule = krl.format_schedule(schedule_data)
            update.message.reply_text('Here is the schedule:')
            update.message.reply_text(str(formatted_schedule))
            update.message.reply_text('Is there anything else you need?', reply_markup=back_to_menu_keyboard())
        else:
            update.message.reply_text('No schedule found.')
            update.message.reply_text('Is there anything else you need?', reply_markup=back_to_menu_keyboard())
    else:
        context.user_data['start_time'] = start_time
        update.message.reply_text('Please enter the end time (HH:00):')
        return SCHEDULE_INFO_END_TIME

def schedule_info_end_time(update: Update, context: CallbackContext) -> None:
    end_time = update.message.text
    station_name = context.user_data['station_name']
    start_time = context.user_data['start_time']
    krl = Krl(station_name=station_name, start_time=start_time, end_time=end_time)
    schedule_data = krl.get_schedule()

    if schedule_data:
        formatted_schedule = krl.format_schedule(schedule_data)
        update.message.reply_text('Here is the schedule:')
        update.message.reply_text(str(formatted_schedule))
        update.message.reply_text('Is there anything else you need?', reply_markup=back_to_menu_keyboard())
    else:
        update.message.reply_text('No schedule found.')
        update.message.reply_text('Is there anything else you need?', reply_markup=back_to_menu_keyboard())
    

def fare_info(update: Update, context: CallbackContext) -> int:
    origin_station = update.message.text
    context.user_data['origin_station'] = origin_station
    update.message.reply_text('Please enter the destination station name:')
    return FARE_INFO_DEST

def fare_info_dest(update: Update, context: CallbackContext) -> None:
    dest_station = update.message.text
    origin_station = context.user_data['origin_station']
    fare = Fare(station_name=origin_station, dest_station_name=dest_station)
    fare_data = fare.get_fare()

    if fare_data:
        formatted_fare = fare.format_fare(fare_data)
        update.message.reply_text('The fare for this route is:')
        update.message.reply_text(str(formatted_fare))
        update.message.reply_text('Do you need more information?', reply_markup=back_to_menu_keyboard())
    else:
        update.message.reply_text('No fare information found.')
        update.message.reply_text('Do you need more information?', reply_markup=back_to_menu_keyboard())

def route_info(update: Update, context: CallbackContext) -> int:
    area = update.message.text
    context.user_data['area'] = area.upper()
    route = Route(area.upper())
    image_url = route.find_route_map()
    if image_url:
        update.message.reply_text(f'Please wait, we will provide the commuter line {area} route map to you')
        local_image_path = route.download_route_map(image_url)
        print(f"Downloaded {area} route map to {local_image_path}")
        with open(local_image_path, 'rb') as photo_file:
            update.message.reply_photo(photo=photo_file)
        update.message.reply_text('Do you anything else?', reply_markup=back_to_menu_keyboard())
        # os.remove(local_image_path)
    else:
        update.message.reply_text('No route map found.')
        update.message.reply_text('Do you anything else?', reply_markup=back_to_menu_keyboard())
    # return ROUTE_MAP_DOWNLOADED

# def route_map_downloaded

def main() -> None:
    config:dict = get_config()
    updater = Updater(token=config["TELEGRAM_API_TOKEN"], use_context=True)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start), 
            CallbackQueryHandler(button)
        ],
        states={
            SCHEDULE_INFO: [MessageHandler(Filters.text & ~Filters.command, schedule_info)],
            SCHEDULE_INFO_START_TIME: [MessageHandler(Filters.text & ~Filters.command, schedule_info_start_time)],
            SCHEDULE_INFO_END_TIME: [MessageHandler(Filters.text & ~Filters.command, schedule_info_end_time)],
            FARE_INFO: [MessageHandler(Filters.text & ~Filters.command, fare_info)],
            FARE_INFO_DEST: [MessageHandler(Filters.text & ~Filters.command, fare_info_dest)],
            ROUTE_INFO: [MessageHandler(Filters.text & ~Filters.command, route_info)]
        },
        fallbacks=[],
        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()