from unittest.mock import MagicMock, patch

from redis.exceptions import RedisError

from app import alert_threshold, sanitize_input, app


def test_alert_threshold():
    assert alert_threshold() == 25


def test_sanitize_input_escapes_html():
    assert sanitize_input("<script>") == "&lt;script&gt;"


def test_health_endpoint_ok():
    mock_client = MagicMock()
    mock_client.ping.return_value = True
    with patch("app.get_redis_client", return_value=mock_client):
        client = app.test_client()
        response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_health_endpoint_redis_down():
    mock_client = MagicMock()
    mock_client.ping.side_effect = RedisError("redis down")
    with patch("app.get_redis_client", return_value=mock_client):
        client = app.test_client()
        response = client.get("/health")
    assert response.status_code == 503
    assert response.get_json()["status"] == "unavailable"


def test_status_endpoint():
    client = app.test_client()
    response = client.get("/status")
    assert response.status_code == 200
    body = response.get_json()
    assert body["service"] == "projet-devops-groupe-demo"
    assert "deploy_color" in body
    assert "git_sha" in body


def test_metrics_endpoint_exposes_counter():
    client = app.test_client()
    client.get("/status")
    response = client.get("/metrics")
    assert response.status_code == 200
    body = response.data.decode("utf-8")
    assert "http_requests_total" in body
    assert 'endpoint="/status"' in body


def test_metrics_endpoint_exposes_histogram():
    client = app.test_client()
    client.get("/status")
    response = client.get("/metrics")
    body = response.data.decode("utf-8")
    assert "http_request_duration_seconds_bucket" in body
    assert "http_request_duration_seconds_count" in body
    assert "http_request_duration_seconds_sum" in body


def test_simulate_error_endpoint():
    client = app.test_client()
    response = client.get("/simulate-error")
    assert response.status_code == 500
    assert response.get_json()["error"] == "simulated failure"
