class Channel:

    def __init__(self, default=None):
        self._default = default

    def read(self):
        try:
            return self._current
        except AttributeError:
            return self._default

    def write(self, current=None):
        try:
            previous = self._current
        except AttributeError:
            previous = self._default
        self._current = current
        return previous

    def delete(self):
        try:
            deleted = self._current
            del self._current
            return deleted
        except AttributeError:
            pass
