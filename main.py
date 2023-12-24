from pytube import YouTube
import schedule
from telebot import TeleBot
from config import TOKEN, SENDING_TIME, CHAT_IDS, URL
from datetime import datetime
bot = TeleBot(TOKEN)


def get_prev_views():
    try:
        with open("last.txt", "r") as f:
            views = f.read().strip()
        if views in (None, ""):
            return 0
        return int(views)
    except FileNotFoundError:
        write_prev_views(0)
        return 0


def write_prev_views(views):
    with open("last.txt", "w") as f:
        f.write(str(views))


def get_views(url):
    yt = YouTube(url)
    return yt.views


def get_title(url):
    yt = YouTube(url)
    return yt.title


def get_time(url):
    yt = YouTube(url)
    return yt.publish_date


def add_spaces(s):
    s = str(s)[::-1]
    result = ' '.join(s[i:i + 3] for i in range(0, len(s), 3))
    return result[::-1]


def send_message(chat_id, title, views, time, average):
    text = f"<a href='{URL}'>{title}</a> \nтолько что достиг {add_spaces(views)} просмотров!!1!!11! \n(ему понадобилось {time}, и он получал в среднем {average:.2f} миллионов просмотров в день)"
    bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML", disable_web_page_preview=True)


def get_prognosis(views):
    rate = views - get_prev_views()
    remaining = 200000000 - views
    return f"approximately {remaining/rate:.1f} days remain"


def send_messages():
    url = URL
    title = get_title(url)
    views = get_views(url)
    time = get_time(url)
    time_diff = datetime.now() - time
    time_diff_days = int(time_diff.days)
    average = views / time_diff_days / 1_000_000

    if views >= 200_000_000:
        for chat_id in CHAT_IDS:
            send_message(chat_id, title, views, time_diff, average)
        exit()


schedule.every(10).seconds.do(send_messages)

while True:
    schedule.run_pending()
