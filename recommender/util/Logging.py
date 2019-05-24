def mkdir_p(path):
    import os
    import errno

    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


def init_logger(name, max_MBbyte=100, log_level=None, log_file=None):
    import logging.handlers
    import os

    logger = logging.getLogger(name)
    if log_level:
        logger.setLevel(log_level)
    else:
        logger.setLevel(logging.INFO)

    formatter = logging.\
        Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    if not len(logger.handlers):
        if log_file:
            mkdir_p(os.path.dirname(log_file))
            fh = logging.handlers.\
                RotatingFileHandler(log_file,
                                    mode='w',
                                    maxBytes=max_MBbyte * 1024 * 1024,
                                    backupCount=2)

            fh.setFormatter(formatter)
            logger.addHandler(fh)
        else:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            logger.addHandler(ch)
    return logger
