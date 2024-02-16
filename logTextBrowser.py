from PyQt6.QtWidgets import QTextBrowser
from PyQt6.QtGui import QFont

class logTextBrowser(QTextBrowser):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 200)
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
