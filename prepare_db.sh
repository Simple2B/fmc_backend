#!/bin/bash
echo Clearing up database
docker compose down -v &&
echo Starting db
docker compose up -d db &&
sleep 6
echo Applying migrations
alembic upgrade head &&

invoke create-sports