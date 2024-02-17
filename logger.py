import logging
from PyQt6.QtWidgets import QTextBrowser

import os
application_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(application_path, 'log.txt')

# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warning message')
# logger.error('error message')
# logger.critical('critical message')

class QTextBrowserLogHandler(logging.Handler):
    def __init__(self, text_browser: QTextBrowser):
        super().__init__()
        self.text_browser = text_browser

    def emit(self, record):
        msg = self.format(record)
        # msg += '\n'  # 添加换行符
        # self.text_browser.insertPlainText(msg)
        self.text_browser.append(msg)

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def setup_logging(self, log_text_browser: QTextBrowser, level=logging.NOTSET):
        # create logger
        self.logger = logging.getLogger()
        self.logger.setLevel(level)

        # create logger handler send log to QTextBrowser
        log_handler = QTextBrowserLogHandler(log_text_browser)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s %(funcName)s %(lineno)d: %(message)s')
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)

        # create logger handler send log to QTextBrowser
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


DBG_logger = Logger()
