from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLabel
from PyQt6 import QtCore
from PyQt6.QtCore import Qt

class orderTableWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table_widget = QTableWidget()
        self.table_widget.setMinimumSize(600, 400)
        self.table_widget.setObjectName("order_table")
        self.table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # select all row
        self.table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)         # can't modify the table value

        headers = ["品名", "單價", "數量", "單項總和"]
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)

        self.table_widget.setColumnWidth(0, 200)
        self.table_widget.setColumnWidth(1, 90)
        self.table_widget.setColumnWidth(2, 90)
        self.table_widget.setColumnWidth(3, 90)

        self.total_price_label = QLabel("總價：0 TWD")
        self.total_price_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.layout.addWidget(self.table_widget)
        self.layout.addWidget(self.total_price_label)

        # stop keyPressEvent in this widget
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def update_order_table(self, obj):
        # Clear previous content
        self.table_widget.clearContents()

        # Set row and column count
        num_products = len(obj.products_dict)
        self.table_widget.setRowCount(num_products)

        # Populate table with product names and quantities
        all_item_price = 0
        row_index = 0  # To keep track of the row index in the table
        for product, details in obj.products_dict.items():
            price = details['Price']
            numbers = details['Numbers']
            total_price = price * numbers
            all_item_price += total_price
            # Only add to the table if the quantity is greater than 1
            if numbers > 0:
                name_item = QTableWidgetItem(product)
                price_item = QTableWidgetItem(str(price))
                quantity_item = QTableWidgetItem(str(numbers))
                total_item = QTableWidgetItem(str(total_price))
                self.table_widget.setItem(row_index, 0, name_item)
                self.table_widget.setItem(row_index, 1, price_item)
                self.table_widget.setItem(row_index, 2, quantity_item)
                self.table_widget.setItem(row_index, 3, total_item)
                row_index += 1  # Increment row index for the next product

        self.total_price_label.setText(f"總價：{all_item_price} TWD")

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = orderTableWidget()
    window.show()
    sys.exit(app.exec())