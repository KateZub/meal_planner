#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from typing import Any, List, Optional

DB_NAME = "data/meal_planner.db"


async def get_db():
    """
    Yields db connection and then closes it.
    """
    db = sqlite3.connect(DB_NAME)
    try:
        yield db
    finally:
        db.close()


def db_read(db: sqlite3.Connection, sql: str, params: tuple = (), **kwargs: Any) -> List[dict]:
    """
    Reads sql from db.
    """
    db.row_factory = sqlite3.Row
    try:
        cursor = db.cursor()
        cursor.execute(sql, params or kwargs)
        result = cursor.fetchall()
        db.commit()
        return result
    except Exception:
        db.rollback()
        raise


def db_write(db: sqlite3.Connection, sql: str, params: tuple = (), **kwargs: Any) -> tuple[int, Optional[int]]:
    """
    Writes sql to db.
    """
    try:
        cursor = db.cursor()
        cursor.execute(sql, params or kwargs)
        rows_affected = cursor.rowcount
        inserted_ids = cursor.lastrowid
        db.commit()
        return rows_affected, inserted_ids
    except Exception:
        db.rollback()
        raise
