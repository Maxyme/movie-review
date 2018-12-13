#!/usr/bin/env bash

cd app
gunicorn "app:create_app()" --daemon
python worker.py