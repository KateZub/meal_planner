#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import os
from datetime import datetime
from sqlite3 import Connection
from typing import Literal, Tuple

from openai import OpenAI

from app import common
from app.datatypes.meal_plan import MealPlan
from app.datatypes.recipe import HttpUrl, Recipe, RecipeIngredient, Unit
from app.db import db_read, db_write

logger = logging.getLogger("uvicorn.error")

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


async def get_the_recipe_from_url(db: Connection, url: HttpUrl, force: bool = False) -> Tuple[Recipe | str, datetime]:
    """
    Connection to the openAI and getting the recipe from given url.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = """chci recept z teto url: %s, vrat mi ho v json formatu typu: { "nazev": "", "porce": "", "postup": "", "nazev zdroje": "", "ingredience": [{"nazev": "", "mnozstvi": "", "jednotka": ""}]}. Pokud je potreba, preved jednotky do metrickeho systemu."""
    prompt = prompt % str(url)

    if not force:
        sql = """SELECT output, created_at FROM open_ai_outputs WHERE prompt = ? ORDER BY created_at DESC LIMIT 1"""
        result = db_read(db, sql, (prompt,))
        if result:
            return process_open_ai_result(result[0]["output"], url), datetime.strptime(
                result[0]["created_at"], "%Y-%m-%d %H:%M:%S"
            )

    result = ""
    try:
        response = client.responses.create(model="gpt-5.6", tools=[{"type": "web_search"}], input=prompt)

        sql = """INSERT INTO open_ai_outputs (output, prompt) VALUES (?, ?)"""
        db_write(db, sql, (response.output_text, prompt))

        result = process_open_ai_result(response.output_text, url)
    except Exception as exc:
        logger.exception(exc)

    return result, datetime.now()


def process_open_ai_result(result: str, url: HttpUrl) -> Recipe | str:
    """
    Tries to extract just the json output.
    """
    start = result.find("{")
    end = result.rfind("}")

    if start != -1 and end != -1:
        result = result[start : end + 1]

    recipe = result
    try:
        recipe = json.loads(result)
        recipe_attributes = {
            "id": None,
            "name": recipe["nazev"],
            "servings": recipe["porce"],
            "instructions": recipe["postup"],
            "source": recipe["nazev zdroje"],
            "source_url": url,
        }
        ingredients = []
        for ingredient in recipe["ingredience"]:
            ingredients.append(
                {
                    "ingredient_id": None,
                    "name": ingredient["nazev"],
                    "amount": ingredient["mnozstvi"],
                    "unit": Unit(ingredient["jednotka"]),
                }
            )

        recipe = Recipe()
        recipe.load_from_dict(recipe_attributes, ingredients)
    except Exception as exc:
        logger.exception(exc)

    return recipe
