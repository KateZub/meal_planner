#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db_read, db_write
from typing import Union

from datatypes.ingredient import Ingredient
from datatypes.meal_plan import MealPlan
from datatypes.recipe import Recipe

EntityObject = Union[Ingredient, MealPlan, Recipe]

LOAD_SECOND_ATTRIBUTES_SQLS = {
    "meal plan": """SELECT mpr.*, recipes.name
            FROM meal_plan_recipes mpr
            JOIN recipes ON mpr.recipe_id = recipes.id
            WHERE mpr.meal_plan_id = ?
        """,

    "recipe": """SELECT * 
            FROM recipe_ingredients ri
            JOIN ingredients ON ri.ingredient_id = ingredients.id
            WHERE ri.recipe_id = ?
        """
}

def get_id(entity: EntityObject) -> int | None:
    """
    Returns id of the entity object.
    """
    if entity.id:
        return entity.id

    if not entity.name:
        raise Exception(f"{entity.entity_name} has no name.")

    sql = f"SELECT id FROM {entity.entity_db_table} WHERE name = ?"
    result = db_read(sql, (entity.name,))
    if not result:
        print(f"{entity.entity_name} '{entity.name}' not found.")
        return None

    entity.id = result[0]['id']
    return entity.id

def load(entity: EntityObject) -> None:
    """
    Loads entity data from db.
    """
    sql = f"SELECT * FROM {entity.entity_db_table} WHERE "
    if entity.id:
        sql += "id = ?"
        params = (entity.id,)
    elif entity.name:
        sql += "name = ?"
        params = (entity.name,)
    else:
        raise Exception(f"Id or name of the {entity.entity_name} must be given.")

    attributes = db_read(sql, params)
    if not attributes:
        print(f"{entity.entity_name} '{params[0]}' not found.")
        return

    sql = LOAD_SECOND_ATTRIBUTES_SQLS.get(entity.entity_name)
    if sql:
        second_attributes = db_read(sql, (entity.id,))
        entity.load_from_dict(attributes[0], second_attributes)
    else:
        entity.load_from_dict(attributes[0])

def save(entity: EntityObject) -> None:
    """
    Updates or creates new entity in db.
    """
    # TODO ukladat ingredience receptu a recepty planu
    # TODO neukladat vsechny udaje, jen pokud se neco meni

    attributes = entity.get_dict_to_save()

    if entity.id:
        sql = f"UPDATE {entity.entity_db_table} SET {", ".join([f"{name} = ?" for name in attributes.keys()])} WHERE id = ?"
        params = list(attributes.values())
        params.append(entity.id)
    else:
        sql = f"INSERT INTO {entity.entity_db_table} ({", ".join(attributes.keys())}) VALUES ({", ".join("?" * len(attributes))})"
        params = attributes.values()

    _, id_ = db_write(sql, tuple(params))
    if not entity.id and id_:
        print(f"New {entity.entity_name} created.")
        entity.id = id_
    else:
        print(f"{entity.entity_name} updated.")


