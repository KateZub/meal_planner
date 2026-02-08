#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException

import app.actions as actions
import app.common as common
from app.datatypes.recipe import NewRecipeEntry, Recipe, RecipeEntry, RecipeIngredient
from app.exceptions import NotFoundException

router = APIRouter(tags=["recipes"])


@router.get("/")
async def list_recipes(
    offset: int = 0, limit: int = 10, criterion: actions.RecipesCriterionType = "name", direction: actions.DirectionType = "asc"
) -> list[Recipe]:
    """
    Lists recipes
    """
    result = await actions.list_recipes(offset=offset, limit=limit, criterion=criterion, direction=direction)
    return result


@router.post("/", status_code=201)
async def create_recipe(recipe_entry: NewRecipeEntry) -> Recipe:
    """
    Creates new recipe
    """
    recipe = Recipe(**recipe_entry.dict(exclude_unset=True))
    try:
        await common.load(recipe)
    except NotFoundException:
        pass
    else:
        raise HTTPException(status_code=400, detail="Recipe already exists")

    await common.save(recipe)
    await common.load(recipe)
    return recipe


@router.get("/{recipe_id}/")
async def load_recipe(recipe_id: int) -> Recipe:
    """
    Returns recipe
    """
    recipe = Recipe(id=recipe_id)
    await common.load(recipe)
    return recipe


@router.put("/{recipe_id}/")
async def update_recipe(recipe_id: int, recipe_entry: RecipeEntry) -> Recipe:
    """
    Updates recipe
    """
    recipe = Recipe(id=recipe_id)
    await common.load(recipe)
    entry_data = recipe_entry.dict(exclude_unset=True)

    if entry_data.get("name"):
        try:
            await common.load(Recipe(name=entry_data["name"]))
        except NotFoundException:
            pass
        else:
            raise HTTPException(status_code=400, detail="Recipe with the same name already exists")

    new_recipe = recipe.model_copy(update=entry_data)
    await common.save(new_recipe)
    await common.load(new_recipe)
    return new_recipe


@router.put("/{recipe_id}/ingredients", status_code=204)
async def add_ingredients(recipe_id: int, ingredients: list[RecipeIngredient]) -> None:
    """
    Adds ingredients to the recipe. ingredient_name or ingredient_id must be given.
    """
    recipe = Recipe(id=recipe_id)
    await common.load(recipe)
    await common.add_entity_items(recipe, ingredients)


@router.delete("/{recipe_id}/ingredients", status_code=204)
async def remove_ingredients(recipe_id: int, ingredients: list[int] | list[str]) -> None:
    """
    Deletes ingredients from the recipe.
    @param ingredients  list of ingredients names or list of ingredients ids
    """
    recipe = Recipe(id=recipe_id)
    await common.load(recipe)
    await common.remove_entity_items(recipe, ingredients)
