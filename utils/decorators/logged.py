import functools
import logging


def logged(
    func=None,
    *,
    level=logging.DEBUG,
    name=None,
    message=None,
    func_name=None,
):
    """
    A decorator to print logs
    :param func: Function to be decorated
    :param level: Log level
    :param name: Logger name
    :param message: Message
    :param func_name: A customized name of the function
    """
    if func is None:
        return functools.partial(
            logged, level=level, name=name, message=message,
            func_name=func_name,
        )
    logger = logging.getLogger(name)

    @functools.wraps(func)
    def wrapper_logged(*args, **kwargs):
        f_name = func_name or func.__qualname__
        if level == logging.DEBUG and not message:
            logger.log(level, f'Enter: {f_name}')
        else:
            logger.log(level, message)
        value = func(*args, **kwargs)
        if level == logging.DEBUG and not message:
            logger.log(level, f'Leave: {f_name}')
        return value
    return wrapper_logged
