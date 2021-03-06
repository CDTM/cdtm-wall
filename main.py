# app.py
import time
import gevent.monkey
import os

gevent.monkey.patch_all()
from flask import Flask, send_from_directory, jsonify, request
from flask_socketio import SocketIO

from mvg import get_departures
from owncloud import get_photos
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)

socketio = SocketIO(app)

# Define the static directory
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')


@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return send_from_directory(static_file_dir, 'index.html')


@app.route("/api/mvg/<int:station>")
def rest_get_mvg(station):
    response = dict()
    walking_distance = request.args.get('walking_distance', default=8)
    # hauptbahnhof is station with id 6
    response["mvg"] = get_departures(station, walking_distance)
    # return response
    return jsonify(response)


@app.route("/api/photos")
def rest_get_photos():
    response = dict()
    response["photos"] = get_photos()
    return jsonify(response)


@app.route("/api/welcome")
def rest_post_welcome():
    socket_welcome_emit("Sebastian")
    return ('', 204)


def socket_welcome_emit(name):
    response = dict()
    response['message'] = "Welcome " + name
    socketio.emit('welcome', response, json=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5003, host='0.0.0.0')
