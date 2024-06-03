#!/usr/bin/env bash

redis-server &
~/.local/bin/poetry run rq worker --with-scheduler &
~/.local/bin/poetry run flask --app app run --host 0.0.0.0