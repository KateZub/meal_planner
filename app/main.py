#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import MissingIdOrNameException, NotFoundException
from app.ingredients import router as ingredients_router
from app.meal_plans import router as meal_plans_router
from app.recipes import router as recipes_router

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Meal planner", description="App for creating meal plans and generating shopping lists from them.")
app.include_router(ingredients_router, prefix="/ingredients")
app.include_router(recipes_router, prefix="/recipes")
app.include_router(meal_plans_router, prefix="/meal_plans")


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": f"Item '{exc.identifier}' not found."},
    )


@app.exception_handler(MissingIdOrNameException)
async def missing_exception_handler(request: Request, exc: MissingIdOrNameException):
    return JSONResponse(
        status_code=404,
        content={"message": f"Missing {exc.item} id or name."},
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
