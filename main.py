import os.path
import sys
import logging
import time
from functools import partial

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QPushButton, QTextBrowser, QMessageBox, QComboBox, QTabWidget,
    QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal

import productManager
import inventoryManager
from quantityControlDialog import QuantityControlDialog

from logger import DBG_logger
from orderTableWidget import orderTableWidget
from productListBtnWidget import productListBtnWidget
from inventoryTableWidget import inventoryTableWidget
from logTextBrowser import LogTextBrowser


application_path = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(application_path, 'coffeelionProductList.json')
record_file_path = os.path.join(application_path, 'recorder.txt')

release_version = '242020v01 45f4d3'


def write_to_record_file(message):
    with open(record_file_path, "a") as file:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file.write(f"{current_time} - {message}\n")


class CoffeeLionApp(QMainWindow):
    scanModeSignal = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.setup_variables()
        self.init_ui()
        self.link_ui()
        DBG_logger.logger.info(f"\n ======== START {release_version} ======== \n")

    def setup_variables(self):
        self.manager = productManager.ProductManager(json_file_path)
        self.inventoryManager = inventoryManager.InventoryManager()

        self.input_text = ""
        self.scan_btn_state = False
        self.scan_mode = None  # 0: '+' 1: '-'
        self.pay_method = 'Cash'
        self.order_num = 0

    def keyPressEvent(self, event):
        if not self.scan_btn_state:
            DBG_logger.logger.info("非掃描添加模式")
            return

        key_text = event.text()
        if key_text.isdigit():
            self.input_text += key_text
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if not self.input_text.isdigit():
                DBG_logger.logger.info("滑鼠點擊 Log 顯示視窗")
                return
            DBG_logger.logger.debug(f"Scan {self.input_text} -> {self.manager.find_product_by_code(self.input_text)} mode {self.scan_mode}")
            self.scanModeSignal.emit(str(self.manager.find_product_by_code(self.input_text)), int(self.scan_mode))
            self.input_text = ""
        else:
            DBG_logger.logger.info("輸入法有誤")
            self.input_text = ""

    def order_btn_clicked(self):
        DBG_logger.logger.debug("order_btn_clicked")
        self.manager.order_clear()

    def checkout_btn_clicked(self):
        DBG_logger.logger.debug("checkout_btn_clicked")
        write_to_record_file(f"===== Customer {self.order_num} =====")
        order_summary, sum_total_item_price = self.create_order_summary()

        write_to_record_file(f"Total Price: {sum_total_item_price} TWD")
        write_to_record_file(f"Payment: {self.pay_method}")
        write_to_record_file(f"===== END {self.order_num} ===== \n")

        self.show_order_summary(order_summary, sum_total_item_price)
        self.reset_order()

    def create_order_summary(self):
        order_summary = ""
        sum_total_item_price = 0
        for product, details in self.manager.products_dict.items():
            price = details['Price']
            nums = details['Numbers']
            sum_each_item_price = price * nums

            if nums > 0:
                order_summary += f"{product}: {price} * {nums} = {sum_each_item_price}\n"
                write_to_record_file(f"{product}: {price} * {nums} = {sum_each_item_price}")
                sum_total_item_price += sum_each_item_price
        return order_summary, sum_total_item_price

    def show_order_summary(self, order_summary, sum_total_item_price):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("訂購清單")
        msg_box.setText(f"訂購清單: \n{order_summary}\n\n 總價: {sum_total_item_price} 元 \n\n 支付方式: {self.pay_method}")
        msg_box.exec()

    def reset_order(self):
        self.order_num += 1
        self.manager.print_current_quantities()
        self.manager.order_clear()

    def scan_btn_clicked(self):
        DBG_logger.logger.debug("scan_btn_clicked")
        self.scan_btn_state = not self.scan_btn_state
        self.scan_status_label.setText("Scan ON" if self.scan_btn_state else "Scan OFF")

    def scan_plus_clicked(self):
        DBG_logger.logger.debug("scan_plus_btn_clicked")
        self.scan_mode = 0
        self.scan_mode_status_label.setText("+")

    def scan_minus_clicked(self):
        DBG_logger.logger.debug("scan_minus_btn_clicked")
        self.scan_mode = 1
        self.scan_mode_status_label.setText("-")

    def update_pay_method(self, index):
        self.pay_method = 'Cash' if index == 0 else 'LinePay'

    def refresh_btn_clicked(self):
        DBG_logger.logger.debug("refresh_btn_clicked")
        inventory_dict = self.inventoryManager.get_inventory_dict()
        self.inventory_table.update_table(inventory_dict)
    
    def show_dialog(self):
        dialog = QuantityControlDialog(self)
        if dialog.exec():
            code, number = dialog.get_input()
            DBG_logger.logger.info(f"QuantityControlDialog Code: {code}, Number: {number}")
            self.inventoryManager.update_quantity(code, int(number))
        inventory_dict = self.inventoryManager.get_inventory_dict()
        self.inventory_table.update_table(inventory_dict)

    def inventory_table_scan_clicked(self):
        DBG_logger.logger.debug("inventory_table_scan_clicked")
        self.scan_btn_state = not self.scan_btn_state
        self.scan_status_label.setText("Scan ON" if self.scan_btn_state else "Scan OFF")

    def inventory_table_plus_clicked(self):
        DBG_logger.logger.debug("inventory_table_plus_clicked")
        self.scan_mode = 0
        self.scan_mode_status_label.setText("+")

    def inventory_table_minus_clicked(self):
        DBG_logger.logger.debug("inventory_table_minus_clicked")
        self.scan_mode = 1
        self.scan_mode_status_label.setText("-")

    def init_ui(self):
        self.setWindowTitle("CoffeeLion")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        tab_widget = self.create_tabs()
        main_layout.addWidget(tab_widget)

        self.log_textBrowser = LogTextBrowser()
        main_layout.addWidget(self.log_textBrowser)
        DBG_logger.setup_logging(self.log_textBrowser, level=logging.NOTSET)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)

        screen_geometry = self.screen().availableGeometry()
        self.setGeometry(screen_geometry)

        self.create_status_bar()

    def create_tabs(self):
        tab_widget = QTabWidget()

        checkout_tab_widget = QWidget()
        tab_widget.addTab(checkout_tab_widget, "Checkout")
        checkout_tab_widget.setLayout(self.create_checkout_layout())

        inventory_tab_widget = QWidget()
        tab_widget.addTab(inventory_tab_widget, "Inventory")
        inventory_tab_widget.setLayout(self.create_inventory_layout())

        return tab_widget

    def create_checkout_layout(self):
        checkout_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        checkout_layout.addLayout(left_layout)

        self.order_table = orderTableWidget()
        self.order_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        left_layout.addWidget(self.order_table)

        self.create_order_buttons(left_layout)
        self.create_scan_buttons(left_layout)

        self.product_list_widget = productListBtnWidget()
        self.product_list_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        checkout_layout.addWidget(self.product_list_widget)

        return checkout_layout

    def create_order_buttons(self, layout):
        order_button_layout = QHBoxLayout()
        layout.addLayout(order_button_layout)

        self.order_button = QPushButton("Order")
        order_button_layout.addWidget(self.order_button)
        self.order_button.clicked.connect(self.order_btn_clicked)

        self.checkout_button = QPushButton("Checkout")
        order_button_layout.addWidget(self.checkout_button)
        self.checkout_button.clicked.connect(self.checkout_btn_clicked)

        self.payment_combo = QComboBox()
        self.payment_combo.addItem("Cash")
        self.payment_combo.addItem("LinePay")
        order_button_layout.addWidget(self.payment_combo)

    def create_scan_buttons(self, layout):
        scan_button_layout = QHBoxLayout()
        layout.addLayout(scan_button_layout)

        self.scan_button = QPushButton("Scan")
        scan_button_layout.addWidget(self.scan_button)
        self.scan_button.clicked.connect(self.scan_btn_clicked)

        self.scan_plus_button = QPushButton("+")
        scan_button_layout.addWidget(self.scan_plus_button)
        self.scan_plus_button.clicked.connect(self.scan_plus_clicked)

        self.scan_minus_button = QPushButton("-")
        scan_button_layout.addWidget(self.scan_minus_button)
        self.scan_minus_button.clicked.connect(self.scan_minus_clicked)

    def create_inventory_layout(self):
        inventory_layout = QVBoxLayout()

        self.inventory_table = inventoryTableWidget()
        inventory_layout.addWidget(self.inventory_table)

        button_layout = QVBoxLayout()
        inventory_layout.addLayout(button_layout)

        self.refresh_btn = QPushButton(f"Refresh")
        button_layout.addWidget(self.refresh_btn)
        self.refresh_btn.clicked.connect(self.refresh_btn_clicked)

        self.quantity_control_button = QPushButton(f"Quantity Control")
        button_layout.addWidget(self.quantity_control_button)
        self.quantity_control_button.clicked.connect(self.show_dialog)

        horizontal_buttons_layout = QHBoxLayout()
        self.inventory_table_scan_btn = QPushButton("Scan")
        self.inventory_table_plus_btn = QPushButton("+")
        self.inventory_table_minus_btn = QPushButton("-")
        horizontal_buttons_layout.addWidget(self.inventory_table_scan_btn)
        horizontal_buttons_layout.addWidget(self.inventory_table_plus_btn)
        horizontal_buttons_layout.addWidget(self.inventory_table_minus_btn)
        button_layout.addLayout(horizontal_buttons_layout)
        inventory_layout.addLayout(button_layout)

        self.inventory_table_scan_btn.clicked.connect(self.inventory_table_scan_clicked)
        self.inventory_table_plus_btn.clicked.connect(self.inventory_table_plus_clicked)
        self.inventory_table_minus_btn.clicked.connect(self.inventory_table_minus_clicked)
        return inventory_layout

    def create_status_bar(self):
        self.statusBar = self.statusBar()
        self.scan_status_label = QLabel("Scan", self)
        self.statusBar.addPermanentWidget(self.scan_status_label)
        self.scan_mode_status_label = QLabel("mode", self)
        self.statusBar.addPermanentWidget(self.scan_mode_status_label)
        self.scan_status_label.setText("Ready")
        self.scan_mode_status_label.setText("None")

    def link_ui(self):
        self.product_list_widget.increaseQuantity.connect(self.manager.increase_quantity_from_signal)
        self.product_list_widget.decreaseQuantity.connect(self.manager.decrease_quantity_from_signal)

        self.manager.updateTable.connect(partial(self.order_table.update_order_table, self.manager))

        self.scanModeSignal.connect(self.manager.scan_mode_from_signal)
        self.payment_combo.currentIndexChanged.connect(self.update_pay_method)


def main():
    app = QApplication(sys.argv)
    coffeelion_app = CoffeeLionApp()
    coffeelion_app.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
