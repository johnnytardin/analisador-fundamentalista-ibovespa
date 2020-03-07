import logging
import logging.handlers


def config_log(pathlogprefix):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # cria o handler info
    handleri = logging.handlers.RotatingFileHandler(
        f"{pathlogprefix}-info.log", maxBytes=52428800, backupCount=5
    )
    handleri.setLevel(logging.INFO)

    # cria o handler error
    handlere = logging.handlers.RotatingFileHandler(
        f"{pathlogprefix}-error.log", maxBytes=52428800, backupCount=5
    )
    handlere.setLevel(logging.ERROR)
    handlere.setLevel(logging.CRITICAL)

    # create a logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handleri.setFormatter(formatter)
    handlere.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handleri)
    logger.addHandler(handlere)

    return logger
