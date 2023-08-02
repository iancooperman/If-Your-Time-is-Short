# Various utility functions
import logging

# A function that takes a function, runs it, and if it errors, logs it and returns None.
def simple_try(func, log):
    try:
        return func()
    except Exception as e:
        logging.debug(e)
        return None
    
def logging_config() -> None:

    log: logging.Logger = logging.getLogger()
    log.setLevel(logging.DEBUG)

    formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s')

    fh: logging.FileHandler = logging.FileHandler('iytis.log', mode='w', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)    
    log.addHandler(fh)

    ch: logging.StreamHandler = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)