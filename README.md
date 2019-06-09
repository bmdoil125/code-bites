[![Build Status](https://travis-ci.org/bmdoil/code-bites.svg?branch=master)](https://travis-ci.org/bmdoil/code-bites)

Grading Branch for CS493 Final Project

Testing setup:

export BASE_URL=http://localhost

docker-compose up -d --build
docker-compose exec server python manage.py recreate_db
docker-compose exec server python manage.py add_test_data
docker-compose exec server python manage.py test
