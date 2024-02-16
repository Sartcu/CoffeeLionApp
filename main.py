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

        self.dynamic_Btn = None
        self.log_textBrowser = None
        self.checkout_button = None
        self.scan_button = None
        self.order_button = None
        self.total_price_label = None
        self.order_table = None

        self.all_item_price = 0
        self.manager = productManager.ProductManager('coffeelionProductList.json')
        # init ui
        self.init_ui()
        DBG_logger.logger.info("===== START =====")
        # Connect button clicks to functions
        # self.order_button.clicked.connect(self.order)
        # self.checkout_button.clicked.connect(self.checkout)
        # self.scan_button.clicked.connect(self.scan)

    # def order(self):
    #     self.manager = productManager.ProductManager('coffeelionProductList.json')
    #     # self.update_order_table()
    #     self.log_textBrowser.clear()

    # def checkout(self):
    #     order_summary = ""
    #     for item, product in enumerate(self.manager.products_dict):
    #         price = self.manager.products_dict[product]['Price']
    #         nums = self.manager.products_dict[product]['Numbers']
    #         total_price = price * nums
    #
    #         if nums > 0:
    #             order_summary += f"{product}: {price} * {nums} = {total_price}\n"
    #
    #     msg_box = QMessageBox()
    #     msg_box.setWindowTitle("訂購清單")
    #     msg_box.setText(f"訂購清單: \n{order_summary}\n\n 總價: {self.all_item_price} 元")
    #     msg_box.exec()
    #
    #     self.manager = productManager.ProductManager('coffeelionProductList.json')
    #     self.update_order_table()
    #     self.log_textBrowser.clear()

    # def scan(self):
    #     self.log_textBrowser.append(
    #         f'{time.strftime("%m-%d %H:%M:%S", time.localtime())} Scan mode')


    def init_ui(self):
        # uic.loadUi('coffeelion.ui', self)
        # self.setupUi(self)
        self.setWindowTitle("CoffeeLion")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # region A
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        from orderTableWidget import orderTableWidget
        self.order_table = orderTableWidget()
        left_layout.addWidget(self.order_table)

        button_layout = QHBoxLayout()
        left_layout.addLayout(button_layout)

        self.order_button = QPushButton("Order")
        button_layout.addWidget(self.order_button)

        self.scan_button = QPushButton("Scan")
        button_layout.addWidget(self.scan_button)

        self.checkout_button = QPushButton("Checkout")
        button_layout.addWidget(self.checkout_button)

        self.log_textBrowser = QTextBrowser()
        self.log_textBrowser.setMinimumSize(600, 200)
        font = QFont()
        font.setPointSize(10)
        self.log_textBrowser.setFont(font)
        left_layout.addWidget(self.log_textBrowser)
        DBG_logger.setup_logging(self.log_textBrowser, level=logging.NOTSET)

        # region B
        from productListBtnWidget import productListBtnWidget
        self.product_list_widget = productListBtnWidget()

        # Connect signal from ProductListBtnWidget to increase_quantity_from_signal method of ProductManager
        self.product_list_widget.increaseQuantity.connect(self.manager.increase_quantity_from_signal)
        self.product_list_widget.decreaseQuantity.connect(self.manager.decrease_quantity_from_signal)
        main_layout.addWidget(self.product_list_widget)

        from functools import partial # merge the function and param into one functionn
        self.manager.updateTable.connect(partial(self.order_table.update_order_table, self.manager))


def main():
    app = QApplication(sys.argv)
    coffeelion_app = CoffeeLionApp()
    coffeelion_app.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
