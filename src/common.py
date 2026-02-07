#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db_read, db_write
from typing import Union

from datatypes.ingredient import Ingredient
from datatypes.meal_plan import MealPlan, MealPlanRecipe
from datatypes.recipe import Recipe, RecipeIngredient

EntityObject = Union[Ingredient, MealPlan, Recipe]
EntityItemObject = Union[MealPlanRecipe, RecipeIngredient]


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

    if not entity.id:
        entity.id = attributes[0]["id"]

    if hasattr(entity, "entity_items_sql"):
        second_attributes = db_read(entity.entity_items_sql, (entity.id,))
        entity.load_from_dict(attributes[0], second_attributes)
    else:
        entity.load_from_dict(attributes[0])

def save(entity: EntityObject) -> None:
    """
    Updates or creates new entity in db.
    """
    # TODO ukladat ingredience receptu a recepty planu?
    # TODO neukladat vsechny udaje, jen pokud se neco meni?

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

def __add_items_ids(entity_items: list[EntityItemObject]) -> None:
    """
    Adds missing ids for items. If it's Ingredient and it doesn't exist, it will be created.
    """
    for item in entity_items:
        if isinstance(item, MealPlanRecipe) and not item.recipe_id:
            recipe = Recipe(name=item.recipe_name)
            item.recipe_id = get_id(recipe)
        elif isinstance(item, RecipeIngredient) and not item.ingredient_id:
            ingredient = Ingredient(name=item.ingredient_name)
            item.ingredient_id = get_id(ingredient)
            if not item.ingredient_id:
                save(ingredient)
                item.ingredient_id = get_id(ingredient)


def add_entity_items(entity: EntityObject, entity_items: list[EntityItemObject]) -> None:
    """
    Adds items to the entity.
    """
    if not entity_items:
        print("no items to add")
        return

    if not entity.id:
        get_id(entity)

    entity_attributes = {"id": entity.id}
    if isinstance(entity, MealPlan):
        if not entity.default_servings:
            load(entity)
        entity_attributes["default_servings"] = entity.default_servings

    __add_items_ids(entity_items)

    sql, sql_params = entity.get_sql_and_params_for_new_items(entity_attributes, entity_items)
    db_write(sql, sql_params)
    print(f"Items added to the {entity.entity_name}.")

def remove_entity_items(entity: EntityObject, entity_items: list[str] | list[int]) -> None:
    """
    Removes items from the entity.

    @param entity_items - list of items names or list of items ids
    """
    if not entity_items:
        print("no items to remove")
        return

    if not entity.id:
        get_id(entity)

    sql, params = entity.get_sql_and_params_for_items_to_remove(entity.id, entity_items)
    db_write(sql, params)
    print(f"Items removed from the {entity.entity_name}.")
