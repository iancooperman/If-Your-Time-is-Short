# Various utility functions
import logging

# A function that takes a function, runs it, and if it errors, logs it and returns None.
def simple_try(func, logger):
    try:
        return func()
    except Exception as e:
        logger.debug(e)
        return None
    
def logger_init() -> logging.Logger:

    logger: logging.Logger = logging.getLogger('iytis_log')
    logger.setLevel(logging.DEBUG)

    formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s')

    fh: logging.FileHandler = logging.FileHandler('iytis.log', mode='w', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)    
    logger.addHandler(fh)

    ch: logging.StreamHandler = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.propagate = False

    return logger