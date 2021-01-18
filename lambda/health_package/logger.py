""" Define a shared logger instance """
import os
import logging

logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("nose").setLevel(logging.WARNING)

LOG = logging.getLogger("health_monitor")
LOG.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG")))
