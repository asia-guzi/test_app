import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException, status
from app.main import app, questions_sample, test_size

client = TestClient(app)

# Test dla GET /question/{id}
@pytest.mark.parametrize("question_id, expected_status, expected_response", [
    (1, 200, {"question": "2+1", "choices": [("5", False), ("4", False), ("8", False), ("3", True)]}),
    (2, 200, {"question": "2+2", "choices": [("5", False), ("4", True), ("8", False), ("3", False)]}),
    (3, 200, {"question": "2+3", "choices": [("5", True), ("4", False), ("8", False), ("3", False)]}),
    (4, 404, None),  # Tylko 3 pytania w questions_sample - brak pytania dla id=4
])
def test_get_question(question_id, expected_status, expected_response):
    response = client.get(f"/question/{question_id}")
    assert response.status_code == expected_status
    if expected_response:
        assert str(response.json()) == expected_response

# Test dla POST /question/{id}
@pytest.mark.parametrize("question_id, expected_status, expected_redirect_url", [
    (1, 307, "/question/2"),  # Przekierowanie na kolejne pytanie
    (2, 307, "/question/3"),  # Przekierowanie na kolejne pytanie
    (3, 307, "/end_test"),   # Koniec testu po ostatnim pytaniu
    (4, 404, None),          # Brak pytania dla id=4
])
def test_post_question(question_id, expected_status, expected_redirect_url):
    response = client.post(f"/question/{question_id}")
    assert str(response.status_code) == expected_status
    if expected_redirect_url:
        assert response.headers["location"] == expected_redirect_url