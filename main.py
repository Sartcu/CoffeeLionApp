import os.path
import sys
import logging
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QPushButton, QTextBrowser, QTableWidgetItem, QTableWidget, QMessageBox, QComboBox,
                             QTabWidget, QScrollArea, QSizePolicy, QListWidget)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
import productManager
import inventoryManager
from logger import DBG_logger

from functools import partial  # merge the function and param into one functionn


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
        self.payment_combo = None
        self.product_list_widget = None
        self.log_textBrowser = None
        self.checkout_button = None
        self.scan_button = None
        self.order_button = None
        self.total_price_label = None
        self.order_table = None

        self.manager = productManager.ProductManager(json_file_path)
        self.inventoryManager = inventoryManager.InventoryManager()

        self.input_text = ""
        self.scan_btn_state = False
        self.scan_mode = None  # 0: '+' 1: '-'
        self.pay_method = 'Cash'
        self.order_num = 0

        # init ui
        self.init_ui()
        self.link_ui()
        DBG_logger.logger.info(f"\n ============================= START {release_version} ============================= \n")

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
        write_to_record_file(f"Payment: {self.pay_method}")
        write_to_record_file(f"===== END {self.order_num} ===== \n")

        msg_box = QMessageBox()
        msg_box.setWindowTitle("訂購清單")
        msg_box.setText(f"訂購清單: \n{order_summary}\n\n 總價: {sum_total_item_price} 元 \n\n 支付方式: {self.pay_method}")
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

    def update_pay_method(self, index):
        if index == 0:
            self.pay_method = 'Cash'
        elif index == 1:
            self.pay_method = 'LinePay'

    def init_ui(self):
        # uic.loadUi('coffeelion.ui', self)
        # self.setupUi(self)
        self.setWindowTitle("CoffeeLion")

        # Create a central widget and set a main vertical layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create a QTabWidget
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        """
        Tabel 1 Checkout Tabel
        """
        # Create a container widget for the first tab
        checkout_tab_widget = QWidget()
        tab_widget.addTab(checkout_tab_widget, "Checkout")

        # Main layout for the first tab
        checkout_layout = QHBoxLayout()
        checkout_tab_widget.setLayout(checkout_layout)

        # Region A: Vertical Layout
        left_layout = QVBoxLayout()
        checkout_layout.addLayout(left_layout)

        from orderTableWidget import orderTableWidget
        self.order_table = orderTableWidget()
        self.order_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
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

        # ComboBox for payment method
        self.payment_combo = QComboBox()
        self.payment_combo.addItem("Cash")
        self.payment_combo.addItem("LinePay")
        order_button_layout.addWidget(self.payment_combo)

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

        from productListBtnWidget import productListBtnWidget
        self.product_list_widget = productListBtnWidget()
        self.product_list_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        checkout_layout.addWidget(self.product_list_widget)

        """
        Tabel 2
        """
        # Create a container widget for the second tab
        inventory_tab_widget = QWidget()
        tab_widget.addTab(inventory_tab_widget, "Inventory")

        # Main layout for the inventory tab
        inventory_layout = QHBoxLayout()
        inventory_tab_widget.setLayout(inventory_layout)

        # Create and add the QTableWidget to the left side
        from inventoryTableWidget import inventoryTableWidget
        self.inventory_table = inventoryTableWidget()
        inventory_layout.addWidget(self.inventory_table)

        # Create and add the vertical button layout to the right side
        button_layout = QVBoxLayout()
        inventory_layout.addLayout(button_layout)

        self.button1 = QPushButton("Button 1")
        button_layout.addWidget(self.button1)
        self.button2 = QPushButton("Button 2")
        button_layout.addWidget(self.button2)
        self.button3 = QPushButton("Button 3")
        button_layout.addWidget(self.button3)
        self.button4 = QPushButton("Button 4")
        button_layout.addWidget(self.button4)

        """
        LogTextBrowser
        """
        # Create and add the logTextBrowser widget below the tabs
        from logTextBrowser import LogTextBrowser
        self.log_textBrowser = LogTextBrowser()
        main_layout.addWidget(self.log_textBrowser)
        DBG_logger.setup_logging(self.log_textBrowser, level=logging.NOTSET)

        # Create a scroll area to handle overflow
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)

        screen_geometry = self.screen().availableGeometry()
        self.setGeometry(screen_geometry)  # Ensure it fits within screen bounds

        """
        Status Bar
        """
        # Status Bar
        self.statusBar = self.statusBar()
        self.scan_status_label = QLabel("Scan", self)
        self.statusBar.addPermanentWidget(self.scan_status_label)
        self.scan_mode_status_label = QLabel("mode", self)
        self.statusBar.addPermanentWidget(self.scan_mode_status_label)
        self.scan_status_label.setText("Ready")
        self.scan_mode_status_label.setText("None")

    def link_ui(self):
        # Connect signal from ProductListBtnWidget to increase_quantity_from_signal method of ProductManager
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
