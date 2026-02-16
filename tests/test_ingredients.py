#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_ingredient():
    response = client.get("/ingredients/1")
    assert response.status_code == 200
    assert response.json() == {"name": "brambory", "id": 1}

def test_get_nonexistent_ingredient():
    response = client.get("/ingredients/-1")
    assert response.status_code == 404
    assert response.json() == {"message": f"Item '-1' not found."}

