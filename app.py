from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Define occupation factors
    occupation_factors = {
        'manager': 0.0,
        'sales representative': 1.0,
        'salesperson': 0.8,
        'nurse': 0.7,
        'teacher': 0.6,
        'scientist': 0.5,
        'software engineer': 0.4,
        'accountant': 0.4,
        'lawyer': 0.2,
        'doctor': 0.2,
        'engineer': 0.2
    }
    occupation_factor = occupation_factors.get(data['occupation'].lower(), 1.0)
    try:
        age_factor = 1.5 if data['age'] > 30 else 1.0
        sleep_factor = 1.2 if data['sleepDuration'] >= 7 else 0.8
        bp_factor = 0.9 if data['bloodPressure'] < 120 else 1.5

        # Calculate prediction score including the occupation factor
        prediction_score = (data['weight'] / data['height']) * age_factor * sleep_factor * bp_factor * occupation_factor
        prediction = "Healthy" if prediction_score < 0.5 else "At Risk"

        return jsonify({
            "success": True,
            "prediction": prediction
        })
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
