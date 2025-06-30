from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

STATE_FILE = "bot_state.json"

# Initialize default state if not present
default_state = {
    "bot_active": True,
    "stop_after_sell": False,
    "trade_amount": 100
}

if not os.path.exists(STATE_FILE):
    with open(STATE_FILE, "w") as f:
        json.dump(default_state, f)

def load_state():
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

@app.route("/state", methods=["GET"])
def get_state():
    state = load_state()
    return jsonify(state)

@app.route("/state", methods=["POST"])
def update_state():
    state = load_state()
    data = request.json or {}

    if "bot_active" in data:
        state["bot_active"] = bool(data["bot_active"])

    if "stop_after_sell" in data:
        state["stop_after_sell"] = bool(data["stop_after_sell"])

    if "trade_amount" in data:
        try:
            state["trade_amount"] = max(1, float(data["trade_amount"]))
        except ValueError:
            return jsonify({"error": "Invalid trade amount"}), 400

    save_state(state)
    return jsonify({"status": "updated", "new_state": state})

@app.route("/", methods=["GET"])
def home():
    return "Trading Bot Control API is live."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))