#!/bin/bash

# Wait for MySQL to be ready (without netcat)
# while ! python -c "import socket; import os; sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); sock.settimeout(1); result = sock.connect_ex((os.getenv('DB_HOST'), int(os.getenv('DB_PORT')))); sock.close(); exit(result)"; do
#   echo "Waiting for MySQL..."
#   sleep 2
# done

# echo "MySQL is ready"

# Run migrations (jika menggunakan alembic)
# if [ -f "alembic.ini" ]; then
#     alembic upgrade head
# fi

# Start the application
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload --reload-exclude "mariadb/*"