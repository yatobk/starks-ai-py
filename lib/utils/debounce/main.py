from threading import Timer

class Debounce:
    def __init__(self, callback, interval: float):
        self.callback = callback
        self.interval = interval
        self.timer = None

    def call(self, *args, **kwargs):
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.interval, self.callback, args=args, kwargs=kwargs)
        self.timer.start()
