#!/bin/bash




if ! [ -x "$(command -v docker)" ]; then
    echo "Error: docker is not installed"
    exit 1
elif ! [ -x "$(command -v docker-compose)" ]; then
    echo "Error: docker-compose is not installed"
    exit 1
elif ! [ -x "$(command -v python)" ]; then
    echo "Error: python is not installed"
    exit 1
fi

export BASE_URL=http://localhost

if [ "$(docker-compose -f docker-compose.yml up -d --build)" -ne 0 ]; then
    echo "Build failed."
    exit 1
fi

docker-compose -f docker-compose.yml exec server python manage.py recreate_db
docker-compose -f docker-compose.yml exec server python manage.py add_test_data
docker-compose -f docker-compose.yml exec server python manage.py test
docker-compose down