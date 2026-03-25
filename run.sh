#!/bin/bash
# Launch MD2PDF local web app
cd "$(dirname "$0")"

# Create venv if it doesn't exist
if [ ! -d .venv ]; then
  echo "Setting up virtual environment..."
  python3 -m venv .venv
  .venv/bin/pip install -q flask weasyprint
fi

echo "Starting MD2PDF at http://localhost:8787"
open http://localhost:8787 &
.venv/bin/python3 server.py
