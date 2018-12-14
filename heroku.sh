#!/usr/bin/env bash

cd app
hypercorn "app:create_app()"
