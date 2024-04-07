def final(method):
    def wrapper(self, *args, **kwargs):
        if wrapper.__func__ is not getattr(self.__class__, method.__name__).__func__:
            raise RuntimeError(f"Overriding final method '{method.__name__}' is not allowed")
        return method(self, *args, **kwargs)
    return wrapper