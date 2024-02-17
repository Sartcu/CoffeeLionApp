from PyQt6.QtWidgets import QTextBrowser
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QEvent

class logTextBrowser(QTextBrowser):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 200)
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        self.setReadOnly(True)

    #     # 安裝事件過濾器
    #     self.installEventFilter(self)
    #
    # # 事件過濾器
    # def eventFilter(self, obj, event):
    #     if event.type() == QEvent.Type.KeyPress or event.type() == QEvent.Type.MouseButtonPress:
    #         # 阻止滑鼠和鍵盤事件
    #         return True
    #
    #     # 其他事件繼續正常處理
    #     return super().eventFilter(obj, event)