#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from pydantic import BaseModel, Field
from typing import List


from db import db_read, db_write
from entities.ingredient import Ingredient

class Unit(Enum):
    GRAM = 'g'
    MILLILITER = 'ml'
    PIECE = 'ks'
    TEASPOON = 'ČL'
    TABLESPOON = 'PL'
    PINCH = 'špetka'

class RecipeIngredient(BaseModel):
    ingredient_name: str
    amount: int
    unit: Unit
    ingredient_id: int = None

class Recipe(BaseModel):
    name: str = Field(default=None, min_length=3)
    servings: int = Field(default=1, ge=1)
    id: int = None
    instructions: str = None
    source: str = None
    source_url: str = None
    ingredients: list[RecipeIngredient] = Field(default_factory=list)

    def remove_ingredients(self, ingredients: list[str] | list[int]) -> None:
        """
        Removes ingredients from the recipe.

        @param ingredients - list of ingredients names or list of ingredients ids
        """
        if not self.id:
            self.get_id()

        if isinstance(ingredients[0], int):
            sql = f"DELETE FROM recipe_ingredients WHERE recipe_id = ? AND ingredient_id IN ({", ".join("?" * len(ingredients))})"
        else:
            sql = f"""
                DELETE FROM recipe_ingredients
                WHERE recipe_id = ? AND ingredient_id IN
                 (SELECT id FROM ingredients WHERE name IN ({", ".join("?" * len(ingredients))}))
            """

        db_write(sql, tuple([self.id] + ingredients))
        print("Ingredients removed from the recipe.")

def list_recipes(offset: int = 0, limit: int = 10, criterion: str = "name", direction: str = "asc") -> List[Recipe]:
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
        recipe.load()
        result.append(recipe)

    return result


