#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field
from typing import ClassVar

class Ingredient(BaseModel):
    entity_name: ClassVar[str] = "ingredient"
    entity_db_table: ClassVar[str] = "ingredients"

    name: str = Field(default=None, min_length=3)
    id: int = None

    def load_from_dict(self, attributes) -> None:
        """
        Loads Ingredient from dict.
        """
        self.id = attributes["id"]
        self.name = attributes["name"]

    def get_dict_to_save(self) -> dict:
        """
        Returns dict of the Ingredient for saving to db.
        """
        return self.dict(exclude={'id'})
