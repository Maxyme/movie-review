#!/usr/bin/env bash

cd app
hypercorn -b 127.0.0.1:${PORT} "app:create_app()"
