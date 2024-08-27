from multiprocessing import cpu_count

wsgi_app = "dashboard_app:aplicacao()"

# The socket to bind
bind = "0.0.0.0:8501"

# Type Worker
worker_class = "gthread"

# The number of worker processes for handling requests
workers = cpu_count() * 2 + 1

# Threads
threads = cpu_count() * 2 + 1

# Load application code before the worker processes are forked
preload_app = True

# Timeout in seconds
timeout = 120

keepalive = 5

# Evitar erro no Docker
worker_tmp_dir = "/dev/shm"

# The granularity of Error log outputs
loglevel = "info"
