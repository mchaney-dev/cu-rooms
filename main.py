from backend.driver import Driver
import flask
import json

driver = Driver(verbose=True)
app = flask.Flask('CU Rooms')

@app.route("/")
def home():
    return "Home"

@app.route("/rooms", methods=["GET"])
def get_rooms():
    return json.dumps(driver.get_rooms())

@app.route("/events", methods=["GET"])
def get_events():
    return json.dumps(driver.get_events())

if __name__ == '__main__':
    app.run("localhost", 5000)