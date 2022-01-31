import datetime
import logging
import os
import sys

"""
All lambda methods use this loging config.
Provides a single place where all log config/level/formatting is setup so that one
can see source file, line numbers, and any other desired log fields. 

Level           When it’s used
-------------------------------------------------------------------------------------------------------------
DEBUG           Detailed information, typically of interest only when diagnosing problems.
INFO            Confirmation that things are working as expected.
WARNING         An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
ERROR           Due to a more serious problem, the software has not been able to perform some function.
CRITICAL        A serious error, indicating that the program itself may be unable to continue running.

%(name)s            Name of the logger (logging channel)
%(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                    WARNING, ERROR, CRITICAL)
%(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                    "WARNING", "ERROR", "CRITICAL")
%(pathname)s        Full pathname of the source file where the logging
                    call was issued (if available)
%(filename)s        Filename portion of pathname
%(module)s          Module (name portion of filename)
%(lineno)d          Source line number where the logging call was issued
                    (if available)
%(funcName)s        Function name
%(created)f         Time when the LogRecord was created (time.time()
                    return value)
%(asctime)s         Textual time when the LogRecord was created
%(msecs)d           Millisecond portion of the creation time
%(relativeCreated)d Time in milliseconds when the LogRecord was created,
                    relative to the time the logging module was loaded
                    (typically at application startup time)
%(thread)d          Thread ID (if available)
%(threadName)s      Thread name (if available)
%(process)d         Process ID (if available)
%(message)s         The result of record.getMessage(), computed just as
                    the record is emitted
"""
if not os.path.exists('logs/'):
    os.makedirs("logs/")
today = datetime.date.today().strftime('%Y%m%d')
log_file = f'logs/{today}.log'

# Cleanup Loggers
logger = logging.getLogger()
for h in logger.handlers:
    logger.removeHandler(h)

# Set Standard Output Logging
stdout_handler = logging.StreamHandler(sys.stdout)

# Set File Output Logging
file_handler = logging.FileHandler(log_file)

# Load the two logging outputs with formating
handlers = [file_handler, stdout_handler]
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s \t %(process)d \t %(thread)d \t %(levelname)-8s \t %(name)s \t [%(filename)s:%(lineno)d] \t %(message)s',
    handlers=handlers
)

# Suppress the more verbose modules
logging.getLogger('__main__').setLevel(logging.DEBUG)
logging.getLogger('requests_oauthlib').setLevel(logging.INFO)