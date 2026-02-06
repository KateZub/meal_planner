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

    def get_id(self) -> int | None:
        """
        Returns id of the meal plan.
        """
        if self.id:
            return self.id

        if not self.name:
            raise Exception("Meal plan has no name.")

        sql = "SELECT id FROM meal_plan WHERE name = ?"
        result = db_read(sql, (self.name,))
        if not result:
            print("Meal plan '%s' not found." % self.name)
            return None

        self.id = result[0]['id']
        return self.id

    def load(self) -> None:
        """
        Loads meal plan from db.
        """
        sql = "SELECT * FROM meal_plan WHERE "
        if self.id:
            sql += "id = ?"
            params = (self.id,)
        elif self.name:
            sql += "name = ?"
            params = (self.name,)
        else:
            raise Exception("Id or name of the meal plan must be given.")

        result = db_read(sql, params)
        if not result:
            print("Meal plan '%s' not found." % params[0])
            return

        # TODO udelat elegantneji
        self.id = result[0]['id']
        self.name = result[0]['name']
        self.start_date = result[0]['start_date']
        self.end_date = result[0]['end_date']
        self.default_servings = result[0]['default_servings']

        sql = """SELECT mpr.*, recipes.name
            FROM meal_plan_recipes mpr
            JOIN recipes ON mpr.recipe_id = recipes.id
            WHERE mpr.meal_plan_id = ?
        """
        for recipe in db_read(sql, (self.id,)):
            self.recipes.append(MealPlanRecipe(recipe_name=recipe["name"], recipe_id=recipe["recipe_id"],
                                               weekday=recipe["weekday"], meal_type=recipe["meal_type"],
                                               servings=recipe["servings"]))

    def save(self) -> None:
        """
        Updates or creates new meal plan in db.
        """
        # TODO pred ulozenim udelat load, aby se nesmazaly puvodni informace nebo ukladat jen vstupy
        if not self.name:
            raise Exception("Meal plan has to have name.")

        # TODO UPSERT?
        if self.id:
            sql = "UPDATE meal_plan SET name = ?, start_date = ?, end_date = ?, default_servings = ? WHERE id = ?"
            params = (self.name, self.start_date, self.end_date, self.default_servings or 1, self.id)
        else:
            sql = "INSERT INTO meal_plan (name, start_date, end_date, default_servings) VALUES (?, ?, ?, ?)"
            params = (self.name, self.start_date, self.end_date, self.default_servings or 1)

        _, id = db_write(sql, params)
        if not self.id and id:
            print("New meal plan created.")
            self.id = id
        else:
            print("Meal plan updated.")

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

