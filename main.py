from pytube import YouTube
import schedule
from telebot import TeleBot
from config import TOKEN, SENDING_TIME, CHAT_IDS, URL

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


def add_spaces(s):
    s = str(s)[::-1]
    result = ' '.join(s[i:i + 3] for i in range(0, len(s), 3))
    return result[::-1]


def send_message(chat_id, title, views, prev_views, prognosis):
    text = f"<a href='{URL}'>{title}</a>  has {add_spaces(views)} views \n(+{add_spaces(views - prev_views)}, {prognosis})"
    bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML", disable_web_page_preview=True)
    send_200m_alert(views, chat_id)


def send_200m_alert(views, chat_id):
    if views >= 200_000_000:
        for i in range(10):
            bot.send_message(chat_id=chat_id, text="WTF TADC JUST HIT 200M")


def get_prognosis(views):
    rate = views - get_prev_views()
    remaining = 200000000 - views
    return f"approximately {remaining/rate:.1f} days remain"


def send_messages():
    url = URL
    title = get_title(url)
    views = get_views(url)
    prev_views = get_prev_views()
    prognosis = get_prognosis(views)
    print(f"Previous views {prev_views}, currently {views}, prognosis {prognosis}")
    for chat_id in CHAT_IDS:
        send_message(chat_id, title, views, prev_views, prognosis)
        print(f"Sent to {chat_id}")
    write_prev_views(views)
    print(f"Wrote {views} to file")


if __name__ == "__main__":
    schedule.every().day.at(SENDING_TIME).do(send_messages)

    while True:
        schedule.run_pending()
