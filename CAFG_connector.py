
from flask_cors import CORS
from flask import Flask, request

import EventHandler
import CAFG_variables as gloVar

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/info')
def info():
    return [EventHandler.actionhandlersub("info")]


@app.route('/buy')
def buy():
    return [EventHandler.actionhandlersub("buy")]

@app.route('/status')
def status():
    return [str(gloVar.current_score), str(gloVar.player_money),
            str(gloVar.current_country), str(gloVar.global_threat),
            str(gloVar.local_threat[gloVar.current_country])]

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
