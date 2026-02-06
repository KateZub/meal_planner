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

    def get_id(self) -> int | None:
        """
        Returns id of the recipe.
        """
        if self.id:
            return self.id

        if not self.name:
            raise Exception("Recipe has no name.")

        sql = "SELECT id FROM recipes WHERE name = ?"
        result = db_read(sql, (self.name,))
        if not result:
            print("Recipe '%s' not found." % self.name)
            return None

        self.id = result[0]['id']
        return self.id

    def load(self) -> None:
        """
        Loads recipe from db.
        """
        sql = "SELECT * FROM recipes WHERE "
        if self.id:
            sql += "id = ?"
            params = (self.id,)
        elif self.name:
            sql += "name = ?"
            params = (self.name,)
        else:
            raise Exception("Id or name of the recipe must be given.")

        result = db_read(sql, params)
        if not result:
            print("Recipe '%s' not found." % params[0])
            return

        # TODO udelat elegantneji
        self.id = result[0]['id']
        self.name = result[0]['name']
        self.servings = result[0]['servings']
        self.instructions = result[0]['instructions']
        self.source = result[0]['source']
        self.source_url = result[0]['source_url']

        sql = """SELECT * 
            FROM recipe_ingredients ri
            JOIN ingredients ON ri.ingredient_id = ingredients.id
            WHERE ri.recipe_id = ?
        """
        for ingredient in db_read(sql, (self.id,)):
            self.ingredients.append(RecipeIngredient(ingredient_name=ingredient["name"],
                                                     ingredient_id=ingredient["ingredient_id"],
                                                     amount=ingredient["amount"],
                                                     unit=ingredient["unit"]))

    def save(self) -> None:
        """
        Updates or creates new recipe in db.
        """
        # TODO pred ulozenim udelat load, aby se nesmazaly puvodni informace nebo ukladat jen vstupy
        if not self.name:
            raise Exception("Recipe has to have name.")

        if self.id:
            sql = "UPDATE recipes SET name = ?, servings = ?, instructions = ?, source = ?, source_url = ? WHERE id = ?"
            params = (self.name, self.servings, self.instructions, self.source, self.source_url, self.id)
        else:
            sql = "INSERT INTO recipes (name, servings, instructions, source, source_url) VALUES (?, ?, ?, ?, ?)"
            params = (self.name, self.servings, self.instructions, self.source, self.source_url)

        _, id = db_write(sql, params)
        if not self.id and id:
            print("New recipe created.")
            self.id = id
        else:
            print("Recipe updated.")


    def add_ingredients(self, ingredients: list[RecipeIngredient]) -> None:
        """
        Adds ingredients to the recipe.
        """
        if not self.id:
            self.get_id()

        sql = "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit) VALUES "
        sql_values = []
        sql_params = []

        for recipe_ingredient in ingredients:
            if not recipe_ingredient.ingredient_id:
                ingredient = Ingredient(name=recipe_ingredient.ingredient_name)
                recipe_ingredient.ingredient_id = ingredient.get_id_or_create()

            sql_values.append("(?, ?, ?, ?)")
            sql_params.extend([self.id, recipe_ingredient.ingredient_id, recipe_ingredient.amount, recipe_ingredient.unit.value])

        sql += ", ".join(sql_values)
        sql += " ON CONFLICT DO Update SET amount=excluded.amount, unit=excluded.unit"
        db_write(sql, tuple(sql_params))
        print("Ingredients added to the recipe.")

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


