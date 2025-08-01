from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime

app = Flask(__name__)
CORS(app)

# CSV file from GitHub
CSV_URL = "https://raw.githubusercontent.com/jphsu87/my-powerball-api/main/powerball_data.csv"

# Load the CSV once
df = pd.read_csv(CSV_URL)
df['draw_date'] = pd.to_datetime(df['draw_date'])

# Endpoint: Get latest winning numbers
@app.route('/latest', methods=['GET'])
def get_latest():
    latest_row = df.loc[df['draw_date'].idxmax()]
    return jsonify({
        "date": latest_row['draw_date'].strftime('%Y-%m-%d'),
        "numbers": [int(latest_row[f'number{i}']) for i in range(1, 6)],
        "powerball": int(latest_row['powerball'])
    })

# Endpoint: Get frequency of all numbers (including Powerball)
@app.route('/frequency', methods=['GET'])
def get_frequency():
    frequency = {}
    for _, row in df.iterrows():
        numbers = [int(row[f'number{i}']) for i in range(1, 6)]
        for num in numbers:
            frequency[num] = frequency.get(num, 0) + 1
        pb = int(row['powerball'])
        frequency[pb] = frequency.get(pb, 0) + 1  # Optional: include PB in same dict
    return jsonify(frequency)

# Endpoint: Get history within date range
@app.route('/history', methods=['GET'])
def get_history():
    start = request.args.get('start')
    end = request.args.get('end')

    try:
        start_date = pd.to_datetime(start) if start else df['draw_date'].min()
        end_date = pd.to_datetime(end) if end else df['draw_date'].max()
    except Exception as e:
        return jsonify({"error": f"Invalid date format: {e}"}), 400

    filtered = df[(df['draw_date'] >= start_date) & (df['draw_date'] <= end_date)].copy()
    filtered.sort_values(by='draw_date', ascending=False, inplace=True)

    results = []
    for _, row in filtered.iterrows():
        results.append({
            "date": row['draw_date'].strftime('%Y-%m-%d'),
            "numbers": [int(row[f'number{i}']) for i in range(1, 6)],
            "powerball": int(row['powerball'])
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)