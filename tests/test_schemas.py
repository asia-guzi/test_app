import pytest
from fastapi.testclient import TestClient
from main import app  # Zakładamy, że kod powyżej jest w pliku main.py


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker


client = TestClient(app)


def test_case_1_pass_answers():
    response = client.post(
        "/test_answers",
        json={
            "question_id": "Do you like FastAPI?",
            "response_id": "Yes"
        }
    )

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["your_answer"] == "Yes"

def test_case_2_pass_answers():
    response = client.post(
        "/test_answers",
        json={
            "question_id": "Do you like FastAPI?",
            "response_id": 3
        }
    )

    assert response.status_code == 400






# # Tworzenie testowej bazy danych SQLite w pamięci
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#

# # Dependency zamienione na testową sesję DB
# @pytest.fixture(scope="function")
# def test_db():
#     Base.metadata.create_all(bind=engine)  # Tworzy tabele w testowej bazie danych
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         Base.metadata.drop_all(bind=engine)  # Usuwa tabele po wykonaniu testów
#
# #
# # Integracja aplikacji z testową bazą zamiast prawdziwej
# @pytest.fixture(scope="function")
# def client(test_db):
#     def override_get_db():
#         yield test_db
#
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)
#     app.dependency_overrides.clear()


# # Test poprawnego POST
# def test_create_user(client):
#     # Tworzenie nowego użytkownika przez symulowanie POST
#     response = client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
#
#     # Sprawdzanie odpowiedzi serwera
#     assert response.status_code == 200
#     assert response.json() == {
#         "id": 1,
#         "name": "John Doe",
#         "email": "john@example.com"
#     }
#

