#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from typing import List, Optional

DB_NAME = "data/meal_planner.db"


def db_read(sql: str, params: tuple = ()) -> List[dict]:
    """
    Reads sql from db.
    """
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    try:
        cursor = con.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchall()
        con.commit()
        con.close()
        return result
    except Exception:
        con.rollback()
        con.close()
        raise


def db_write(sql: str, params: tuple = ()) -> tuple[int, Optional[int]]:
    """
    Writes sql to db.
    """
    con = sqlite3.connect(DB_NAME)
    try:
        cursor = con.cursor()
        cursor.execute(sql, params)
        rows_affected = cursor.rowcount
        inserted_ids = cursor.lastrowid
        con.commit()
        con.close()
        return rows_affected, inserted_ids
    except Exception:
        con.rollback()
        con.close()
        raise
