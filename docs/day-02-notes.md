Day 2 – Flask App + Docker

Date: 18 Dec 2025
Objective: Create a working Flask app, containerize it, understand Docker internals.

1️⃣ Flask Application

File: app/flask-app/app.py

Routes:

/ → returns message, hostname, environment

/health → returns status UP

Environment variable: ENV defaults to dev


Code snippet:

from flask import Flask, jsonify
import socket, os

app = Flask(__name__)

@app.route("/")
def index():
    hostname = socket.gethostname()
    env = os.getenv("ENV", "dev")
    return jsonify(message="CI/CD DevOps demo app running", hostname=hostname, environment=env)

@app.route("/health")
def health_check():
    return jsonify(status="UP")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


2️⃣ Dockerfile

FROM python:3.11-slim
WORKDIR /app
COPY app/flask-app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/flask-app/ .
EXPOSE 5000
CMD ["python", "app.py"]

Build & run:

docker build -t flask-devops-app -f docker/Dockerfile .
docker run -d -p 5000:5000 --name flask-app flask-devops-app




Key Learnings (Interview Mode)
Concept	Explanation
WORKDIR	Sets default directory in container. Docker creates it if missing.
0.0.0.0	Allows Flask to listen on all interfaces so host can access it.
RUN vs CMD	RUN → executes at build-time (creates image layers)
CMD → executes at container start (runtime)
Container Start Flow	1. Docker creates container from image
2. Sets WORKDIR
3. Executes CMD
4. Flask app starts
5. Accessible via mapped port



4️⃣ Troubleshooting Notes

Docker build context must include all app files

Always build from project root

.dockerignore not yet used but should be in future

5️⃣ Status ✅

Flask app running locally

Docker container running

Debugging build context learned

Interview answers prepared






























