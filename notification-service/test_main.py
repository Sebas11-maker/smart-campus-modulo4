import sys
from unittest.mock import MagicMock

sys.modules['confluent_kafka'] = MagicMock()
sys.modules['kafka'] = MagicMock()

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main_frontend_notification():
    response = client.get("/")
    assert response.status_code == 200
    assert "Notification Microservice" in response.text