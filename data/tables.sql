CREATE TABLE ingredients (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    UNIQUE (name)
);

CREATE TABLE recipes (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    servings INTEGER NOT NULL DEFAULT 1,
    instructions TEXT DEFAULT NULL,
    source TEXT DEFAULT NULL,
    source_url TEXT DEFAULT NULL,
    UNIQUE (name)
);

CREATE TABLE recipe_ingredients (
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    unit TEXT CHECK(unit in ('g', 'ml', 'ks', 'ČL', 'PL', 'špetka')),
    UNIQUE (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id)
        REFERENCES recipes (id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
    FOREIGN KEY (ingredient_id)
        REFERENCES ingredients (id)
            ON DELETE RESTRICT
            ON UPDATE NO ACTION
);

CREATE TABLE meal_plan (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    default_servings INTEGER DEFAULT 1,
    UNIQUE (name)
);

CREATE TABLE meal_plan_recipes (
    meal_plan_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    weekday TEXT CHECK (weekday in ('pondělí', 'úterý', 'středa', 'čtvrtek', 'pátek', 'sobota', 'neděle')),
    meal_type TEXT CHECK (meal_type in ('snídaně', 'oběd', 'večeře', 'svačina')),
    servings INTEGER NOT NULL,
    UNIQUE(meal_plan_id, recipe_id, weekday, meal_type),
    FOREIGN KEY (meal_plan_id)
        REFERENCES meal_plan (id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
    FOREIGN KEY (recipe_id)
        REFERENCES recipes (id)
            ON DELETE SET NULL
            ON UPDATE NO ACTION
);
