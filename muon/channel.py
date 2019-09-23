class Channel:

    def __init__(self, default=None):
        self._default = default

    def read(self):
        try:
            return self._current
        except AttributeError:
            return self._default

    def write(self, current=None):
        self._current = current
        return current

    def delete(self):
        try:
            del self._current
        except AttributeError:
            pass
