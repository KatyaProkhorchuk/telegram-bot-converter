from app.resource import postBot
from app.Global import TOKEN, URLHERUKU
from flask import request
from flask import Flask
from flask_sslify import SSLify
import seaborn as sns
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram


app = Flask(__name__)
sns.set(style='darkgrid')

bot = telegram.Bot(token=TOKEN)


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    global URLHERUKU
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URLHERUKU, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    postBot(bot)
    return 'ok'


@app.route('/', methods=['GET', 'POST'])
def index():
    updater = Updater(TOKEN)
    updater.start_webhook(listen="0.0.0.0", port=8443, url_path=TOKEN,
                          webhook_url='https://coinsconvert.herokuapp.com/{TOKEN}')
    updater.idle()
    if request.method == 'POST':
        postBot()
    return '<h1>hello</h1>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443)
