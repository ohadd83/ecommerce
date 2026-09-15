from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_products():

    response = client.get("/products/")

    assert response.status_code == 200

    products = response.json()

    assert len(products) > 0


def test_get_product():

    response = client.get("/products/1")

    assert response.status_code == 200

    product = response.json()

    assert product["name"] == "Laptop"


def test_product_not_found():

    response = client.get("/products/999")

    assert response.status_code == 200

    assert response.json()["error"] == "Product not found"
