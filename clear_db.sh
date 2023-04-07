#!/bin/bash
docker compose down -v &&
docker compose up -d db
sleep 5
alembic upgrade head
inv create-sports
inv get-coach-subscription
