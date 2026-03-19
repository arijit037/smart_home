from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

def smart_home_ai(temp, motion, time_mode):
    result = {
        "ac": "OFF",
        "heater": "OFF",
        "light": "OFF",
        "security": "SAFE"
    }

    #  Temperature 
    if temp > 30:
        result["ac"] = "ON"
    elif temp < 15:
        result["heater"] = "ON"

    #  Time Logic
    hour = datetime.now().hour

    if time_mode == "auto":
        night = (hour >= 18 or hour <= 6)
    elif time_mode == "night":
        night = True
    else:
        night = False

    # Motion Logic
    if motion == "yes":
        if night:
            result["light"] = "ON"
        result["security"] = "ALERT"

    return result


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/smart', methods=['POST'])
def smart():
    data = request.get_json()

    temp = float(data['temperature'])
    motion = data['motion']
    time_mode = data['time']

    result = smart_home_ai(temp, motion, time_mode)

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)