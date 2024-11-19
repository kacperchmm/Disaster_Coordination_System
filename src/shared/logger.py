import logging

# Configure logging
# Configure logging
logging.basicConfig(
    filename='log.txt',
    filemode='a',  # Append mode
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Replace print statements with logging
# logging.info("This is an info message.")
# logging.debug("This is a debug message.")
# logging.error("This is an error message.")

