import os, json
from flask import Flask, render_template


dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/config/settings.json", "r") as f:
    json_settings = json.load(f)

# get the screen height and width
SCREEN_WIDTH = json_settings["screen_settings"]["width"]
SCREEN_HEIGHT = json_settings["screen_settings"]["height"]
TARGET_SIZE = json_settings["screen_settings"]["target_size"]

app = Flask(__name__)

# this is the main display
@app.route('/')
def main():
    return render_template('index.html',
                            screen_width=SCREEN_WIDTH,
                            screen_height=SCREEN_HEIGHT)

# calibrate is functional
@app.route('/calibrate/')
def calibrate():
    # relead on a refresh because this potentially takes fine tuning
    with open(dir_path + "/config/settings.json", "r") as f:
        json_settings = json.load(f)

    # get the screen height and width
    SCREEN_WIDTH = json_settings["screen_settings"]["width"]
    SCREEN_HEIGHT = json_settings["screen_settings"]["height"]
    TARGET_SIZE = json_settings["screen_settings"]["target_size"]

    return render_template('calibrate.html',
                            screen_width=SCREEN_WIDTH,
                            screen_height=SCREEN_HEIGHT,
                            target_size=TARGET_SIZE)

if __name__ == '__main__':
    app.run(debug=True)
