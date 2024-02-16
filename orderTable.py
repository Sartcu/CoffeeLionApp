from PyQt6.QtWidgets import QTableWidget
from PyQt6 import QtCore

class orderTableWidget(QTableWidget):
    cell_clicked = QtCore.pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.setFixedSize(450, 650)
        self.setObjectName("order_table")
        self.cellClicked.connect(self.on_cell_clicked)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # select all row
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)        # can't modify the table value

        headers = ["品名", "單價", "數量", "單項總和"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

        self.setColumnWidth(0, 130)
        self.setColumnWidth(1, 90)
        self.setColumnWidth(2, 90)

    def on_cell_clicked(self, row, column):
        self.cell_clicked.emit(row, column)

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = orderTableWidget()
    window.show()
    sys.exit(app.exec())