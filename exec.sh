#!/bin/bash
exec gunicorn -b 0.0.0.0:$PORT -w 4 src.server:app
#exec python src/tests/test_index.py
