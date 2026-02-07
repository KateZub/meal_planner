#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, ClassVar


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
    entity_name: ClassVar[str] = "meal plan"
    entity_db_table: ClassVar[str] = "meal_plan"
    entity_items_sql: ClassVar[str] = """SELECT mpr.*, recipes.name
            FROM meal_plan_recipes mpr
            JOIN recipes ON mpr.recipe_id = recipes.id
            WHERE mpr.meal_plan_id = ?
        """

    name: str = Field(default=None, min_length=3)
    default_servings: int = Field(default=1, ge=1)
    id: int = None
    start_date: date = None
    end_date: date = None
    recipes: list[MealPlanRecipe] = Field(default_factory=list)

    def load_from_dict(self, attributes: dict, recipes: List[dict]) -> None:
        """
        Loads MealPlan from dict.
        """
        self.id = attributes['id']
        self.name = attributes['name']
        self.start_date = datetime.strptime(attributes['start_date'], "%Y-%m-%d").date()
        self.end_date = datetime.strptime(attributes['end_date'], "%Y-%m-%d").date()
        self.default_servings = attributes['default_servings']

        for recipe in recipes:
            self.recipes.append(MealPlanRecipe(recipe_name=recipe["name"], recipe_id=recipe["recipe_id"],
                                               weekday=recipe["weekday"], meal_type=recipe["meal_type"],
                                               servings=recipe["servings"]))

    def get_dict_to_save(self) -> dict:
        """
        Returns dict of the MealPlan for saving to db.
        """
        return self.dict(exclude={'recipes', 'id'})

    @staticmethod
    def get_sql_and_params_for_new_items(entity_attributes: dict, recipes: List[MealPlanRecipe]) -> tuple:
        """
        Returns sql and params for adding new recipes to the meal plan.
        """
        if not entity_attributes.get("id"):
            raise Exception("Missing entity id.")

        sql = "INSERT INTO meal_plan_recipes (meal_plan_id, recipe_id, weekday, meal_type, servings) VALUES "
        sql_values = []
        sql_params = []

        for meal_plan_recipe in recipes:
            if not meal_plan_recipe.recipe_id:
                raise Exception("Missing recipe id.")

            if not meal_plan_recipe.servings:
                meal_plan_recipe.servings = entity_attributes.get("default_servings", 1)

            sql_values.append("(?, ?, ?, ?, ?)")
            sql_params.extend([entity_attributes["id"], meal_plan_recipe.recipe_id, meal_plan_recipe.weekday.value,
                               meal_plan_recipe.meal_type.value, meal_plan_recipe.servings])

        sql += ", ".join(sql_values)
        sql += " ON CONFLICT DO Update SET weekday=excluded.weekday, meal_type=excluded.meal_type, servings=excluded.servings"

        return sql, tuple(sql_params)

    @staticmethod
    def get_sql_and_params_for_items_to_remove(entity_id: int, recipes: list[str] | list[int]) -> tuple:
        """
        Returns sql for removing recipes from the meal plan.
        """
        if isinstance(recipes[0], int):
            sql = f"DELETE FROM meal_plan_recipes WHERE meal_plan_id = ? AND recipe_id IN ({", ".join("?" * len(recipes))})"
        else:
            sql = f"""
                DELETE FROM meal_plan_recipes
                WHERE meal_plan_id = ? AND recipe_id IN
                 (SELECT id FROM recipes WHERE name IN ({", ".join("?" * len(recipes))}))
            """

        return sql, tuple([entity_id] + recipes)
