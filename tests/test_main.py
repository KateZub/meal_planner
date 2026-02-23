#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_read_main(client):
    """
    Simple test for root
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
