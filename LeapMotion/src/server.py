import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template

sio = socketio.Server()
app = Flask(__name__)

@sio.on('connect', namespace='/leap')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('cursor_update', namespace='/leap')
def message(sid, data):
    print("[LeapNamespace] cursor_update ", data)

@sio.on('cursor_click', namespace='/leap')
def message(sid, data):
    print("[LeapNamespace] cursor_click ", data)

@sio.on('clear', namespace='/leap')
def message(sid, data):
    print("[LeapNamespace] clear ")

@sio.on('disconnect', namespace='/leap')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    app = socketio.Middleware(sio, app)

    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
