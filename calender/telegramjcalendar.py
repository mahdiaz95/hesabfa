from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from convert_numbers import english_to_hindi

import jdatetime as datetime
import utils
import messages
import jdatetime
days = [
    'ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج'
]


def create_calendar(year=None, month=None):
    now = datetime.datetime.now()
    if not year: year = now.year
    if not month: month = now.month

    keyboard = []

    # First row - Month and Year
    row = []
    datetime.set_locale('fa_IR')
    row.append(
        InlineKeyboardButton(
            datetime.date(year, month, 1).strftime("%B") + " " + str(year),
            callback_data=create_callback_data("IGNORE")
        )
    )
    keyboard.append(row)

    # Second row - Week Days
    row = []
    for day in days:
        row.append(InlineKeyboardButton(day, callback_data=create_callback_data("IGNORE")))
    keyboard.append(row)

    month_weeks = monthcalendar(year, month)
    for week in month_weeks:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data=create_callback_data("IGNORE")))
            else:
                row.append(
                    InlineKeyboardButton(
                        str(day),
                        callback_data=create_callback_data("DAY", year, month, day)
                    )
                )
        keyboard.append(row)

    # Last row - Buttons
    row = []
    #if month != now.month:
    row.append(InlineKeyboardButton("<",callback_data=create_callback_data("PREV-MONTH", year, month, day)))
    #else:
      #  row.append(InlineKeyboardButton(" ", callback_data=create_callback_data("IGNORE")))
    row.append(
        InlineKeyboardButton(
            ">",
            callback_data=create_callback_data("NEXT-MONTH", year, month, day)
        )
    )
    keyboard.append(row)
    print(keyboard)
    return InlineKeyboardMarkup(keyboard)


async def process_calendar_selection(bot, update):
    out = (False, None)
    query = update.callback_query
    (_, action, year, month, day) = utils.separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        await bot.answer_callback_query(callback_query_id=query.id)
    elif action == "DAY":
        await bot.edit_message_text(
            text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )
        out = True,datetime.datetime(int(year), int(month), int(day)).strftime('%Y-%m-%d')
        #translate_date_to_fa(
           # datetime.datetime(int(year), int(month), int(day)).strftime('%A %d %B'))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        await bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(int(pre.year), int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        await bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(int(ne.year), int(ne.month)))
    else:
        await bot.answer_callback_query(callback_query_id=query.id, text=CALLBACK_ERROR)

    return out


def monthcalendar(year=datetime.datetime.today().year, month=datetime.datetime.today().month):
    start_day_week_day = datetime.date(year, month, 1).weekday()

    weeks = []
    weeks.append([0] * start_day_week_day + list(range(1, 8 - start_day_week_day)))

    days_left = (datetime.date(year, month, 1) - datetime.timedelta(days=1)).day - weeks[0][-1]
    days_left = monthrange(year, month) - weeks[0][-1]


    for i in range(days_left // 7):
        weeks.append(list(range(weeks[i][-1] + 1, weeks[i][-1] + 8)))
    if days_left % 7:
        weeks.append(list(range(weeks[-1][-1] + 1, weeks[-1][-1] + 1 + (days_left % 7))) + [0] * (7 - days_left % 7))


    return weeks
def monthrange(year, month):
    """Return the number of days in the given month."""
    start_day = jdatetime.date(year, month, 1)
    if month == 12:
        next_month = jdatetime.date(year + 1, 1, 1)
    else:
        next_month = jdatetime.date(year, month + 1, 1)
    return (next_month - start_day).days

# Then, we can use this function to calculate days_left:



def translate_date_to_fa(date: str) -> str:
    date = utils.reformat_persian_date(date)
    splitted = date.split()
    return f'{splitted[0]} {english_to_hindi(int(splitted[1]))} {splitted[2]}'


def create_callback_data(action, year=0, month=0, day=0):
    return messages.JCALENDAR_CALLBACK + ";" + ";".join([action, str(year), str(month), str(day)])