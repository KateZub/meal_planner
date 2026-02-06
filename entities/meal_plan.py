#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Literal

from db import db_read, db_write
from entities.recipe import Recipe

class Weekday(Enum):
    MONDAY = "pondělí"
    TUESDAY = "úterý"
    WEDNESDAY = "středa"
    THURSDAY = "čtvrtek"
    FRIDAY = "pátek"
    SATURDAY = "sobota"
    SUNDAY = "neděle"

class MealType(Enum):
    BREAKFAST = "snídaně"
    LUNCH = "oběd"
    DINNER = "večeře"
    SNACK = "svačina"

class MealPlanRecipe(BaseModel):
    recipe_name: str
    weekday: Weekday
    meal_type: MealType
    servings: int = Field(default=None, ge=1)
    recipe_id: int = None

class MealPlan(BaseModel):
    name: str = Field(default=None, min_length=3)
    default_servings: int = Field(default=None, ge=1)
    id: int = None
    start_date: date = None
    end_date: date = None
    recipes: list[MealPlanRecipe] = Field(default_factory=list)
    entity_name: Literal["meal plan"] = "meal plan"
    entity_db_table: Literal["meal_plan"] = "meal_plan"

    def add_recipes(self, recipes: list[MealPlanRecipe]) -> None:
        """
        Adds recipes to the meal plan.
        """
        if not self.id:
            self.get_id()

        sql = "INSERT INTO meal_plan_recipes (meal_plan_id, recipe_id, weekday, meal_type, servings) VALUES "
        sql_values = []
        sql_params = []

        for meal_plan_recipe in recipes:
            if not meal_plan_recipe.recipe_id:
                recipe = Recipe(name=meal_plan_recipe.recipe_name)
                meal_plan_recipe.recipe_id = recipe.get_id()
            if not meal_plan_recipe.servings:
                if not self.default_servings:
                    self.load()
                meal_plan_recipe.servings = self.default_servings

            sql_values.append("(?, ?, ?, ?, ?)")
            sql_params.extend([self.id, meal_plan_recipe.recipe_id, meal_plan_recipe.weekday.value, meal_plan_recipe.meal_type.value, meal_plan_recipe.servings])

        sql += ", ".join(sql_values)
        sql += " ON CONFLICT DO Update SET weekday=excluded.weekday, meal_type=excluded.meal_type, servings=excluded.servings"

        db_write(sql, tuple(sql_params))
        print("Recipes added to the meal plan.")

    def remove_recipes(self, recipes: list[str] | list[int]) -> None:
        """
        Removes recipes from the meal plan.

        @param recipes - list of recipes names or list of recipes ids
                        removes all these recipes from the meal plan
        """
        if not self.id:
            self.get_id()

        if isinstance(recipes[0], int):
            sql = f"DELETE FROM meal_plan_recipes WHERE meal_plan_id = ? AND recipe_id IN ({", ".join("?" * len(recipes))})"
        else:
            sql = f"""
                DELETE FROM meal_plan_recipes
                WHERE meal_plan_id = ? AND recipe_id IN
                 (SELECT id FROM recipes WHERE name IN ({", ".join("?" * len(recipes))}))
            """

        db_write(sql, tuple([self.id] + recipes))
        print("Recipes removed from the meal plan.")

    def generate_shopping_list(self) -> dict:
        # TODO vystup dataclass
        """
        Generates shopping list for the meal plan.
        """
        # TODO jak poznat jestli uz je load hotovy? dat si priznak?
        self.load()
        recipes_servings = {}
        for recipe in self.recipes:
            recipes_servings.setdefault(recipe.recipe_id, 0)
            recipes_servings[recipe.recipe_id] += recipe.servings

        shopping_list = {}
        for recipe_id, servings in recipes_servings.items():
            recipe = Recipe(id=recipe_id)
            recipe.load()
            for ingredient in recipe.ingredients:
                shopping_list.setdefault(ingredient.ingredient_name, {"amount": 0, "unit": ingredient.unit.value})
                amount_addition = (ingredient.amount * servings) / recipe.servings
                shopping_list[ingredient.ingredient_name]["amount"] += amount_addition

        return shopping_list


def list_meal_plans(offset: int = 0, limit: int = 10, criterion: str = "name", direction: str = "asc") -> List[MealPlan]:
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
        meal_plan.load()
        result.append(meal_plan)

    return result

