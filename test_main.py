import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

import main
from main import Item, ItemCreate, ItemUpdate, app


@pytest.fixture(autouse=True)
def reset_store():
    main.items.clear()
    main.next_id = 1
    yield
    main.items.clear()
    main.next_id = 1


@pytest.fixture
def client():
    return TestClient(app)


class TestModels:
    def test_item_create_accepts_name(self):
        item = ItemCreate(name="Widget")
        assert item.name == "Widget"

    def test_item_create_rejects_empty_body(self):
        with pytest.raises(ValidationError):
            ItemCreate()

    def test_item_model(self):
        item = Item(id=1, name="Widget")
        assert item.id == 1
        assert item.name == "Widget"

    def test_item_update_accepts_name(self):
        item = ItemUpdate(name="Updated")
        assert item.name == "Updated"


class TestHealth:
    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestListItems:
    def test_list_items_empty(self, client):
        response = client.get("/items")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_items_returns_all_items(self, client):
        client.post("/items", json={"name": "Alpha"})
        client.post("/items", json={"name": "Beta"})

        response = client.get("/items")

        assert response.status_code == 200
        assert response.json() == [
            {"id": 1, "name": "Alpha"},
            {"id": 2, "name": "Beta"},
        ]


class TestGetItem:
    def test_get_item_success(self, client):
        client.post("/items", json={"name": "Widget"})

        response = client.get("/items/1")

        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "Widget"}

    def test_get_item_not_found(self, client):
        response = client.get("/items/999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}


class TestCreateItem:
    def test_create_item_success(self, client):
        response = client.post("/items", json={"name": "Widget"})

        assert response.status_code == 201
        assert response.json() == {"id": 1, "name": "Widget"}
        assert main.items == {1: {"id": 1, "name": "Widget"}}
        assert main.next_id == 2

    def test_create_item_assigns_incrementing_ids(self, client):
        first = client.post("/items", json={"name": "First"})
        second = client.post("/items", json={"name": "Second"})

        assert first.json()["id"] == 1
        assert second.json()["id"] == 2

    def test_create_item_rejects_invalid_body(self, client):
        response = client.post("/items", json={})

        assert response.status_code == 422


class TestUpdateItem:
    def test_update_item_success(self, client):
        client.post("/items", json={"name": "Widget"})

        response = client.put("/items/1", json={"name": "Super Widget"})

        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "Super Widget"}
        assert main.items[1]["name"] == "Super Widget"

    def test_update_item_not_found(self, client):
        response = client.put("/items/999", json={"name": "Missing"})

        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}

    def test_update_item_rejects_invalid_body(self, client):
        client.post("/items", json={"name": "Widget"})

        response = client.put("/items/1", json={})

        assert response.status_code == 422


class TestDeleteItem:
    def test_delete_item_success(self, client):
        client.post("/items", json={"name": "Widget"})

        response = client.delete("/items/1")

        assert response.status_code == 204
        assert response.content == b""
        assert 1 not in main.items

    def test_delete_item_not_found(self, client):
        response = client.delete("/items/999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}
