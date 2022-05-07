from flask import request
from flask import Flask
from flask_sslify import SSLify
import seaborn as sns
from app.resource import postBot
from app.Global import TOKEN, URL
import telegram
# ~/ngrok http 5000
# https://api.telegram.org/bot5312550763:AAEhW6Qbj9TBUW0zQOUThNxpxFGDZ-bsZkY/setWebhook?url=https://328d-93-175-28-9.eu.ngrok.io

app = Flask(__name__)
# sslify = SSLify(app)
sns.set(style='darkgrid')

bot = telegram.Bot(token=TOKEN)
@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        postBot()
    return '<h1>hello</h1>'


if __name__ == '__main__':
    app.run()
