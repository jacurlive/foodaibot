#!/bin/bash
cd /home/jack/www/foodaibot
source venv/bin/activate
DATABASE_URL="postgresql+asyncpg://foodai:foodai_password@localhost:5436/foodai_db" \
  uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
