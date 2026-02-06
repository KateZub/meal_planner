#!/usr/bin/env python
# -*- coding: utf-8 -*-
from calendar import weekday

from datatypes.ingredient import Ingredient
from datatypes.recipe import Recipe, RecipeIngredient, Unit
from datatypes.meal_plan import MealPlan, MealPlanRecipe, MealType, Weekday
# from entities.recipe import Recipe, RecipeIngredient, Unit, list_recipes
# from entities.meal_plan import MealPlan, MealPlanRecipe, MealType, Weekday, list_meal_plans

from datetime import date
import entities.common as common

# TODO refaktor (stejne metody sjednotit)
# TODO ukladat ingredience receptu a recepty planu primo v "save"
# TODO FastAPI
# TODO rozdelit dataclassy a metody - nejspis vytvorit dataclass pro API vstup a jinou pro vystup (Entry/Response)
# TODO vytvorit konkretni Exceptions
# TODO logovani

if __name__ == "__main__":

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
    recipe = Recipe(name="Proteinová čokoládová pěna")
    recipe_id = common.get_id(recipe)
    if not recipe_id:
        common.save(recipe)
        recipe_id = common.get_id(recipe)
    print("recipe id: ", recipe_id)
    # EDITACE RECEPTU
    # recipe.servings = 2
    # recipe.source = "Aktin"
    # recipe.source_url = "https://aktin.cz/proteinova-cokoladova-pena"
    # recipe.instructions = "Do mixéru hoď všechny potřebné ingredience a podle potřeby dolij vodu. Směs přelij do skleniček a dej vychladit.\n\nPo ztuhnutí ozdob proteinovými křupinkami, ovocem a pak už jen vychutnávej."
    # common.save(recipe)

    ingredients = []
    ingredients.append(RecipeIngredient(ingredient_name="chia semínka", amount=40, unit=Unit.GRAM))
    ingredients.append(RecipeIngredient(ingredient_name="čokoládový protein", amount=30, unit=Unit.GRAM))
    ingredients.append(RecipeIngredient(ingredient_name="kakao", amount=15, unit=Unit.GRAM))
    ingredients.append(RecipeIngredient(ingredient_name="mléko", amount=150, unit=Unit.GRAM))
    ingredients.append(RecipeIngredient(ingredient_name="Unicorn Dust", amount=3, unit=Unit.GRAM))

    common.add_entity_items(recipe, ingredients)

    common.load(recipe)
    print(recipe)

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
    # common.load(meal_plan)
    # print(meal_plan)

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
    # meal_plan = MealPlan(name='2.2.-8.2.2026', start_date=date(2026, 2, 2), end_date=date(2026,2,8), default_servings=2)
    # meal_plan.load()
    # if not meal_plan.id:
    #     meal_plan.save()
    # print("id planu: ", meal_plan.id)

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
    # meal_plan = MealPlan(name='2.2.-8.2.2026')
    # shopping_list = meal_plan.generate_shopping_list()
    # print(shopping_list)

