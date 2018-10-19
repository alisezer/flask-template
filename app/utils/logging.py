"""Used for creating handlers for the app logger. Two handles are created:
the first one logs to a file, and is a rotating handler. The second one will
be the client logger which is what you see on the terminal. Their log levels
are defined through .env file. These handlers are imported and attached to the
app during app initiation stage."""

from logging.handlers import RotatingFileHandler
from logging import StreamHandler
from pathlib import Path
import logging
import os

# Logger setup
# Set file paths for logger
log_folder_path = str(Path('logs').absolute())

# Creates logs folder if not existent
if not os.path.exists(log_folder_path):
    os.makedirs(log_folder_path)

log_file_path = os.path.join(log_folder_path, 'log.out')

# Configure logger format
log_fmt = '%(threadName)s - %(asctime)s - %(name)s - ' \
          '%(levelname)s - %(message)s'

logger_formatter = logging.Formatter(log_fmt)

# Sets up rotating file handler for file output
file_logger = RotatingFileHandler(log_file_path, maxBytes=1024*1024*10,backupCount=5)
file_logger.setLevel(logging.DEBUG)
file_logger.setFormatter(logger_formatter)

# Set up stream handler for client output
client_logger = StreamHandler()
client_logger.setLevel(logging.INFO)
client_logger.setFormatter(logger_formatter)
