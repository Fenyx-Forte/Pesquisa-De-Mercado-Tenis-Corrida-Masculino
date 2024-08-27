wsgi_app = "dashboard_app:aplicacao()"

# The socket to bind
bind = "127.0.0.1:8051"

# The number of worker processes for handling requests
workers = 3

# Threads
threads = 1

# Restart workers when code changes (development only!)
# reload = True

# Timeout in seconds
timeout = 30

preload_app = True

# The granularity of Error log outputs
loglevel = "info"
