#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from typing import ClassVar, List

from pydantic import BaseModel, Field, HttpUrl

from app.exceptions import MissingIdOrNameException


class Unit(Enum):
    GRAM = "g"
    MILLILITER = "ml"
    PIECE = "ks"
    TEASPOON = "ČL"
    TABLESPOON = "PL"
    PINCH = "špetka"


class RecipeIngredient(BaseModel):
    amount: int
    unit: Unit
    ingredient_name: str = None
    ingredient_id: int = None


class NewRecipeEntry(BaseModel):
    name: str = Field(min_length=3)
    servings: int = Field(default=1, ge=1)
    instructions: str = None
    source: str = None
    source_url: HttpUrl = None


class RecipeEntry(NewRecipeEntry):
    name: str = Field(default=None, min_length=3)


class Recipe(RecipeEntry):
    entity_name: ClassVar[str] = "recipe"
    entity_db_table: ClassVar[str] = "recipes"
    entity_items_sql: ClassVar[
        str
    ] = """SELECT *
            FROM recipe_ingredients ri
            JOIN ingredients ON ri.ingredient_id = ingredients.id
            WHERE ri.recipe_id = ?
        """

    id: int = None
    ingredients: list[RecipeIngredient] = Field(default_factory=list)

    def load_from_dict(self, attributes: dict, ingredients: List[dict]) -> None:
        """
        Loads Recipe from dict.
        """
        self.id = attributes["id"]
        self.name = attributes["name"]
        self.servings = attributes["servings"]
        self.instructions = attributes["instructions"]
        self.source = attributes["source"]
        self.source_url = attributes["source_url"]

        self.ingredients = []
        for ingredient in ingredients:
            self.ingredients.append(
                RecipeIngredient(
                    ingredient_name=ingredient["name"],
                    ingredient_id=ingredient["ingredient_id"],
                    amount=ingredient["amount"],
                    unit=ingredient["unit"],
                )
            )

    def get_dict_to_save(self) -> dict:
        """
        Returns dict of the Recipe for saving to db.
        """
        return self.dict(exclude={"ingredients", "id"})

    @staticmethod
    def get_sql_and_params_for_new_items(entity_attributes: dict, ingredients: List[RecipeIngredient]) -> tuple:
        """
        Returns sql and params for adding new ingredients to the recipe.
        """
        if not entity_attributes.get("id"):
            raise Exception("Id not in entity_attributes.")

        sql = "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit) VALUES "
        sql_values = []
        sql_params = []

        for recipe_ingredient in ingredients:
            if not recipe_ingredient.ingredient_id:
                raise MissingIdOrNameException("ingredient")

            sql_values.append("(?, ?, ?, ?)")
            sql_params.extend(
                [entity_attributes["id"], recipe_ingredient.ingredient_id, recipe_ingredient.amount, recipe_ingredient.unit.value]
            )

        sql += ", ".join(sql_values)
        sql += " ON CONFLICT DO Update SET amount=excluded.amount, unit=excluded.unit"

        return sql, tuple(sql_params)

    @staticmethod
    def get_sql_and_params_for_items_to_remove(entity_id: int, ingredients: list[str] | list[int]) -> tuple:
        """
        Returns sql for removing ingredients from the recipe.
        """
        if isinstance(ingredients[0], int):
            sql = f"""DELETE FROM recipe_ingredients WHERE recipe_id = ? AND ingredient_id IN ({", ".join("?" * len(ingredients))})"""
        else:
            sql = f"""
                DELETE FROM recipe_ingredients
                WHERE recipe_id = ? AND ingredient_id IN
                 (SELECT id FROM ingredients WHERE name IN ({", ".join("?" * len(ingredients))}))
            """

        return sql, tuple([entity_id] + ingredients)
