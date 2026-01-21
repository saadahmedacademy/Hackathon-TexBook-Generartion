#!/bin/bash
PYTHONPATH=. uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --workers 1 --loop asyncio --http h11
