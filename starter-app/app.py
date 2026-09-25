import os
import time

import redis
from flask import Flask, Response, g, jsonify, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)
from redis.exceptions import RedisError

app = Flask(__name__)

ALERT_THRESHOLD = 25

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Nombre total de requetes HTTP recues",
    ["method", "endpoint", "status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "Duree de traitement des requetes HTTP",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)


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


@app.before_request
def start_timer():
    """Capture l'instant de debut avant le traitement de la requete."""
    g.request_start_time = time.perf_counter()


@app.after_request
def observe_request(response):
    """Enregistre duree + compteur apres chaque requete, sauf /metrics."""
    if request.path != "/metrics":
        endpoint = request.url_rule.rule if request.url_rule else request.path
        method = request.method
        status = str(response.status_code)

        HTTP_REQUESTS_TOTAL.labels(
            method=method,
            endpoint=endpoint,
            status=status,
        ).inc()

        start = getattr(g, "request_start_time", None)
        if start is not None:
            duration = time.perf_counter() - start
            HTTP_REQUEST_DURATION_SECONDS.labels(
                method=method,
                endpoint=endpoint,
            ).observe(duration)

    return response


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


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
        version="1.0",
        deploy_color=os.getenv("DEPLOY_COLOR", "unknown"),
        git_sha=os.getenv("GIT_SHA", "unknown"),
    ), 200


@app.route("/visits")
def visits():
    count = get_redis_client().incr("visits")
    return jsonify(visits=count), 200


@app.route("/simulate-error")
def simulate_error():
    """Endpoint volontairement en erreur pour tester les alertes plus tard."""
    return jsonify(error="simulated failure"), 500


if __name__ == "__main__":
    app.run(debug=True)
