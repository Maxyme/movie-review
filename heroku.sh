#!/usr/bin/env bash

cd app
gunicorn app:app --daemon
python worker.py