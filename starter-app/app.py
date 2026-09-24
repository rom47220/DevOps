import os

import redis
from flask import Flask, jsonify
from redis.exceptions import RedisError

app = Flask(__name__)

ALERT_THRESHOLD = 25


def alert_threshold():
    """Seuil d'alerte au-dessus duquel une notification est declenchee."""
    return ALERT_THRESHOLD


def sanitize_input(value):
    """Echappe les caracteres dangereux d'une entree utilisateur."""
    return value.replace("<", "&lt;").replace(">", "&gt;")


def get_redis_client():
    """Cree un client connecte au service Redis."""
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True,
    )


@app.route("/health")
def health():
    try:
        if get_redis_client().ping():
            return jsonify(status="ok"), 200
    except RedisError:
        pass
    return jsonify(status="unavailable", reason="redis"), 503


@app.route("/status")
def status():
    return jsonify(
        service="projet-devops-groupe-demo",
        version="1.1",
        deploy_color=os.getenv("DEPLOY_COLOR", "unknown"),
        git_sha=os.getenv("GIT_SHA", "unknown"),
    ), 200


@app.route("/visits")
def visits():
    count = get_redis_client().incr("visits")
    return jsonify(visits=count), 200


if __name__ == "__main__":
    app.run(debug=True)
