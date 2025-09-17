from flask import Flask, request, jsonify
import csv
import datetime

app = Flask(__name__)

old_clients = {}
with open('old_clients.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        old_clients[row['clientID']] = row['carrier']


# Tells Flask that the funciton handles requests to /webhook URL
# Only accepts POST requests
@app.route("/webhook", methods=["POST"])
def webhook():
    # Gets the JSON payload sent by EZLynx (or simulated by me)
    data = request.get_json(force=True)

    client_id = data.get("clientId")
    carrier = data.get("carrier")
    label = data.get("label")

    # Check if the client exists in the old system
    if client_id in old_clients:
        # If they exist but now have a different carrier, flag as renewal
        if old_clients[client_id] != carrier:
            decision = "renewal (carrier changed)"
        else:
            decision = "renewal"
    else:
        decision = "new business"

    # Log result with timestamp
    timestamp = datetime.datetime.now().isoformat()
    print(f"{timestamp} - Client {client_id}: Original label = {label}, Classified = {decision}")

    return jsonify({"status": "received", "classification": decision}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
