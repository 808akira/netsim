from flask import Flask, render_template, jsonify, request
import os, requests

app = Flask(__name__)

BACKEND_URL = "http://web-app-samy-private.azurewebsites.net"
TIMEOUT = 30


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/backend-status")
def backend_status():
    try:
        r = requests.get(f"{BACKEND_URL}/status", timeout=5)
        return jsonify({"reachable": True, "data": r.json()})
    except Exception as e:
        return jsonify({"reachable": False, "error": str(e)})


@app.route("/api/metrics")
def metrics():
    try:
        r = requests.get(f"{BACKEND_URL}/metrics", timeout=5)
        return jsonify({"ok": True, "data": r.json()})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


@app.route("/api/simulate", methods=["POST"])
def simulate():
    try:
        payload = request.get_json(silent=True) or {}
        r = requests.post(f"{BACKEND_URL}/simulate", json=payload, timeout=TIMEOUT)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/jobs/<job_id>")
def job_status(job_id):
    try:
        r = requests.get(f"{BACKEND_URL}/jobs/{job_id}", timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
