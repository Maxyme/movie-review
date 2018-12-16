#!/usr/bin/env bash

cd app
hypercorn -b 0.0.0.0:${PORT} --worker-class uvloop "app:app"
