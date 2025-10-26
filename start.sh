#!/bin/bash
set -e
set -x

PORT=${PORT:-8000}

uvicorn app.api.assistant_api:app --host 0.0.0.0 --port 8002

chainlit run main.py --host 0.0.0.0 --port $PORT