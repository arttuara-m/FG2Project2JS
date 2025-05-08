import mysql.connector
from flask_cors import CORS
from flask import Flask, request

import EventHandler
import CAFG_variables as gloVar
from EventHandler import actioncheck, nearbyairports, updatecoords, flyToAirport

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
    list = actioncheck()
    list.pop(-1)
    return list

@app.route('/checkitem/<item>')
def checkitem(item):
    list = actioncheck()
    list.pop(0)
    list.pop(0)
    return list


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

@app.route('/checkmoves')
def checkmoves():
    if gloVar.time_units > 0:
        return [True, gloVar.time_units]
    else:
        return [False, gloVar.time_units]

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
    current_coordinates = updatecoords()
    print(f'Fetched latitude and longitude: {current_coordinates[0]} {current_coordinates[1]}')
    return [current_coordinates]

@app.route('/availableairports')
def availableairports():
    nearby_airports= nearbyairports(gloVar.travel_range_km)
    return [
        nearby_airports
    ]
@app.route('/move')
def move():
    airport_buttons = nearbyairports(gloVar.travel_range_km)
    return airport_buttons

@app.route('/moveto/<location>')
def gotoairport(location):
    flyToAirport(location)
    return ["moving to airport:"]

@app.route('/doevent')
def doevent():
    event = EventHandler.eventhandlersub()
    return [event]

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
