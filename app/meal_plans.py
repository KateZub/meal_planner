from fastapi import APIRouter, HTTPException

from app import actions, common
from app.datatypes.meal_plan import MealPlan, MealPlanEntry, MealPlanRecipe, NewMealPlanEntry
from app.datatypes.recipe import RecipeIngredient
from app.exceptions import NotFoundException

router = APIRouter(tags=["meal plans"])


@router.get("/")
async def list_meal_plans(
    offset: int = 0, limit: int = 10, criterion: actions.MealPlanCriterionType = "name", direction: actions.DirectionType = "asc"
) -> list[MealPlan]:
    """
    Lists meal plans
    """
    result = await actions.list_meal_plans(offset=offset, limit=limit, criterion=criterion, direction=direction)
    return result


@router.post("/", status_code=201)
async def create_meal_plan(meal_plan_entry: NewMealPlanEntry) -> MealPlan:
    """
    Creates new meal plan
    """
    meal_plan = MealPlan(**meal_plan_entry.dict(exclude_unset=True))
    try:
        await common.load(meal_plan)
    except NotFoundException:
        pass
    else:
        raise HTTPException(status_code=400, detail="Meal plan already exists")

    await common.save(meal_plan)
    await common.load(meal_plan)
    return meal_plan


@router.get("/{meal_plan_id}/")
async def load_meal_plan(meal_plan_id: int) -> MealPlan:
    """
    Returns meal plan
    """
    meal_plan = MealPlan(id=meal_plan_id)
    await common.load(meal_plan)
    return meal_plan


@router.put("/{meal_plan_id}/")
async def update_meal_plan(meal_plan_id: int, meal_plan_entry: MealPlanEntry) -> MealPlan:
    """
    Updates meal plan
    """
    meal_plan = MealPlan(id=meal_plan_id)
    await common.load(meal_plan)
    entry_data = meal_plan_entry.dict(exclude_unset=True)

    if entry_data.get("name"):
        try:
            await common.load(MealPlan(name=entry_data["name"]))
        except NotFoundException:
            pass
        else:
            raise HTTPException(status_code=400, detail="Meal plan with the same name already exists")

    new_meal_plan = meal_plan.model_copy(update=entry_data)
    await common.save(new_meal_plan)
    await common.load(new_meal_plan)
    return new_meal_plan


@router.put("/{meal_plan_id}/recipes", status_code=204)
async def add_recipes(meal_plan_id: int, recipes: list[MealPlanRecipe]) -> None:
    """
    Adds recipes to the meal plan. recipe_name or recipe_id must be given.
    """
    meal_plan = MealPlan(id=meal_plan_id)
    await common.load(meal_plan)
    await common.add_entity_items(meal_plan, recipes)


@router.delete("/{meal_plan_id}/recipes", status_code=204)
async def remove_recipes(meal_plan_id: int, recipes: list[int] | list[str]) -> None:
    """
    Deletes recipes from the meal plan.
    @param recipes  list of recipes names or list of recipes ids
    """
    meal_plan = MealPlan(id=meal_plan_id)
    await common.load(meal_plan)
    await common.remove_entity_items(meal_plan, recipes)


@router.get("/{meal_plan_id}/shopping_list/")
async def get_shopping_list(meal_plan_id: int) -> list[RecipeIngredient]:
    """
    Returns shopping list for the meal plan
    """
    meal_plan = MealPlan(id=meal_plan_id)
    result = await actions.generate_shopping_list(meal_plan)
    return result
