#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field

from db import db_read, db_write

class Ingredient(BaseModel):
    name: str = Field(default=None, min_length=3)
    id: int = None

    def create(self) -> None:
        """
        Creates ingredient in db.
        """
        if self.id:
            return

        if not self.name:
            raise Exception('Ingredient has no name.')

        sql = "INSERT INTO ingredients (name) VALUES (?)"
        _, self.id = db_write(sql, (self.name,))
        print("new ingredient created, id: ", self.id)


    def get_id_or_create(self) -> int:
        """
        Returns id of the ingredient. If it's not in db, it creates it.
        """
        if self.id:
            return self.id

        if not self.name:
            raise Exception('Ingredient has no name.')

        sql = "SELECT id FROM ingredients WHERE name = ?"
        result = db_read(sql, (self.name,))
        if not result:
            self.create()
        else:
            self.id = result[0]['id']

        return self.id

