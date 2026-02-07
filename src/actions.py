#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datatypes.meal_plan import MealPlan
from datatypes.recipe import Recipe
from db import db_read

import src.common as common

def list_meal_plans(offset: int = 0, limit: int = 10, criterion: str = "name", direction: str = "asc") -> list[MealPlan]:
    """
    Lists meal plans
    """
    # TODO udelat vstup jako pydantic dataclass kvuli validaci
    sql = f"""
        SELECT id
        FROM meal_plan
        ORDER BY ?
        LIMIT ?, ?
    """
    result = []
    for row in db_read(sql, (f"{criterion} {direction}", offset, limit)):
        meal_plan = MealPlan(id=row["id"])
        common.load(meal_plan)
        result.append(meal_plan)

    return result


def list_recipes(offset: int = 0, limit: int = 10, criterion: str = "name", direction: str = "asc") -> list[Recipe]:
    """
    Lists recipes
    """
    # TODO udelat vstup jako pydantic dataclass kvuli validaci
    sql = f"""
        SELECT id
        FROM recipes
        ORDER BY ?
        LIMIT ?, ?
    """
    result = []
    for row in db_read(sql, (f"{criterion} {direction}", offset, limit)):
        recipe = Recipe(id=row["id"])
        common.load(recipe)
        result.append(recipe)

    return result


def generate_shopping_list(meal_plan: MealPlan) -> dict:
    # TODO vystup dataclass
    """
    Generates shopping list for the meal plan.
    """
    # TODO jak poznat jestli uz je load hotovy? dat si priznak?
    common.load(meal_plan)
    recipes_servings = {}
    for recipe in meal_plan.recipes:
        recipes_servings.setdefault(recipe.recipe_id, 0)
        recipes_servings[recipe.recipe_id] += recipe.servings

    shopping_list = {}
    for recipe_id, servings in recipes_servings.items():
        recipe = Recipe(id=recipe_id)
        common.load(recipe)
        for ingredient in recipe.ingredients:
            shopping_list.setdefault(ingredient.ingredient_name, {"amount": 0, "unit": ingredient.unit.value})
            amount_addition = (ingredient.amount * servings) / recipe.servings
            shopping_list[ingredient.ingredient_name]["amount"] += amount_addition

    return shopping_list

