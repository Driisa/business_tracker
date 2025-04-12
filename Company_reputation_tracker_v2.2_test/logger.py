import logging
import os
import sys
from datetime import datetime
from functools import wraps

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure the main logger
log_file = os.path.join(logs_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')

# Create a custom formatter that includes timestamp, level, and module information
class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Add the timestamp in a readable format
        record.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return super().format(record)

# Configure the logger
logger = logging.getLogger('company_tracker')
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = CustomFormatter('%(timestamp)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s')

# Add formatter to handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Decorator for logging function calls
def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        module_name = func.__module__
        
        # Log function entry
        logger.info(f"Starting {func_name}")
        
        try:
            # Call the original function
            result = func(*args, **kwargs)
            
            # Log function exit
            logger.info(f"Completed {func_name} successfully")
            
            return result
        except Exception as e:
            # Log the exception
            logger.error(f"Error in {func_name}: {str(e)}")
            raise
    
    return wrapper

# Function to get the logger
def get_logger():
    return logger

# Log application startup
def log_startup():
    logger.info("=== Application Started ===")
    logger.info(f"Log file: {log_file}")

# Log application shutdown
def log_shutdown():
    logger.info("=== Application Shutdown ===")

# Log a general message
def log_info(message):
    logger.info(message)

# Log a warning message
def log_warning(message):
    logger.warning(message)

# Log an error message
def log_error(message, exc_info=None):
    if exc_info:
        logger.error(message, exc_info=exc_info)
    else:
        logger.error(message)

# Log a debug message
def log_debug(message):
    logger.debug(message)

# For testing
if __name__ == "__main__":
    log_startup()
    log_info("This is a test info message")
    log_warning("This is a test warning message")
    log_error("This is a test error message")
    log_shutdown()