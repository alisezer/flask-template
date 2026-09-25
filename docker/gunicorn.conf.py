"""Gunicorn settings. Every value can be overridden with GUNICORN_CMD_ARGS."""

import multiprocessing
import os

bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
threads = int(os.environ.get("GUNICORN_THREADS", 2))
timeout = 30
graceful_timeout = 30
accesslog = "-"
errorlog = "-"
