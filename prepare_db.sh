#!/bin/bash
echo Clearing up database
docker compose down -v &&
echo Starting db
docker compose up -d db &&
sleep 6
echo Applying migrations
alembic upgrade head &&
echo Creating data
invoke create-sports &&
invoke get-coach-subscription
invoke dummy-data
invoke create-real-coaches-data
invoke create-sessions