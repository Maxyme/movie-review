#!/usr/bin/env bash

cd app
hypercorn -b 0.0.0.0:${PORT} "app:app"
