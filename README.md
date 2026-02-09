# 🥗 Meal Planner & Shopping List Generator

A Python project for creating weekly meal plans from recipes and automatically generating a shopping list.

## 🚀 Features
🍽️ **Recipe-based logic**  
Meals are created from structured recipe data (ingredients, names, etc.).

📅 **Weekly meal planning**  
Generate a meal plan based on available recipes.

🛒 **Automatic shopping list**  
Collect all required ingredients from planned meals into one consolidated list.

## 🐳 Run using Docker
1. Create docker image:
    ```bash
    docker build -t meal_planner .
    ```
2. Run container:
    ```bash
   docker run -p 8000:8000 meal_planner
    ```
3. Now go to http://127.0.0.1:8000/docs. You will see the automatic **interactive API documentation**.


## 💻 Run locally

Make sure you have **Python 3.x** installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/KateZub/meal_planner.git
   ```
2. Navigate into the project directory:
    ```bash
    cd meal_planner
    ```
3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
4. Run the live server
   ```bash
   fastapi dev app/main.py
    ```
   In the output, there's a line with something like:
    ```
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    ```
    That line shows the URL where your app is being served, in your local machine.

5. Now go to http://127.0.0.1:8000/docs. You will see the automatic **interactive API documentation**.

## ⭐ Future Improvements

- Nutrition tracking
- Web interface
- Automatically created recipe from given webpage url
