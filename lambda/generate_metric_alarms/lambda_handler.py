"""Handler."""
import logging
import os

from generate_metric_alarms import process_alert

LOG = logging.getLogger('generate_metric_alarms')
LOG.setLevel(getattr(logging, str(os.getenv('LOGLEVEL', 'ERROR'))))


def lambda_handler(event, context):
    """Handler."""
    # variables = ['TOKEN', 'TOPIC_ARN', 'DATABASE_URL',
    #              'DATABASE_NAME', 'COLLECTION_NAME']
    # for var in variables:
    #     if not str(os.getenv(var, '')):
    #         LOG.error('Missing variable %s, aborting request', var)
    #         raise ValueError(f'Missing variable {var}, aborting request')

    return process_alert(event)


if __name__ == "__main__":
    STDERRLOGGER = logging.StreamHandler()
    STDERRLOGGER.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    LOG.addHandler(STDERRLOGGER)

    lambda_handler(False, False)
