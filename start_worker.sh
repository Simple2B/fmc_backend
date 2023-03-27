#!/bin/bash
echo Starting server
poetry run celery -A app.controller.celery worker -B --loglevel=INFO
