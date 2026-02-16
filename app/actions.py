#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import Connection
from typing import Literal

from app import common
from app.datatypes.meal_plan import MealPlan
from app.datatypes.recipe import Recipe, RecipeIngredient
from app.db import db_read

MealPlanCriterionType = Literal["id", "name", "default_servings", "start_date", "end_date"]
RecipesCriterionType = Literal["id", "name", "servings", "source"]
DirectionType = Literal["asc", "desc"]


async def list_meal_plans(
    db: Connection, offset: int = 0, limit: int = 10, criterion: MealPlanCriterionType = "name", direction: DirectionType = "asc"
) -> list[MealPlan]:
    """
    Lists meal plans
    """
    sql = f"""
        SELECT id
        FROM meal_plan
        ORDER BY {criterion} {direction}
        LIMIT ?, ?
    """
    result = []
    for row in db_read(db, sql, (offset, limit)):
        meal_plan = MealPlan(id=row["id"])
        await common.load(db, meal_plan)
        result.append(meal_plan)

    return result


async def list_recipes(
    db: Connection, offset: int = 0, limit: int = 10, criterion: RecipesCriterionType = "name", direction: DirectionType = "asc"
) -> list[Recipe]:
    """
    Lists recipes
    """
    sql = f"""
        SELECT id
        FROM recipes
        ORDER BY {criterion} {direction}
        LIMIT ?, ?
    """
    result = []
    for row in db_read(db, sql, (offset, limit)):
        recipe = Recipe(id=row["id"])
        await common.load(db, recipe)
        result.append(recipe)

    return result


async def generate_shopping_list(db: Connection, meal_plan: MealPlan) -> list[RecipeIngredient]:
    """
    Generates shopping list for the meal plan.
    """
    await common.load(db, meal_plan)
    recipes_servings = {}
    for recipe in meal_plan.recipes:
        recipes_servings.setdefault(recipe.recipe_id, 0)
        recipes_servings[recipe.recipe_id] += recipe.servings

    shopping_list = {}
    for recipe_id, servings in recipes_servings.items():
        recipe = Recipe(id=recipe_id)
        await common.load(db, recipe)
        for ingredient in recipe.ingredients:
            shopping_list.setdefault(
                ingredient.ingredient_name,
                RecipeIngredient(
                    ingredient_name=ingredient.ingredient_name,
                    ingredient_id=ingredient.ingredient_id,
                    amount=0,
                    unit=ingredient.unit.value,
                ),
            )
            amount_addition = (ingredient.amount * servings) / recipe.servings
            shopping_list[ingredient.ingredient_name].amount += amount_addition

    return list(shopping_list.values())
