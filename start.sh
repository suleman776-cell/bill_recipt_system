#!/bin/bash
export FLASK_APP=app.py
export FLASK_ENV=production
exec gunicorn --bind 0.0.0.0:$PORT app:app
