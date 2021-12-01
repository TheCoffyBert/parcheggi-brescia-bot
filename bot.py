import time
import telepot
import json
import configparser

from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from urllib.request import urlopen
from bs4 import BeautifulSoup


def on_chat_message(msg):
    get_data()

    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Parcheggio Piazza Vittoria')],
        [KeyboardButton(text='Ospedale Nord')],
        [KeyboardButton(text='Ospedale Sud')],
        [KeyboardButton(text='D\'Azeglio')],
        [KeyboardButton(text='Fossa Bagni')],
        [KeyboardButton(text='Randaccio')],
        [KeyboardButton(text='Piazza Mercato')],
        [KeyboardButton(text='Freccia Rossa')],
        [KeyboardButton(text='San Domenico')],
        [KeyboardButton(text='Benedetto Croce')],
        [KeyboardButton(text='Stazione')],
        [KeyboardButton(text='Palagiustizia')],
        [KeyboardButton(text='Crystal')],
        [KeyboardButton(text='Arnaldo Park')],
        [KeyboardButton(text='Casazza')],
        [KeyboardButton(text='S.Eufemia-Buffalora')],
        [KeyboardButton(text='Autosilo 1')],
        [KeyboardButton(text='Prealpino')],
        [KeyboardButton(text='Poliambulanza')],
        [KeyboardButton(text='Palaleonessa')],
        [KeyboardButton(text='Domus')],
        [KeyboardButton(text='Stadio')],
        [KeyboardButton(text='Ospedale Nord (superficie)')],
        [KeyboardButton(text='Ospedale Poliambulanza')],
    ], resize_keyboard=True)

    json_file = open("data.json", "r")
    parkings = json.load(json_file)

    message = 'Parcheggio non trovato'
    for park in parkings:
        if park['name'] == msg['text']:
            message = '&#x1F17F <b>Parcheggio:</b> ' + park['name'] + '\n\n&#x1F4CD <b>Indirizzo:</b> ' + park['address']
            if park['parking_spaces'] == 'n.a.':
                message += '\n\n&#x1F7E1 <b>Posti disponibili: </b> ' + park['parking_spaces'] + ' / ' + park['total_spaces']
            elif int(park['parking_spaces']) > (int(park['total_spaces']) / 100 * 20):
                message += '\n\n&#x1F7E2 <b>Posti disponibili: </b> ' + park['parking_spaces'] + ' / ' + park['total_spaces']
            elif int(park['parking_spaces']) == 0:
                message += '\n\n&#x1F534 <b>Posti disponibili: </b> ' + park['parking_spaces'] + ' / ' + park['total_spaces']
            else:
                message += '\n\n&#x1F7E1 <b>Posti disponibili: </b> ' + park['parking_spaces'] + ' / ' + park['total_spaces']

    bot.sendMessage(chat_id, message, reply_markup=keyboard, parse_mode='html')


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        bot.sendMessage(chat_id, msg)


