import mysql.connector
from flask_cors import CORS
from flask import Flask, request

import EventHandler
import CAFG_variables as gloVar
from EventHandler import actioncheck, nearbyairports

"""
conn = mysql.connector.connect(
    host="localhost",
    user="surviver",
    password="123",
    database="flight_game",
    charset="latin1",
    collation="latin1_swedish_ci",
)
"""

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/info')
def info():
    return [EventHandler.listcommands()]

@app.route('/use')
def use():
    return EventHandler.actionuse()

@app.route('/useitem/<item>')
def useitem(item):
    return EventHandler.actionusesub(item)

@app.route('/buy')
def buy():
    return EventHandler.actionbuy()

@app.route('/buyitem/<item>')
def buyitem(item):
    return EventHandler.buythis(item)

@app.route('/work')
def work():
    return EventHandler.actionwork()

@app.route('/workitem/<item>')
def workitem(item):
    return [EventHandler.actionworksub(item)]

@app.route('/check')
def check():
    return [actioncheck()]

@app.route('/status')
def status():
    return [str(gloVar.current_score), str(gloVar.player_money),
            str(gloVar.time_units), str(gloVar.current_airport),
            str(gloVar.global_threat),
            str(gloVar.local_threat[gloVar.current_airport])]

@app.route('/turnupdate')
def turnupdate():
    EventHandler.timeunitrefresher(10)
    EventHandler.shoprandomiser(3)
    return "turn refreshed successfully"

@app.route('/resetgame')
def resetgame():
    gloVar.current_score = 0
    gloVar.global_threat = 0
    gloVar.shop_items = []
    gloVar.time_units = 10
    gloVar.player_money = 1000
    gloVar.player_luck = 0
    gloVar.player_items = []
    gloVar.previous_travel_distance = 0
    gloVar.current_airport = "AGGH"
    gloVar.local_threat = {gloVar.current_airport: 0}
    gloVar.global_country_index = 0
    return "Game reseted"

@app.route('/updatemap')
def updatemap():
    conn = mysql.connector.connect(
        host="localhost",
        user="surviver",
        password="123",
        database="flight_game",
        charset="latin1",
        collation="latin1_swedish_ci",
    )

    if not conn.is_connected():
        conn.reconnect()

    cursor = conn.cursor()
    cursor.execute(""
                   "SELECT latitude_deg FROM airport WHERE gps_code = 'AGGH';")
    player_y = cursor.fetchall()
    cursor.execute(""
                   "SELECT longitude_deg FROM airport WHERE gps_code = 'AGGH';")
    player_x = cursor.fetchall()
    return [float(player_x),float(player_y)]

@app.route('/move')
def availableairports():
    nearby_airports= nearbyairports(gloVar.travel_range_km)
    return [
        nearby_airports
    ]

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
