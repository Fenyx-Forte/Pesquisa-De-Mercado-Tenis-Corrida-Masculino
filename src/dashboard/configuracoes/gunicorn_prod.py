from multiprocessing import cpu_count

wsgi_app = "dashboard_app:aplicacao()"

# The socket to bind
bind = "0.0.0.0:8501"

# Type Worker
worker_class = "sync"

# The number of worker processes for handling requests
workers = cpu_count() * 2 + 1

# Threads
threads = 1

# Load application code before the worker processes are forked
preload_app = False

# Timeout in seconds
timeout = 120

# The number of seconds to wait for requests on a Keep-Alive connection.
# sync worker does not support persistent connections and will ignore this option.
# keepalive = 5

# Evitar erro no Docker
worker_tmp_dir = "/dev/shm"

# The granularity of Error log outputs
loglevel = "info"

# Ver como melhorar a questao do pidfile
pidfile = "gunicorn.pid"