def get_maps_link(park):
    address = ''
    if park == 'Parcheggio Piazza Vittoria':
        address = '<a href="https://goo.gl/maps/ApiEGmifftD6RCnL9">Piazza della Vittoria</a>'
    elif park == 'Ospedale Nord':
        address = '<a href="https://goo.gl/maps/5y6f8z4MJqb39xRg7">Piazza San Padre Pio da Pietrelcina, 1</a>'
    elif park == 'Ospedale Sud':
        address = '<a href="https://goo.gl/maps/yeE9rpffMeSFQsAK7">Via Ducco, angolo via dal Monte 44</a>'
    elif park == 'D\'Azeglio':
        address = '<a href="https://goo.gl/maps/QZGwL6tC8qQEqVFx7">Via Massimo D\'Azeglio, 4a</a>'
    elif park == 'Fossa Bagni':
        address = '<a href="https://goo.gl/maps/DSJLhYeqiqaF4hzT7">Piazza Fossa Bagni - Ingresso principale</a> | <a href="https://goo.gl/maps/yk1qhyXDuFmBb4KH6">Piazza Fossa Bagni - Ingresso secondario</a>'
    elif park == 'Randaccio':
        address = '<a href="https://goo.gl/maps/sS5X1Achz9zV6GFB9">Via Lupi di Toscana n 4</a>'
    elif park == 'Piazza Mercato':
        address = '<a href="https://goo.gl/maps/ssxLtQRdSZf9J5JU7">Piazza del Mercato</a>'
    elif park == 'Freccia Rossa':
        address = '<a href="https://goo.gl/maps/RfG5RXt9qkE15Fxm7">Viale Italia, 31</a>'
    elif park == 'San Domenico':
        address = '<a href="https://goo.gl/maps/BFfbkQyDHdsffv8x7">Piazza San Domenico</a>'
    elif park == 'Benedetto Croce':
        address = '<a href="https://goo.gl/maps/7sNwGRDgKHE2Zg5V8">Piazzetta Don L. Sturzo</a>'
    elif park == 'Stazione':
        address = '<a href="https://goo.gl/maps/XhuH6ZQk3nVB8UiB6">V.le Stazione, 51</a>'
    elif park == 'Palagiustizia':
        address = '<a href="https://goo.gl/maps/9agpaJGGYq1wgBZXA">Via Gambara, 44</a>'
    elif park == 'Crystal':
        address = '<a href="https://goo.gl/maps/MC8ZrLt8nyvxZAig6">Via Aldo Moro, 17</a>'
    elif park == 'Arnaldo Park':
        address = '<a href="https://goo.gl/maps/R7xXmCFB8Gr8J48j6">Piazzale Arnaldo</a>'
    elif park == 'Casazza':
        address = '<a href="https://goo.gl/maps/5fbyVYWS6aExoeuj6">Via Triumplina 181/02</a>'
    elif park == 'S.Eufemia-Buffalora':
        address = '<a href="https://goo.gl/maps/HJ3EvwLy41LmofqE7">Via Agostino Chiappa</a>'
    elif park == 'Autosilo 1':
        address = '<a href="https://goo.gl/maps/qPMkDPTBQ95FngQU7">Via Vittorio Emanuele II, 3</a>'
    elif park == 'Prealpino':
        address = '<a href="https://goo.gl/maps/ffCpbwo2m1kh6Btt5">Via Triumplina</a>'
    elif park == 'Poliambulanza':
        address = '<a href="https://goo.gl/maps/eEHAWfyChMupnZnY9">Via Morelli</a>'
    elif park == 'Palaleonessa':
        address = '<a href="https://goo.gl/maps/R3tf3YM3AH9CNUVV7">Via Caprera</a>'
    elif park == 'Domus':
        address = '<a href="https://goo.gl/maps/2bE4ZjXRr5A81Qr59">Via Lazzaretto</a>'
    elif park == 'Stadio':
        address = '<a href="https://goo.gl/maps/sSHrWBs2eFJQE2dY7">Via dello Stadio</a>'
    elif park == 'Ospedale Nord (superficie)':
        address = '<a href="https://goo.gl/maps/aBTWUN6u6aS1ZyhGA">Piazza San Padre Pio da Pietrelcina, 1</a>'
    elif park == 'Ospedale Poliambulanza':
        address = '<a href="https://goo.gl/maps/MpbPxFBvPqbKdzuX8">Via Leonida Bissolati</a>'

    return address


def get_data():
    url = "https://www.bresciamobilita.it/parking/parcheggi-in-struttura"

    html = urlopen(url).read().decode("utf-8")

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find("table", {"class": "bmtable table-condensed"})
    rows = table.find_all('tr')[1:]

    data = []

    for row in rows:
        name = row.find_all('td')[0].get_text().strip()
        address = get_maps_link(name)
        total_spaces = row.find_all('td')[2].get_text().strip()
        parking_spaces = row.find_all('td')[3].get_text().strip()

        data.append({"name": name, "address": address, "total_spaces": total_spaces, "parking_spaces": parking_spaces})

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, sort_keys=False)

config = configparser.ConfigParser()
config.read('config.ini')
bot = telepot.Bot(config["Parcheggi"]["bot_token"])
MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(1)

