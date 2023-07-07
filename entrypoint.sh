#! /usr/bin/env bash

alembic upgrade head
gunicorn -c ./gunicorn.conf.py main:app