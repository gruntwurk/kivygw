__all__ = [
    "Singleton",
]


class Singleton:
    """
    Class decorator that turns the decorated class into a singleton.

    This means that the class' constructer will now only create a new instance
    the first time it's called. Therafter, it will alway return that same (one
    and only) instance.

    Note: type(DecoratedClass()) will no longer be DecoratedClass.
    So, be sure to test that using: isinstance(DecoratedClass(), DecoratedClass)
    """
    def __init__(self, cls):
        self._cls = cls

    def __call__(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


