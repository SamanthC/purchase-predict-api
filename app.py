import pandas as pd
from flask import Flask, request, jsonify
from flask.logging import default_handler
from src.model import Model
import logging
import google.cloud.logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler

app = Flask(__name__)

logging_client = google.cloud.logging.Client()
cloud_handler = CloudLoggingHandler(logging_client, name="purchase-predict-api")

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(cloud_handler)
LOGGER.addHandler(default_handler)

model = Model()

@app.route("/", methods=["GET"])
def home():
	LOGGER.info("OK!!!!")
	return "OK!!!!", 200


@app.route("/auth", methods=["POST"])
def auth():
	body=request.get_json()
	if body and body.get("password", "") == "blent":
		token = generate_token()
		return jsonify({"token": token}), 200
	else:
		return jsonify({"error": "mot de passe invalide"}), 403

@app.route("/predict",  methods=["POST"])
@require_authentication
def predict():
	body = request.get_json()
	df = pd.read_json(body)
	LOGGER.info("Predicting fot DataFrame of shape {}".format(df.shape))
	results = [int(x) for x in model.predict(df).flatten()]
	return jsonify(results), 200

if __name__ == "__main__":
	app.run()