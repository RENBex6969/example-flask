from flask import Flask, jsonify
import random
import string
import threading
import time
import requests

app = Flask(__name__)

random_string = None
webhook_url = "https://discord.com/api/webhooks/1258191407517143142/h5E0PAY9jiUf3pbShAf-Ju6o7gBwc-iLx5zh2NolFd3ozD2Mh7LHKFBs4x1GliDIONV6"

def generate_random_string():
    global random_string
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(16))
    send_webhook(random_string)
    threading.Timer(86400, generate_random_string).start()  # 86400 seconds = 24 hours

def send_webhook(random_string):
    data = {
        "embeds": [
            {
                "title": "New Random String Generated",
                "description": f"**{random_string}**",
                "color": 5814783  # This is a hex color code for the embed
            }
        ]
    }
    try:
        requests.post(webhook_url, json=data)
    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook: {e}")

@app.route('/')
def home():
    return jsonify({"string": random_string})

if __name__ == '__main__':
    generate_random_string()  # Initial call to start the cycle
    app.run(debug=True)
