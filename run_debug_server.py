import uvicorn
import sys
import os
import logging

# Add src to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    try:
        logging.info("Attempting to start uvicorn server...")
        uvicorn.run("src.backend.main:app", host="127.0.0.1", port=8000, workers=1, loop="asyncio", http="h11")
        logging.info("Uvicorn server started successfully.")
    except Exception as e:
        logging.error("Failed to start uvicorn server", exc_info=True)
        # Write error to a file to be sure it's captured
        with open("server_startup_error.log", "w") as f:
            f.write(f"Error: {e}\n")
            import traceback
            traceback.print_exc(file=f)
