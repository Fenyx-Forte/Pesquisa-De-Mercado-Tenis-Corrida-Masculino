wsgi_app = "dashboard_app:aplicacao()"

# The socket to bind
bind = "127.0.0.1:8051"

# Type Worker
worker_class = "sync"

# The number of worker processes for handling requests
workers = 3

# Threads
threads = 1

# Load application code before the worker processes are forked
preload_app = False

# Timeout in seconds
timeout = 30

# The granularity of Error log outputs
loglevel = "info"

pidfile = "gunicorn.pid"
