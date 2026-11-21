import pytest
from fastapi.testclient import TestClient
from app.main import app, manager

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tickets():
    manager.tickets.clear()
    manager.next_id = 1


def sample_ticket():
    return {
        "requester_name": "Arun",
        "department": "Accounts",
        "title": "Laptop not starting",
        "description": "Blank screen after startup",
        "priority": "High"
    }


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_create_ticket():
    response = client.post("/tickets", json=sample_ticket())
    assert response.status_code == 201
    assert response.json()["requester_name"] == "Arun"
    assert response.json()["status"] == "Open"


def test_create_ticket_empty_title():
    data = sample_ticket()
    data["title"] = ""
    response = client.post("/tickets", json=data)
    assert response.status_code == 422


def test_create_ticket_invalid_priority():
    data = sample_ticket()
    data["priority"] = "Urgent"
    response = client.post("/tickets", json=data)
    assert response.status_code == 400


def test_get_all_tickets():
    client.post("/tickets", json=sample_ticket())
    response = client.get("/tickets")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_ticket_by_id():
    client.post("/tickets", json=sample_ticket())
    response = client.get("/tickets/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_ticket_not_found():
    response = client.get("/tickets/999")
    assert response.status_code == 404


def test_update_status():
    client.post("/tickets", json=sample_ticket())
    response = client.put(
        "/tickets/1/status", json={"status": "Resolved"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Resolved"


def test_invalid_status():
    client.post("/tickets", json=sample_ticket())
    response = client.put(
        "/tickets/1/status", json={"status": "Closed"}
    )
    assert response.status_code == 400


def test_assign_ticket():
    client.post("/tickets", json=sample_ticket())
    response = client.put(
        "/tickets/1/assign",
        json={"agent_name": "Support Agent 1"}
    )
    assert response.status_code == 200
    assert response.json()["assigned_to"] == "Support Agent 1"


def test_delete_ticket():
    client.post("/tickets", json=sample_ticket())
    response = client.delete("/tickets/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Ticket deleted successfully"


def test_search_ticket():
    client.post("/tickets", json=sample_ticket())
    response = client.get("/tickets/search/Arun")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_filter_by_priority():
    client.post("/tickets", json=sample_ticket())
    response = client.get("/ticket-filters?priority=High")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_filter_by_status():
    client.post("/tickets", json=sample_ticket())
    response = client.get("/ticket-filters?status=Open")
    assert response.status_code == 200
    assert len(response.json()) == 1
