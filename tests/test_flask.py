from flask_app import app

def test_get_root_returns_200() -> None:
    with app.test_client() as client:
        response = client.get("/")
    assert response.status_code == 200
