import sys
import json
import time

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QPushButton, QTextBrowser, QTableWidgetItem, QTableWidget, QMessageBox)
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic

import productManager

# from coffeelion_ui import Ui_coffeelion
# from dynamicbtn_ui import Ui_dynamicBtnWindow

class CoffeeLionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.log_textBrowser = None
        self.checkout_button = None
        self.scan_button = None
        self.order_button = None
        self.totalprice_label = None
        self.order_table = None

        self.all_item_price = 0
        # init ui
        self.init_ui()

        self.manager = productManager.ProductManager('coffeelionProductList.json')

        # Connect button clicks to functions
        self.order_button.clicked.connect(self.order)
        self.checkout_button.clicked.connect(self.checkout)
        self.scan_button.clicked.connect(self.scan)

    def order(self):
        self.manager = productManager.ProductManager('coffeelionProductList.json')
        self.update_order_table()
        self.log_textBrowser.clear()

    def checkout(self):
        order_summary = ""
        for item, product in enumerate(self.manager.products_dict):
            price = self.manager.products_dict[product]['Price']
            nums = self.manager.products_dict[product]['Numbers']
            total_price = price * nums

            if nums > 0:
                order_summary += f"{product}: {price} * {nums} = {total_price}\n"

        msg_box = QMessageBox()
        msg_box.setWindowTitle("訂購清單")
        msg_box.setText(f"訂購清單: \n{order_summary}\n\n 總價: {self.all_item_price} 元")
        msg_box.exec()

        self.manager = productManager.ProductManager('coffeelionProductList.json')
        self.update_order_table()
        self.log_textBrowser.clear()

    def scan(self):
        self.log_textBrowser.append(
            f'{time.strftime("%m-%d %H:%M:%S", time.localtime())} Scan mode')

    def update_order_table(self):
        # Clear previous content
        self.order_table.clear()

        # Set row and column count
        headers = ["品名", "單價", "數量", "單項總和"]
        num_products = len(self.manager.products_dict)
        self.order_table.setRowCount(num_products)
        self.order_table.setColumnCount(len(headers))
        self.order_table.setHorizontalHeaderLabels(headers)

        # Populate table with product names and quantities
        self.all_item_price = 0
        row_index = 0  # To keep track of the row index in the table
        for product, details in self.manager.products_dict.items():
            price = details['Price']
            numbers = details['Numbers']
            total_price = price * numbers
            self.all_item_price += total_price
            # Only add to the table if the quantity is greater than 1
            if numbers > 0:
                name_item = QTableWidgetItem(product)
                price_item = QTableWidgetItem(str(price))
                quantity_item = QTableWidgetItem(str(numbers))
                total_item = QTableWidgetItem(str(total_price))
                self.order_table.setItem(row_index, 0, name_item)
                self.order_table.setItem(row_index, 1, price_item)
                self.order_table.setItem(row_index, 2, quantity_item)
                self.order_table.setItem(row_index, 3, total_item)
                row_index += 1  # Increment row index for the next product
        self.totalprice_label.setText(f"總價: {self.all_item_price}")
        self.order_table.resizeColumnsToContents()

    def init_ui(self):
        # uic.loadUi('coffeelion.ui', self)
        # self.setupUi(self)
        self.setWindowTitle("CoffeeLion")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # 左側區域 A
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        self.order_table = QTableWidget()
        self.order_table.setFixedSize(450, 650)
        self.order_table.setObjectName("order_table")
        left_layout.addWidget(self.order_table)

        self.totalprice_label = QLabel("總價: 0 元")
        self.totalprice_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        left_layout.addWidget(self.totalprice_label)

        button_layout = QHBoxLayout()
        left_layout.addLayout(button_layout)

        self.order_button = QPushButton("Order")
        button_layout.addWidget(self.order_button)

        self.scan_button = QPushButton("Scan")
        button_layout.addWidget(self.scan_button)

        self.checkout_button = QPushButton("Checkout")
        button_layout.addWidget(self.checkout_button)

        self.log_textBrowser = QTextBrowser()
        self.log_textBrowser.setFixedSize(450, 200)
        left_layout.addWidget(self.log_textBrowser)

        # 右側區域 B
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        # 讀取 'coffeelionProductList.json'
        with open('coffeelionProductList.json', 'r') as file:
            data = json.load(file)

        max_name_width = max(len(item["Name"]) for item in data["CoffeeLineProduct"])

        # 根據 JSON 中的項目數量新增按鈕
        for item in data["CoffeeLineProduct"]:
            name = item["Name"]
            price = item["Price"]

            # 新增水平布局
            hbox = QHBoxLayout()

            # 新增 QLabel 顯示名稱
            name_label = QLabel(f'{name}', self)
            # 調整價格標籤寬度以避免價格被蓋住
            name_label.setFixedWidth(max_name_width * 10 + 30)  # 加上一些額外空間
            hbox.addWidget(name_label)

            # 新增 QLabel 顯示價格
            price_label = QLabel(f'{price:.1f}', self)
            # 調整價格標籤寬度以避免價格被蓋住
            price_label.setFixedWidth(max_name_width * 10)  # 加上一些額外空間
            hbox.addWidget(price_label)

            # 新增 Item +1 按鈕
            btn_plus = QPushButton(f'+1', self)
            btn_plus.setFixedSize(50, 30)  # 設置按鈕大小
            btn_plus.clicked.connect(lambda checked, name=name, price=price: self.on_plus_clicked(name, price))
            hbox.addWidget(btn_plus)

            # 新增 Item -1 按鈕
            btn_minus = QPushButton(f'-1', self)
            btn_minus.setFixedSize(50, 30)  # 設置按鈕大小
            btn_minus.clicked.connect(lambda checked, name=name, price=price: self.on_minus_clicked(name, price))
            hbox.addWidget(btn_minus)

            right_layout.addLayout(hbox)

    def on_plus_clicked(self, name, price):
        self.manager.increase_quantity(str(name))
        self.log_textBrowser.append(
            f'{time.strftime("%m-%d %H:%M:%S", time.localtime())} {name} +1 to order')
        self.update_order_table()

    def on_minus_clicked(self, name, price):
        self.manager.decrease_quantity(str(name))
        self.log_textBrowser.append(
            f'{time.strftime("%m-%d %H:%M:%S", time.localtime())} {name} -1 to order')
        self.update_order_table()

def main():
    app = QApplication(sys.argv)
    coffeelion_app = CoffeeLionApp()
    coffeelion_app.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
