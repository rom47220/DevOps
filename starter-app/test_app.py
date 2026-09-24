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
