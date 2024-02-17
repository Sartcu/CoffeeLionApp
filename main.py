import os.path
import sys
import logging
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QPushButton, QTextBrowser, QTableWidgetItem, QTableWidget, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
import productManager
from logger import DBG_logger

application_path = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(application_path, 'coffeelionProductList.json')
record_file_path = os.path.join(application_path, 'recorder.txt')


def write_to_record_file(message):
    with open(record_file_path, "a") as file:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file.write(f"{current_time} - {message}\n")


class CoffeeLionApp(QMainWindow):
    scanModeSignal = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.product_list_widget = None
        self.log_textBrowser = None
        self.checkout_button = None
        self.scan_button = None
        self.order_button = None
        self.total_price_label = None
        self.order_table = None

        self.manager = productManager.ProductManager(json_file_path)

        self.input_text = ""
        self.scan_btn_state = False
        self.scan_mode = None  # 0: '+' 1: '-'

        self.order_num = 0

        # init ui
        self.init_ui()
        DBG_logger.logger.info("\n ============================= START ============================= \n")

    def keyPressEvent(self, event):
        if not self.scan_btn_state:
            DBG_logger.logger.info("非掃描添加模式")
            return

        key_text = event.text()
        if key_text.isdigit():
            self.input_text += key_text
        elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if not self.input_text.isdigit():
                DBG_logger.logger.info(f"滑鼠點擊 Log 顯示視窗")
                return
            DBG_logger.logger.debug(f"Scan {self.input_text} -> {self.manager.find_product_by_code(self.input_text)} "
                                    f"mode {self.scan_mode}")
            self.scanModeSignal.emit(str(self.manager.find_product_by_code(self.input_text)), int(self.scan_mode))
            self.input_text = ""
        else:
            DBG_logger.logger.info("輸入法有誤")
            self.input_text = ""

    def order_btn_clicked(self):
        DBG_logger.logger.debug(f"order_btn_clicked")
        self.manager.order_clear()

    def checkout_btn_clicked(self):
        DBG_logger.logger.debug(f"checkout_btn_clicked")
        write_to_record_file(f"===== Customer {self.order_num} =====")
        order_summary = ""
        sum_total_item_price = 0
        for item, product in enumerate(self.manager.products_dict):
            price = self.manager.products_dict[product]['Price']
            nums = self.manager.products_dict[product]['Numbers']
            sum_each_item_price = price * nums

            if nums > 0:
                order_summary += f"{product}: {price} * {nums} = {sum_each_item_price}\n"
                write_to_record_file(f"{product}: {price} * {nums} = {sum_each_item_price}")
                sum_total_item_price += sum_each_item_price

        write_to_record_file(f"Total Price: {sum_total_item_price} TWD")
        write_to_record_file(f"===== END {self.order_num} ===== \n")

        msg_box = QMessageBox()
        msg_box.setWindowTitle("訂購清單")
        msg_box.setText(f"訂購清單: \n{order_summary}\n\n 總價: {sum_total_item_price} 元")
        msg_box.exec()

        # update
        self.order_num += 1
        self.manager.print_current_quantities()
        self.manager.order_clear()

    def scan_btn_clicked(self):
        DBG_logger.logger.debug(f"scan_btn_clicked")

        self.scan_btn_state = not self.scan_btn_state
        if self.scan_btn_state:
            self.scan_status_label.setText("Scan ON ")
        else:
            self.scan_status_label.setText("Scan OFF")

    def scan_plus_clicked(self):
        DBG_logger.logger.debug(f"scan_plus_btn_clicked")
        self.scan_mode = 0
        self.scan_mode_status_label.setText("+")

    def scan_minus_clicked(self):
        DBG_logger.logger.debug(f"scan_minus_btn_clicked")
        self.scan_mode = 1
        self.scan_mode_status_label.setText("-")

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

        self.scan_plus_button = QPushButton("+")
        scan_button_layout.addWidget(self.scan_plus_button)
        self.scan_plus_button.clicked.connect(self.scan_plus_clicked)

        self.scan_minus_button = QPushButton("-")
        scan_button_layout.addWidget(self.scan_minus_button)
        self.scan_minus_button.clicked.connect(self.scan_minus_clicked)

        from logTextBrowser import logTextBrowser
        self.log_textBrowser = logTextBrowser()
        left_layout.addWidget(self.log_textBrowser)
        DBG_logger.setup_logging(self.log_textBrowser, level=logging.INFO)

        # Region B: Product List Widget (Horizontal Layout)
        from productListBtnWidget import productListBtnWidget
        self.product_list_widget = productListBtnWidget()
        main_layout.addWidget(self.product_list_widget)

        # Connect signal from ProductListBtnWidget to increase_quantity_from_signal method of ProductManager
        self.product_list_widget.increaseQuantity.connect(self.manager.increase_quantity_from_signal)
        self.product_list_widget.decreaseQuantity.connect(self.manager.decrease_quantity_from_signal)

        from functools import partial  # merge the function and param into one functionn
        self.manager.updateTable.connect(partial(self.order_table.update_order_table, self.manager))

        self.scanModeSignal.connect(self.manager.scan_mode_from_signal)

        # Status Bar
        self.statusBar = self.statusBar()

        self.scan_status_label = QLabel("Scan", self)
        self.statusBar.addPermanentWidget(self.scan_status_label)

        self.scan_mode_status_label = QLabel("mode", self)
        self.statusBar.addPermanentWidget(self.scan_mode_status_label)

        self.scan_status_label.setText("Ready")
        self.scan_mode_status_label.setText("None")


def main():
    app = QApplication(sys.argv)
    coffeelion_app = CoffeeLionApp()
    coffeelion_app.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
