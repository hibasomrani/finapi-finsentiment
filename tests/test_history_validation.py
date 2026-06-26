"""Tests de validation des parametres de /history."""


def test_invalid_days(client):
    response = client.get("/history/AAPL?days=abc")
    assert response.status_code == 400
    data = response.get_json()
    assert data["code"] == 400
    assert "entier" in data["error"]


def test_days_out_of_range(client):
    response = client.get("/history/AAPL?days=999")
    assert response.status_code == 400
    data = response.get_json()
    assert data["code"] == 400
    assert "365" in data["error"]


def test_days_negative(client):
    response = client.get("/history/AAPL?days=-5")
    assert response.status_code == 400


def test_days_zero(client):
    response = client.get("/history/AAPL?days=0")
    assert response.status_code == 400
