#!/bin/bash


# cd cs162-hc-feedback

git fetch && git reset origin/dev --hard

docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build