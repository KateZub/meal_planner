#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import Connection

from fastapi import APIRouter, Depends

from app import common, db
from app.datatypes.ingredient import Ingredient

router = APIRouter(tags=["ingredients"])


@router.get("/{ingredient_id}/")
async def load_ingredient(ingredient_id: int, db: Connection = Depends(db.get_db)) -> Ingredient:
    """
    Returns ingredient
    """
    ingredient = Ingredient(id=ingredient_id)
    await common.load(db, ingredient)
    return ingredient
