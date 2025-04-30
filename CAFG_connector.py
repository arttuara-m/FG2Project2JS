from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/info')
def info():
    commands = "use, buy, check, work, move, info"
    return commands

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)