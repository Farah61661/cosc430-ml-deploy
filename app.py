# flask app for prediction

from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# load the saved model
model = joblib.load("model.pkl")


# simple health check to see if the app is running
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# main endpoint for predictions
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # check if request has data
        if data is None:
            return jsonify({"error": "No JSON data received"}), 400

        # check if X exists in request
        if "X" not in data:
            return jsonify({"error": "Missing 'X' key"}), 400

        X = data["X"]

        # check if X is in correct format
        if not isinstance(X, list):
            return jsonify({"error": "'X' must be a list"}), 400

        # make predictions
        predictions = model.predict(X)

        # return results as json
        return jsonify({"y": predictions.tolist()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# run the app locally
if __name__ == "__main__":
    app.run(debug=True)
