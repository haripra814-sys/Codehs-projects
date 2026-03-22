from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/air_quality')
def air_quality():
    return render_template('air_quality.html')

@app.route('/food_tips')
def food_tips():
    return render_template('food_tips.html')

@app.route('/body_signals')
def body_signals():
    return render_template('body_signals.html')

@app.route('/api/air_quality')
def api_air_quality():
    # Placeholder for MQ-135 data integration
    # Later: read from CSV or serial connection to Arduino
    data = {"status": "good", "suggestion": "All clear!"}
    return jsonify(data)

@app.route('/api/food_tips')
def api_food_tips():
    # Placeholder for nutrition/spoilage data
    data = {"item": "Apples", "tip": "Store in the fridge to slow ripening."}
    return jsonify(data)

@app.route('/api/circadian_rhythm')
def api_circadian_rhythm():
    # Placeholder for biometrics data
    data = {"time": "8 AM", "bio_state": "Peak alertness."}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)