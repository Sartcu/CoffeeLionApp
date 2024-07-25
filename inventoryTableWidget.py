from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt6 import QtCore


class inventoryTableWidget(QWidget):
    update_inventory_table = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Create a vertical layout and set it for the widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create the table widget
        self.table_widget = QTableWidget()
        self.table_widget.setMinimumSize(600, 400)
        self.table_widget.setObjectName("inventory_table")
        self.table_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Select all rows
        self.table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Can't modify the table value

        # Set column headers
        headers = ["品名", "Code", "數量"]
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)

        # Set column widths
        self.table_widget.setColumnWidth(0, 200)
        self.table_widget.setColumnWidth(1, 90)
        self.table_widget.setColumnWidth(2, 90)

        # Add table widget to the layout
        self.layout.addWidget(self.table_widget)

        # stop keyPressEvent in this widget
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def update_table(self, data_dict):
        self.table_widget.setRowCount(len(data_dict))  # Set the number of rows

        for row, (code, details) in enumerate(data_dict.items()):
            item_name = QTableWidgetItem(details['name'])
            item_code = QTableWidgetItem(code)
            item_quantity = QTableWidgetItem(str(details['quantity']))

            self.table_widget.setItem(row, 0, item_name)
            self.table_widget.setItem(row, 1, item_code)
            self.table_widget.setItem(row, 2, item_quantity)

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys, sqlite3
    app = QApplication(sys.argv)
    inventory = sqlite3.connect('inventory.db')  # 替換為你的資料庫檔案名稱

    window = inventoryTableWidget()
    window.update_table(inventory.cursor())
    window.show()
    sys.exit(app.exec())