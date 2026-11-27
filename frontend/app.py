
from flask import Flask, render_template, request, jsonify
import urllib.request
import urllib.parse
import json
from urllib.error import HTTPError, URLError

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Please enter a comment."}), 400

    query = urllib.parse.urlencode({"text": text})

    url  = f"https://multilingual-sentiment-analysis-api.onrender.com/make_prediction?{query}"
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        return jsonify(result)

    except HTTPError as e:
        return jsonify({
            "error": f"Backend API returned HTTP {e.code}"
        }), 502

    except URLError:
        return jsonify({
            "error": "Cannot connect to backend API. Make sure api.py is running on port 5000."
        }), 502

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )
