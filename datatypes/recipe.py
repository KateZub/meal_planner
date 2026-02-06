#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from pydantic import BaseModel, Field
from typing import List, ClassVar

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
    entity_name: ClassVar[str] = "recipe"
    entity_db_table: ClassVar[str] = "recipes"

    name: str = Field(default=None, min_length=3)
    servings: int = Field(default=1, ge=1)
    id: int = None
    instructions: str = None
    source: str = None
    source_url: str = None
    ingredients: list[RecipeIngredient] = Field(default_factory=list)

    def load_from_dict(self, attributes: dict, ingredients: List[dict]) -> None:
        """
        Loads Recipe from dict.
        """
        self.id = attributes['id']
        self.name = attributes['name']
        self.servings = attributes['servings']
        self.instructions = attributes['instructions']
        self.source = attributes['source']
        self.source_url = attributes['source_url']

        for ingredient in ingredients:
            self.ingredients.append(RecipeIngredient(ingredient_name=ingredient["name"],
                                                     ingredient_id=ingredient["ingredient_id"],
                                                     amount=ingredient["amount"],
                                                     unit=ingredient["unit"]))

    def get_dict_to_save(self) -> dict:
        """
        Returns dict of the Recipe for saving to db.
        """
        # TODO pripravit ingredients na ulozeni
        return self.dict(exclude={'ingredients', 'id'})

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
                raise Exception("Missing ingredient id.")

            sql_values.append("(?, ?, ?, ?)")
            sql_params.extend([entity_attributes["id"], recipe_ingredient.ingredient_id, recipe_ingredient.amount, recipe_ingredient.unit.value])

        sql += ", ".join(sql_values)
        sql += " ON CONFLICT DO Update SET amount=excluded.amount, unit=excluded.unit"

        return sql, tuple(sql_params)
