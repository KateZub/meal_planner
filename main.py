#!/usr/bin/env python
# -*- coding: utf-8 -*-
from calendar import weekday

from entities.ingredient import Ingredient
from entities.recipe import Recipe, RecipeIngredient, Unit, list_recipes
from entities.meal_plan import MealPlan, MealPlanRecipe, MealType, Weekday, list_meal_plans

from datetime import date

# TODO refaktor (stejne metody sjednotit)
# TODO FastAPI
# TODO rozdelit dataclassy a metody - nejspis vytvorit dataclass pro API vstup a jinou pro vystup (Entry/Response)
# TODO vytvorit konkretni Exceptions
# TODO logovani

if __name__ == "__main__":

    # VYTVORENI INGREDIENCE
    # ingredient = Ingredient(name="brambory")
    # id = ingredient.get_id_or_create()
    # print("ID of 'brambory' = ", id)

    # NALEZENI A VYTVORENI RECEPTU
    # recipe = Recipe(name='Čokoládové overnight oats')
    # recipe.get_id()
    # if not recipe.id:
    #     recipe.save()
    # print("id receptu: ", recipe.id)

    # EDITACE RECEPTU
    # recipe.load()
    # recipe.servings = 2
    # recipe.instructions = """Ovesné vločky smícháme s čokoládovým proteinem a kakaem, zalijeme mlékem a promícháme. Směs rozdělíme do dvou skleniček a vložíme přes noc do lednice.\n\nRáno přidáme nakrájený banán, lískové ořechy nebo pekany a vysokoprocentní čokoládu nalámanou na kostičky.\n\nDobrou chuť."""
    # recipe.source = 'Aktin'
    # recipe.source_url = 'https://aktin.cz/snidane-do-sklenicky-podzimni-overnight-oats-4x-jinak'
    # recipe.save()

    # PRIDANI INGREDIENCI DO RECEPTU
    # recipe_ingredients = []
    # recipe_ingredients.append(RecipeIngredient(ingredient_name="ovesné vločky", amount=100, unit=Unit.GRAM))
    # recipe_ingredients.append(RecipeIngredient(ingredient_name="mléko", amount=250, unit=Unit.MILLILITER))
    # recipe_ingredients.append(RecipeIngredient(ingredient_name="čokoládový protein", amount=30, unit=Unit.GRAM))
    # recipe_ingredients.append(RecipeIngredient(ingredient_name="kakao", amount=1, unit=Unit.TABLESPOON))
    # recipe_ingredients.append(RecipeIngredient(ingredient_name="banán", amount=1, unit=Unit.PIECE))
    # recipe_ingredients.append(RecipeIngredient(ingredient_name="lískové ořechy", amount=20, unit=Unit.GRAM))
    # recipe_ingredients.append(RecipeIngredient(ingredient_name="hořká čokoláda", amount=12, unit=Unit.GRAM))
    # recipe.add_ingredients(recipe_ingredients)

    # SMAZANI INGREDIENCI Z RECEPTU
    # recipe.remove_ingredients([2, 3, 4])
    # recipe.remove_ingredients(["kakao", "banán"])

    # NACTENI RECEPTU
    # recipe.load()
    # print(recipe)

    # VYTVORENI PLANU
    meal_plan = MealPlan(name='2.2.-8.2.2026', start_date=date(2026, 2, 2), end_date=date(2026,2,8), default_servings=2)
    meal_plan.load()
    if not meal_plan.id:
        meal_plan.save()
    print("id planu: ", meal_plan.id)

    # PRIDANI RECEPTU DO PLANU
    # meal_plan_recipes = []
    # meal_plan_recipes.append(MealPlanRecipe(recipe_name="Čokoládové overnight oats", meal_type=MealType.BREAKFAST, weekday=Weekday.MONDAY))
    # meal_plan_recipes.append(MealPlanRecipe(recipe_name="Čokoládové overnight oats", meal_type=MealType.BREAKFAST, weekday=Weekday.TUESDAY))
    # meal_plan.add_recipes(meal_plan_recipes)

    # SMAZANI RECEPTU Z PLANU
    # meal_plan.remove_recipes([1])
    # meal_plan.remove_recipes(["Čokoládové overnight oats"])

    # NACTENI PLANU
    # meal_plan.load()
    # print(meal_plan)

    # LIST
    # recipes = list_recipes()
    # print(recipes)
    # meal_plans = list_meal_plans()
    # print(meal_plans)

    # GENEROVANI NAKUPNIHO SEZNAMU
    meal_plan = MealPlan(name='2.2.-8.2.2026')
    shopping_list = meal_plan.generate_shopping_list()
    print(shopping_list)

