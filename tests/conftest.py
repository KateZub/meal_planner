#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.db import DB_NAME
from app.main import app


@pytest.fixture(scope="session")
def client():
    """
    TestClient for the app
    """
    return TestClient(app)


@pytest.fixture(scope="session")
def db_connection():
    """
    DB connection for the tests
    """
    db = sqlite3.connect(DB_NAME)
    try:
        yield db
    finally:
        db.close()
