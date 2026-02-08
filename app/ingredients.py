#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fastapi

from app import common
from app.datatypes.ingredient import Ingredient

router = fastapi.APIRouter(tags=["ingredients"])


@router.get("/{ingredient_id}/")
async def load_ingredient(ingredient_id: int) -> Ingredient:
    """
    Returns ingredient
    """
    ingredient = Ingredient(id=ingredient_id)
    await common.load(ingredient)
    return ingredient
