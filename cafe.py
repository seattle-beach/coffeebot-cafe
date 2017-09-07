import os
from flask import Flask, request, jsonify

app = Flask(__name__)

EMPTY_POT_GRAMS = 1800
FULL_POT_GRAMS = 3300

devices = {}
allStates = [
            {
                "devId": "Homer",
                "status": "BREWING",
                "level": 75
            },
            {
                "devId": "Marge",
                "status": "AVAILABLE",
                "level": 0
            },
            {
                "devId": "Maggie",
                "status": "AVAILABLE",
                "level": 50
            },
            {
                "devId": "Lisa",
                "status": "AVAILABLE",
                "level": 100
            },
            {
                "devId": "Bart",
                "status": "UNAVAILABLE",
                "level": None
            }
        ]

@app.route('/')
def hello():
    return "Not that kind of java..."

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/report', methods=['POST'])
def report():
    json_data = request.get_json(force=True)
    global devices
    devices[json_data["devId"]] = json_data["qty"]
    return "", 200

@app.route('/allstates')
def allstates():
    return jsonify(allStates)

@app.route('/status')
def status():
    devFormatted = []
    for devId, qty in devices.items():
        devLevel = (qty - EMPTY_POT_GRAMS)/(FULL_POT_GRAMS - EMPTY_POT_GRAMS)
        devLevel = round(devLevel * 100, 0)
        devLevel = min(max(devLevel, 0), 100)
        devStatus = "AVAILABLE" if (devLevel > 0) else "UNAVAILABLE"
        devFormatted.append({
            "devId": devId,
            "status": devStatus,
            "level": devLevel
        })
    return jsonify(devFormatted)

# run app
if __name__ == "__main__":
    if os.environ.get('VCAP_SERVICES') is None: # running locally
        PORT = 5000
        DEBUG = True
    else:                                       # running on CF
        PORT = int(os.getenv("PORT"))
        DEBUG = False

    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)