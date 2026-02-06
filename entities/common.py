#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db_read, db_write
from typing import Union
from entities.recipe import Recipe
from entities.meal_plan import MealPlan

EntityObject = Union[Recipe, MealPlan]


def get_id(entity_object: EntityObject) -> int | None:
    """
    Returns id of the entity object.
    """
    if entity_object.id:
        return entity_object.id

    if not entity_object.name:
        raise Exception(f"{entity_object.entity_name} has no name.")

    sql = f"SELECT id FROM {entity_object.entity_db_table} WHERE name = ?"
    result = db_read(sql, (entity_object.name,))
    if not result:
        print(f"{entity_object.entity_name} '{entity_object.name}' not found.")
        return None

    entity_object.id = result[0]['id']
    return entity_object.id

