import os.path
import sys
import logging

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QTabWidget, QScrollArea )
from PyQt6.QtCore import pyqtSignal

import productManager
import inventoryManager
from logger import DBG_logger
from inventoryPage import InventoryPage
from checkoutPage import CheckoutPage
from logTextBrowser import LogTextBrowser

application_path = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(application_path, 'coffeelionProductList.json')
record_file_path = os.path.join(application_path, 'recorder.txt')

release_version = '242020v01 45f4d3'

class CoffeeLionApp(QMainWindow):
    scanModeSignal = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.setup_variables()
        self.init_ui()
        DBG_logger.logger.info(f"\n ======== START {release_version} ======== \n")

    def setup_variables(self):
        self.manager = productManager.ProductManager(json_file_path)
        self.official_inventoryManager = inventoryManager.InventoryManager('official_inventory.db')
        self.shopee_inventoryManager = inventoryManager.InventoryManager('shopee_inventory.db')
        self.scan_btn_state = False
        self.scan_mode = None  # 0: '+' 1: '-'

    def on_tab_changed(self, index):
        tab_name = self.tab_widget.tabText(index)
        self.page_status_label.setText(f"{tab_name}")

    def init_ui(self):
        self.setWindowTitle("CoffeeLion")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.tab_widget = self.create_tabs()
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        main_layout.addWidget(self.tab_widget)

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
        checkoutPage = CheckoutPage(self, self.manager)
        tab_widget.addTab(checkoutPage, "Checkout")
        inventoryPage = InventoryPage(self, self.official_inventoryManager)
        tab_widget.addTab(inventoryPage, "Inventory(official)")
        inventoryPage = InventoryPage(self, self.shopee_inventoryManager)
        tab_widget.addTab(inventoryPage, "Inventory(shopee)")

        return tab_widget

    def create_status_bar(self):
        self.statusBar = self.statusBar()
        self.page_status_label = QLabel("Checkout", self)
        self.statusBar.addPermanentWidget(self.page_status_label)
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
