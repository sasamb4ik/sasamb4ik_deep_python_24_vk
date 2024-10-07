from functools import wraps


def retry_deco(retries, exceptions=None):
    if retries < 1:
        raise ValueError

    if exceptions is None:
        exceptions = ()
    elif isinstance(exceptions, type) and issubclass(exceptions, Exception):
        exceptions = (exceptions,)
    elif not isinstance(exceptions, (list, tuple, set, frozenset)):
        raise TypeError
    else:
        exceptions = tuple(exceptions)
        for exc in exceptions:
            if not isinstance(exc, type) or not issubclass(exc, Exception):
                raise TypeError

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            args_parts = []
            if args:
                args_parts.append(f"positional args = {args}")
            if kwargs:
                kwargs_str = ", ".join(
                    f'"{k}": {repr(v)}' for k, v in kwargs.items()
                )
                args_parts.append(f"keyword kwargs = {{{kwargs_str}}}")
            arguments = (
                ", ".join(args_parts) if args_parts else "no arguments"
            )

            attempt = 1
            while attempt <= retries:
                try:
                    result = function(*args, **kwargs)
                    log_attempt(
                        function.__name__, arguments, attempt, 'result', result
                    )
                    return result
                except exceptions as error:
                    log_attempt(
                        function.__name__, arguments, attempt,
                        'exception', f'{type(error).__name__}: {error}'
                    )
                    raise
                except Exception as error:
                    log_attempt(
                        function.__name__, arguments, attempt,
                        'exception', f'{type(error).__name__}: {error}'
                    )
                    if attempt == retries:
                        raise
                    attempt += 1

        return wrapper

    return decorator


def log_attempt(func_name, arguments, attempt, status, value):
    print(
        f'run "{func_name}" with {arguments}, '
        f'attempt = {attempt}, {status} = {value}'
    )
