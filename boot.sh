#!/bin/bash
source venv/bin/activate
exec gunicorn --config ./conf/gunicorn_conf.py application:app