import sys
import json
import time
import logging

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QPushButton, QTextBrowser, QTableWidgetItem, QTableWidget, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic

import productManager
from logger import DBG_logger


# from coffeelion_ui import Ui_coffeelion
# from dynamicbtn_ui import Ui_dynamicBtnWindow

class CoffeeLionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.product_list_widget = None
        self.log_textBrowser = None
        self.checkout_button = None
        self.scan_button = None
        self.order_button = None
        self.total_price_label = None
        self.order_table = None

        self.manager = productManager.ProductManager('coffeelionProductList.json')

        # init ui
        self.init_ui()
        DBG_logger.logger.info("\n ============================= START ============================= \n")

    def order_btn_clicked(self):
        DBG_logger.logger.debug(f"order_btn_clicked")
        self.manager.new_order()

    def checkout_btn_clicked(self):
        DBG_logger.logger.debug(f"checkout_btn_clicked")
        order_summary = ""
        sum_total_item_price = 0
        for item, product in enumerate(self.manager.products_dict):
            price = self.manager.products_dict[product]['Price']
            nums = self.manager.products_dict[product]['Numbers']
            sum_each_item_price = price * nums

            if nums > 0:
                order_summary += f"{product}: {price} * {nums} = {sum_each_item_price}\n"
                sum_total_item_price += sum_each_item_price

        msg_box = QMessageBox()
        msg_box.setWindowTitle("訂購清單")
        msg_box.setText(f"訂購清單: \n{order_summary}\n\n 總價: {sum_total_item_price} 元")
        msg_box.exec()

        self.manager.new_order()

    def scan_btn_clicked(self):
        DBG_logger.logger.debug(f"scan_btn_clicked")
        self.update_status("Scan")

    def init_ui(self):
        # uic.loadUi('coffeelion.ui', self)
        # self.setupUi(self)
        self.setWindowTitle("CoffeeLion")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Region A: Vertical Layout
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        from orderTableWidget import orderTableWidget
        self.order_table = orderTableWidget()
        left_layout.addWidget(self.order_table)

        # Horizontal layout for order and checkout buttons
        order_button_layout = QHBoxLayout()
        left_layout.addLayout(order_button_layout)

        self.order_button = QPushButton("Order")
        order_button_layout.addWidget(self.order_button)
        self.order_button.clicked.connect(self.order_btn_clicked)

        self.checkout_button = QPushButton("Checkout")
        order_button_layout.addWidget(self.checkout_button)
        self.checkout_button.clicked.connect(self.checkout_btn_clicked)

        # Horizontal layout for scan, +, - buttons
        scan_button_layout = QHBoxLayout()
        left_layout.addLayout(scan_button_layout)

        self.scan_button = QPushButton("Scan")
        scan_button_layout.addWidget(self.scan_button)
        self.scan_button.clicked.connect(self.scan_btn_clicked)

        plus_button = QPushButton("+")
        scan_button_layout.addWidget(plus_button)

        minus_button = QPushButton("-")
        scan_button_layout.addWidget(minus_button)

        from logTextBrowser import logTextBrowser
        self.log_textBrowser = logTextBrowser()
        left_layout.addWidget(self.log_textBrowser)
        DBG_logger.setup_logging(self.log_textBrowser, level=logging.NOTSET)

        # Region B: Product List Widget (Horizontal Layout)
        from productListBtnWidget import productListBtnWidget
        self.product_list_widget = productListBtnWidget()

        # Status Bar
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Ready")  # 初始訊息

        # Connect signal from ProductListBtnWidget to increase_quantity_from_signal method of ProductManager
        self.product_list_widget.increaseQuantity.connect(self.manager.increase_quantity_from_signal)
        self.product_list_widget.decreaseQuantity.connect(self.manager.decrease_quantity_from_signal)
        main_layout.addWidget(self.product_list_widget)

        from functools import partial  # merge the function and param into one functionn
        self.manager.updateTable.connect(partial(self.order_table.update_order_table, self.manager))

        self.update_status("Done")

    def update_status(self, message):
        self.statusBar.showMessage(message)


def main():
    app = QApplication(sys.argv)
    coffeelion_app = CoffeeLionApp()
    coffeelion_app.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
