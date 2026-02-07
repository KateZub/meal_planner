#!/usr/bin/env python
# -*- coding: utf-8 -*-
from calendar import weekday

from datatypes.ingredient import Ingredient
from datatypes.recipe import Recipe, RecipeIngredient, Unit
from datatypes.meal_plan import MealPlan, MealPlanRecipe, MealType, Weekday

from datetime import date
import src.common as common
import src.actions as actions

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/meal_plans/")
async def list_meal_plans(offset: int = 0, limit: int = 10, criterion: actions.MealPlanCriterionType = "name", direction: actions.DirectionType = "asc") -> list[MealPlan]:
    """
    Lists meal plans
    """
    result = actions.list_meal_plans(offset=offset, limit=limit, criterion=criterion, direction=direction)
    return result

@app.get("/recipes/")
async def list_recipes(offset: int = 0, limit: int = 10, criterion: actions.RecipesCriterionType = "name", direction: actions.DirectionType = "asc") -> list[Recipe]:
    """
    Lists recipes
    """
    result = actions.list_recipes(offset=offset, limit=limit, criterion=criterion, direction=direction)
    return result

@app.get("/meal_plan/{meal_plan_id}/shopping_list/")
async def get_shopping_list(meal_plan_id: int) -> list[RecipeIngredient]:
    """
    Returns shopping list for the meal plan
    """
    meal_plan = MealPlan(id=meal_plan_id)
    result = actions.generate_shopping_list(meal_plan)
    return result

# TODO FastAPI
# TODO rozdelit dataclassy a metody - nejspis vytvorit dataclass pro API vstup a jinou pro vystup (Entry/Response)
# TODO vytvorit konkretni Exceptions
# TODO logovani

# if __name__ == "__main__":

    # VYTVORENI INGREDIENCE
    # ingredient = Ingredient(name="chia semínka")
    # ingredient_id = common.get_id(ingredient)
    # if not ingredient_id:
    #     common.save(ingredient)
    #     ingredient_id = common.get_id(ingredient)
    # print("ingredient id: ", ingredient_id)
    # common.load(ingredient)
    # print(ingredient)

    # VYTVORENI RECEPTU
    # recipe = Recipe(name="Proteinová čokoládová pěna")
    # recipe_id = common.get_id(recipe)
    # if not recipe_id:
    #     common.save(recipe)
    #     recipe_id = common.get_id(recipe)
    # print("recipe id: ", recipe_id)
    # # EDITACE RECEPTU
    # # recipe.servings = 2
    # # recipe.source = "Aktin"
    # # recipe.source_url = "https://aktin.cz/proteinova-cokoladova-pena"
    # # recipe.instructions = "Do mixéru hoď všechny potřebné ingredience a podle potřeby dolij vodu. Směs přelij do skleniček a dej vychladit.\n\nPo ztuhnutí ozdob proteinovými křupinkami, ovocem a pak už jen vychutnávej."
    # # common.save(recipe)
    #
    # ingredients = []
    # ingredients.append(RecipeIngredient(ingredient_name="chia semínka", amount=40, unit=Unit.GRAM))
    # ingredients.append(RecipeIngredient(ingredient_name="čokoládový protein", amount=30, unit=Unit.GRAM))
    # ingredients.append(RecipeIngredient(ingredient_name="kakao", amount=15, unit=Unit.GRAM))
    # ingredients.append(RecipeIngredient(ingredient_name="mléko", amount=150, unit=Unit.GRAM))
    # ingredients.append(RecipeIngredient(ingredient_name="Unicorn Dust", amount=3, unit=Unit.GRAM))
    #
    # common.add_entity_items(recipe, ingredients)
    #
    # # common.remove_entity_items(recipe, ["chia semínka", "čokoládový protein"])
    # # common.remove_entity_items(recipe, [3, 5])
    #
    # common.load(recipe)
    # print(recipe)

    # VYTVORENI PLANU
    # meal_plan = MealPlan(name="9.2.-15.2.2026", start_date=date(2026, 2, 9), end_date=date(2026, 2, 15), default_servings=2)
    # meal_plan_id = common.get_id(meal_plan)
    # if not meal_plan_id:
    #     common.save(meal_plan)
    #     meal_plan_id = common.get_id(meal_plan)
    # print("meal plan id: ", meal_plan_id)
    # # EDITACE PLANU
    # # meal_plan.default_servings = 2
    # # common.save(meal_plan)
    #
    # recipes = []
    # recipes.append(MealPlanRecipe(recipe_name="Proteinová čokoládová pěna", meal_type=MealType.SNACK, weekday=Weekday.MONDAY))
    # recipes.append(MealPlanRecipe(recipe_name="Proteinová čokoládová pěna", meal_type=MealType.SNACK, weekday=Weekday.TUESDAY))
    #
    # common.add_entity_items(meal_plan, recipes)
    #
    # # common.remove_entity_items(meal_plan, ["Proteinová čokoládová pěna"])
    # # common.remove_entity_items(meal_plan, [2])
    #
    # common.load(meal_plan)
    # print(meal_plan)

    # LIST
    # meal_plans = actions.list_meal_plans()
    # print(meal_plans)
    #
    # recipes = actions.list_recipes()
    # print(recipes)

    # GENEROVANI NAKUPNIHO SEZNAMU
    # meal_plan = MealPlan(name='2.2.-8.2.2026')
    # shopping_list = actions.generate_shopping_list(meal_plan)
    # print(shopping_list)

