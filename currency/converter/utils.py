def exc_raiser(exc):
    def decor(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception:
                raise exc
            else:
                return result
        return wrapper
    return decor
