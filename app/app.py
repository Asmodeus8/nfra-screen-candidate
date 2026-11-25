import os
import socket

import redis
from flask import Flask, jsonify, render_template

app = Flask(__name__)
client = redis.from_url(
    os.environ.get("REDIS_SERVER", "redis://localhost:6379"), decode_responses=True
)
KEY = "visits"
HOST = socket.gethostname()


def unavailable():
    return jsonify(error="redis unavailable"), 503


@app.route("/")
def index():
    try:
        visits = client.incr(KEY)
    except redis.exceptions.ConnectionError:
        return render_template("index.html", visits=None, host=HOST), 503
    return render_template("index.html", visits=visits, host=HOST)


@app.get("/api/visits")
def get_visits():
    try:
        return jsonify(visits=int(client.get(KEY) or 0))
    except redis.exceptions.ConnectionError:
        return unavailable()


@app.post("/api/visits")
def add_visit():
    try:
        return jsonify(visits=client.incr(KEY))
    except redis.exceptions.ConnectionError:
        return unavailable()


@app.get("/health")
def health():
    try:
        client.ping()
    except redis.exceptions.ConnectionError:
        return jsonify(status="redis unreachable"), 503
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("BINDING_ADDRESS", "0.0.0.0"),
        port=int(os.environ.get("SERVER_PORT", "8081")),
    )
