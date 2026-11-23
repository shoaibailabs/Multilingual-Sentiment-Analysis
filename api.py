from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import json
import os

app = Flask(__name__)

# Project folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load TensorFlow model
MODEL_PATH = os.path.join(
    BASE_DIR, "sentiment_model_tf", "sentiment_model_compatible.keras"
)

model = tf.keras.models.load_model(MODEL_PATH,compile=False)

# Load sentiment labels
CLASS_PATH = os.path.join(
    BASE_DIR, "sentiment_model_tf", "class_names.json"
)

with open(CLASS_PATH, 'r', encoding='utf-8') as file:
    class_names = json.load(file)


@app.route("/", methods=["GET"])
def hello():
    return "Sentiment Analysis API is running!"


@app.route("/make_prediction", methods=["GET"])
def prediction():

    message = request.args.get("text", "")

    if not message.strip():
        return jsonify({
            "error": "Please provide a text message"
        }), 400

    message = message.strip()

    # Make prediction
    result = model(
        tf.constant([message], dtype=tf.string),
        training=False
    ).numpy()[0]

    predicted_id = int(np.argmax(result))

    sentiment = class_names[predicted_id]

    confidence = float(result[predicted_id]) * 100

    return jsonify({
        "input": message,
        "sentiment": sentiment,
        "confidence": round(confidence, 2)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))