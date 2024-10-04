#!/bin/bash

cd /home/johnny/ckjz
source .venv/bin/activate

TODAY=$(date "+%Y%m%d")
TIMESTAMP=$(date | tr -d "[[:punct:]]" | tr -d ' ')

PORT=${1:-8050}
NUM_WORKERS=${8:-9}
THREADS=${8:-8}

GUNICORN_PROD_LOGS="/home/johnny/ckjz/gunicorn/logs/${TODAY}"
mkdir -p $GUNICORN_PROD_LOGS

#exec gunicorn \
#  --bind unix:/tmp/gunicorn.sock \
#  -w $NUM_WORKERS \
#  --worker-class uvicorn.workers.UvicornWorker \
#  --threads $THREADS \
#  --name "ckjz-${TODAY}" \
#  --max-requests 100 \
#  --max-requests-jitter 10 \
#  --access-logfile "${GUNICORN_PROD_LOGS}/${TODAY}.access.log" \
#  ckjz.main:app

exec uvicorn \
  --workers 4 \
  --host 0.0.0.0 \
  --port 8000 \
  ckjz.main:app

