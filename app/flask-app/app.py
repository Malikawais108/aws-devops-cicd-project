from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

@app.route("/")
def index():
    hostname = socket.gethostname()
    env = os.getenv("ENV", "dev")

    return jsonify(
        message="CI/CD DevOps demo app running",
        hostname=hostname,
        environment=env
    )

@app.route("/health")
def health_check():
    return jsonify(status="UP")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

