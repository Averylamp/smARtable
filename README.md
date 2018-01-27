# smARtable: a smart table project

CALIBRATION
run python app.py
run sh calibrate_window
run python3 calibration.py
Click the points as they appear on the screen in the correct order: 0 to 3. Press f to refresh the picture. Press 'q' to cancel. Homography results will be saved in the pickle file specified in settings.json.

TESTING
webcam_display.py
This is a simple script to test out camera pixel width/height settings. It also shows allows you to experiment with which input port the camera is on. After finding a good result, you can update the settings.json file.

VISION_API
camera_api.py
This contains a camera class that can locate where images are with some model. It can then use the homography to map it to the correct place on the screen.

INFORMATION
information_class.py
Used to take a topic/item and grab pertinent information. This will then be used by some sort of drawing protocall to place information in a good location.

MAIN FILE
app.py
This needs to run before anything else. It launches the Flask server.


Fullscreen mode
press CMD+CTL+f to toggle between full screen on chrome
