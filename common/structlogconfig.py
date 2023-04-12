import structlog


def log_config():
    log = structlog.get_logger()
    return log
