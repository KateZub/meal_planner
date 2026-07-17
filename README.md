# 🥗 Meal Planner & Shopping List Generator

A Python project for creating weekly meal plans from recipes and automatically generating a shopping list.

## 🚀 Features
🍽️ **Recipe-based logic**  
Meals are created from structured recipe data (ingredients, names, etc.).

📅 **Weekly meal planning**  
Generate a meal plan based on available recipes.

🛒 **Automatic shopping list**  
Collect all required ingredients from planned meals into one consolidated list.

## 🛠️ Prerequisites

Before starting the application, create a `.env` file in the project root with your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

Without this environment variable, the application will not be able to communicate with the OpenAI API.

## 🐳 Run using Docker
1. Create docker image:
    ```bash
    docker build --target release -t meal_planner .
    ```
2. Run container:
    ```bash
   docker run --env-file .env -p 8000:8000 meal_planner
    ```

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

## 📘 Interactive API Documentation (Swagger UI)

Now go to <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noopener noreferrer">http://127.0.0.1:8000/docs</a>. You will see the automatic **interactive API documentation**.

<img width="900" alt="image" src="https://github.com/user-attachments/assets/d3f0080f-6d22-4cb9-b076-a50ceea798c1" />

## 🌐 Frontend (React/Vite)

A basic React frontend now lives in the `frontend/` folder.

Run it locally:

```bash
cd frontend
npm install
npm run dev
```

The frontend uses Vite's dev server and proxies `/api/*` requests to your FastAPI backend running on `http://127.0.0.1:8000`.

## 🐳 Docker

You can run the backend and frontend together with Docker Compose:

```bash
docker compose up --build
```

Then open:

- Frontend: http://127.0.0.1:5173/
- Backend API docs: http://127.0.0.1:8000/docs

If you want to use the OpenAI-powered recipe import feature, provide an `OPENAI_API_KEY` in your environment before starting the containers.

## ⭐ Future Improvements

- Nutrition tracking
- Web interface
- Automatically created recipe from given webpage url
