#!/usr/bin/env bash

cd app
hypercorn -b 127.0.0.1:8000 "app:create_app()"
