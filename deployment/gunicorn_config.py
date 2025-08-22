"""
Gunicorn configuration for production deployment
"""

import os
import multiprocessing

# Server socket
bind = f"0.0.0.0:{os.getenv('FLASK_PORT', 5000)}"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 300  # Increased for long-running AI operations
keepalive = 2
max_requests = 1000
max_requests_jitter = 50

# Restart workers after this many requests, with up to 50 jitter
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "agentic-focus-group-workflow"

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
# keyfile = None
# certfile = None