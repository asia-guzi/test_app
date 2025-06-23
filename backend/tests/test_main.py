from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app)


def test_index():
    response = client.get(f"/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Welcome to a test , after you log in there is 30 min to fulfill the test "
    }
