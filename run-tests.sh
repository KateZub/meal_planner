#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"

sqlite3 ${DIR}/data/meal_planner.db .schema > ${DIR}/schema.sql
sqlite3 ${DIR}/test_db.db < schema.sql
echo "new db created"

docker build . -t meal_planner_test
docker run --rm -i \
  -v `pwd`/app:/meal_planner/app \
  -v ${DIR}/test_db.db:/meal_planner/data/meal_planner.db --name meal_planner-test meal_planner_test

rm ${DIR}/schema.sql
rm ${DIR}/test_db.db
