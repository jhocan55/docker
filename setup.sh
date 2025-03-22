#!/bin/bash
mkdir -p logs
docker compose build
docker compose up --abort-on-container-exit
cp logs/api_test.log ./log.txt