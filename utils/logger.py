import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),  # Logs to the console
        logging.FileHandler('output/app.log')  # Logs to a file
    ]
)

# Create a logger object
logger = logging.getLogger(__name__)
