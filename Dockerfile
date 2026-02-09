FROM python:3-alpine

WORKDIR /meal_planner

COPY requirements.txt /requirements.txt

RUN pip3 install --no-cache-dir -r /requirements.txt

COPY app /meal_planner/app
RUN mkdir -p /meal_planner/data/
COPY data/meal_planner.db /meal_planner/data/

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]
