from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

@app.route("/")
def home():
    return jsonify({
        "message": "Flask Redis app is running...",
        "redis_host": REDIS_HOST
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "alive"
    }), 200

@app.route("/ready")
def ready():
    try:
        redis_client.ping()
        return jsonify({
            "status": "ready",
            "redis": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "not ready",
            "redis": "disconnected",
            "error": str(e)
        }), 500

@app.route("/count")
def count():
    try:
        count_value = redis_client.incr("visitor_count")
        return jsonify({
            "message": "Counter updated successfully",
            "count": count_value
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Redis connection failed",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
