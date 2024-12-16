#!/bin/bash


# cd cs162-hc-feedback

git fetch && git reset origin/dev --hard

docker compose -f docker-compose.dev.yml down
docker compose -f docker-compose.dev.yml up -d --build