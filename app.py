from flask import Flask, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for the extension

# Simulated Powerball historical data (format: date, white balls, powerball)
powerball_data = [
    {"date": "2025-01-01", "numbers": [3, 12, 23, 45, 67], "powerball": 15},
    {"date": "2025-02-01", "numbers": [5, 19, 28, 39, 61], "powerball": 7},
    {"date": "2025-03-01", "numbers": [1, 14, 25, 36, 58], "powerball": 22},
    {"date": "2025-04-01", "numbers": [9, 17, 33, 44, 66], "powerball": 3},
    {"date": "2025-07-01", "numbers": [4, 13, 27, 42, 59], "powerball": 19},
    {"date": "2025-07-28", "numbers": [2, 11, 24, 38, 55], "powerball": 10}  # Today’s simulated draw
]

# Endpoint for latest winning numbers
@app.route('/latest', methods=['GET'])
def get_latest():
    latest_date = max(data["date"] for data in powerball_data)
    latest_draw = next(data for data in powerball_data if data["date"] == latest_date)
    return jsonify(latest_draw)

# Endpoint for historical number frequency
@app.route('/frequency', methods=['GET'])
def get_frequency():
    frequency = {}
    for draw in powerball_data:
        for num in draw["numbers"]:
            frequency[num] = frequency.get(num, 0) + 1
        frequency[draw["powerball"]] = frequency.get(draw["powerball"], 0) + 1
    return jsonify(frequency)

# Endpoint for filtered data by date range
@app.route('/history', methods=['GET'])
def get_history():
    start_date = request.args.get('start', '2025-01-01')
    end_date = request.args.get('end', datetime.datetime.now().strftime('%Y-%m-%d'))
    filtered_data = [draw for draw in powerball_data if start_date <= draw["date"] <= end_date]
    return jsonify({"draws": filtered_data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)