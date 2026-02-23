#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.db import db_write


def test_get_nonexistent_ingredient(client):
    response = client.get("/ingredients/1")
    assert response.status_code == 404
    assert response.json() == {"message": "Item '1' not found."}


def test_get_ingredient(db_connection, client):
    ingredient = {"name": "mrkev", "id": 1}
    sql = """INSERT INTO ingredients (id, name) VALUES (:id, :name)"""
    db_write(db_connection, sql, **ingredient)

    response = client.get("/ingredients/1")
    result = response.json()
    db_write(db_connection, "DELETE FROM ingredients WHERE id = ?", (ingredient["id"],))

    assert response.status_code == 200
    assert result["name"] == "mrkev"
    assert result["id"] == 1
