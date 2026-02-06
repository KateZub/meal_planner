#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
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
        self.start_date = attributes['start_date']
        self.end_date = attributes['end_date']
        self.default_servings = attributes['default_servings']

        for recipe in recipes:
            self.recipes.append(MealPlanRecipe(recipe_name=recipe["name"], recipe_id=recipe["recipe_id"],
                                               weekday=recipe["weekday"], meal_type=recipe["meal_type"],
                                               servings=recipe["servings"]))

    def get_dict_to_save(self) -> dict:
        """
        Returns dict of the MealPlan for saving to db.
        """
        # TODO pripravit recipes na ulozeni
        return self.dict(exclude={'recipes', 'id'})
