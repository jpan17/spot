import os
import inspect
from datetime import datetime

class Logger():
    TRACE = 4
    DEBUG = 3
    INFO = 2
    WARN = 1
    ERROR = 0

    def __init__(self, filename = 'default'):
        if filename == 'default':
            frame = inspect.stack()[1]
            filename = frame[0].f_code.co_filename

        self._filename = filename
        self._level = (os.environ.get('SPOT_LOG_LEVEL') or '').lower()

        if(self._level == 'trace'):
            self._level = self.TRACE
        elif(self._level == 'debug'):
            self._level = self.DEBUG
        elif(self._level == 'warn'):
            self._level = self.WARN
        elif(self._level == 'error'):
            self._level = self.ERROR
        else:
            self._level = self.INFO

    def log(self, *message, level = -1):
        if level == -1:
            level = self.INFO

        if level <= self._level:
            now = datetime.now()
            dtstr = now.strftime('[%d/%b/%Y %H:%M:%S]')

            print(dtstr, '{0}:'.format(self._filename), *message)

    def trace(self, *message):
        self.log(*message, self.TRACE)

    def debug(self, *message):
        self.log(*message, self.DEBUG)

    def info(self, *message):
        self.log(*message, self.INFO)

    def warn(self, *message):
        self.log(*message, self.WARN)

    def error(self, *message):
        self.log(*message, self.ERROR)