from app import create_app
from app.logger import logger
from app.config import DEBUG

if __name__ == "__main__":
    logger.info("Starting Flask server...")
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=DEBUG)
