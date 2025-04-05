import logging
from pathlib import Path

# diagnose problems and get info
class Log:
    def __init__(self):
        # configuring log
        self._log_dir = Path(__file__).parent.absolute()
        self._log_file = self._log_dir / "http_server.log"

        # creating a logger
        self.logger = logging.getLogger("http")
        self.logger.setLevel(logging.DEBUG)

        # file handler
        self._file_handler = logging.FileHandler(self._log_file)
        self._file_handler.setLevel(logging.DEBUG)

        # format of the logging message
        self._formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
        self._file_handler.setFormatter(self._formatter)

        self.logger.addHandler(self._file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)
    
    def critical(self, message):
        self.logger.critical(message)
