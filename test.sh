#!/bin/bash

fails=""

inspect() {
    if [ $1 -ne 0 ]; then
        fails="${fails} $2"
    fi
}

docker-compose up -d --build
docker-compose exec server python manage.py test
inspect $? server
#docker-compose exec server flake8 project
# inspect $? server-lint
docker-compose exec client npm test -- --coverage
inspect $? client
docker-compose down


# integration testing
#docker-compose -f docker-compose-prod.yml up -d --build
#docker-compose -f docker-compose-prod.yml exec server python manage.py recreate_db
#./node_modules/.bin/cypress run --config baseUrl=http://localhost
#inspect $? e2e
#docker-compose -f docker-compose-prod.yml down

if [ -n "${fails}" ]; then
    echo "Tests failed: ${fails}"
    exit 1
else
    echo "Tests passed"
    exit 0
fi