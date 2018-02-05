import os, sys, inspect, thread, time, json

from socketIO_client import SocketIO, LoggingNamespace

src_dir  = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

# install_name_tool -change /Library/Frameworks/Python.framework/Versions/2.7/Python /usr/local/Cellar/python/2.7.14_2/Frameworks/Python.framework/Versions/2.7/lib/libpython2.7.dylib /Users/matthew/Dropbox\ \(MIT\)/Developer/Projects/smARt\ Table/LeapMotion/lib/LeapPython.so
import Leap
from Leap import KeyTapGesture, SwipeGesture

socketIO = SocketIO('localhost', 8000)
leap_namespace = socketIO.define(LoggingNamespace, '/leap')

def cursor_update(position):
    # print("[TableListener] Cursor Update: %s at %s" % (position, direction))
    data = {}
    data['x'] = position[0]
    data['y'] = position[1]
    json_data = json.dumps(data)
    leap_namespace.emit('cursor_update', json_data)

def cursor_click(position):
    print("[TableListener] Cursor Click: %s at %s", position)
    data = {}
    data['x'] = position[0]
    data['y'] = position[1]
    json_data = json.dumps(data)
    leap_namespace.emit('cursor_click', json_data)

def clear():
    print("[TableListener] Clear")
    leap_namespace.emit('clear', '')

class TableListener(Leap.Listener):
    def on_init(self, controller):
        print "[TableListener] Initialized"

    def on_connect(self, controller):
        print "[TableListener] Controller connected"

        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_disconnect(self, controller):
        print "[TableListener] Controller Disconnected"

    def on_exit(self, controller):
        print "[TableListener] Exited"

    def on_frame(self, controller):
        frame = controller.frame()
        pointables = frame.fingers.extended()

        if len(pointables) == 1:
            location = pointables.frontmost.stabilized_tip_position

            iBox = frame.interaction_box
            normalizedLocation = iBox.normalize_point(location, False)

            x = normalizedLocation.x * 1920
            y = (1 - normalizedLocation.z) * 1080

            cursor_update((x, y))

            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                    cursor_click((x, y))

        elif len(pointables) >= 4 :
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    if swipe.state == 3:
                        clear()

def main():
    tableListener = TableListener()
    controller = Leap.Controller()

    controller.add_listener(tableListener)
    socketIO.wait()

if __name__ == "__main__":
    main()
