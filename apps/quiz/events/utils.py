import time
from threading import Timer, Lock
import logging

logger = logging.getLogger(__name__)

class TimerManager:
    def __init__(self, interval: int, callback):
        self.interval = interval
        self.callback = callback
        self.timer = None
        self.lock = Lock()

    def start_or_reset_timer(self):
        with self.lock:
            if self.timer and self.timer.is_alive():
                self.timer.cancel()
            self.timer = Timer(self.interval, self.check_and_execute)
            self.timer.start()

    def check_and_execute(self):
        with self.lock:
            self.callback()

    def stop_timer(self):
        with self.lock:
            if self.timer:
                self.timer.cancel()
                self.timer = None
