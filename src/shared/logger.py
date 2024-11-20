import logging

# Configure logging
logging.basicConfig(
    filename='log.txt',
    filemode='w',  # Write new file every make run
    format='%(name)s - %(message)s',
    level=logging.INFO
)

# Example usage
# logging.info("This is an info message.")
# logging.debug("This is a debug message.")
# logging.error("This is an error message.")

