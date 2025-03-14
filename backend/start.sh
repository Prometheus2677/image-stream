#!/bin/bash

# Activate virtual environment (if applicable)
# source venv/bin/activate  # Uncomment if using a virtual environment

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
