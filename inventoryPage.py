from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QPushButton)
from inventoryTableWidget import inventoryTableWidget
from quantityControlDialog import QuantityControlDialog
from logger import DBG_logger

class InventoryPage(QWidget):
    def __init__(self, app, inventoryManager):
        super().__init__()
        self.app = app
        self.inventoryManager = inventoryManager
        self.setup_ui()
        self.setup_link()

    def setup_ui(self):
        inventory_layout = QVBoxLayout()
        self.inventory_table = inventoryTableWidget()
        inventory_layout.addWidget(self.inventory_table)

        button_layout = QVBoxLayout()
        inventory_layout.addLayout(button_layout)

        self.refresh_btn = QPushButton(f"Refresh")
        button_layout.addWidget(self.refresh_btn)

        self.quantity_control_button = QPushButton(f"Quantity Control")
        button_layout.addWidget(self.quantity_control_button)

        horizontal_buttons_layout = QHBoxLayout()
        self.inventory_table_scan_btn = QPushButton("Scan")
        horizontal_buttons_layout.addWidget(self.inventory_table_scan_btn)
        self.inventory_table_plus_btn = QPushButton("+")
        horizontal_buttons_layout.addWidget(self.inventory_table_plus_btn)
        self.inventory_table_minus_btn = QPushButton("-")
        horizontal_buttons_layout.addWidget(self.inventory_table_minus_btn)

        button_layout.addLayout(horizontal_buttons_layout)
        self.inventory_table_write_btn = QPushButton("Write")
        button_layout.addWidget(self.inventory_table_write_btn)
        inventory_layout.addLayout(button_layout)
        self.setLayout(inventory_layout)

    def refresh_btn_clicked(self):
        DBG_logger.logger.debug("refresh_btn_clicked")
        inventory_dict = self.inventoryManager.get_inventory_dict()
        self.inventory_table.update_table(inventory_dict)
    
    def show_dialog(self):
        dialog = QuantityControlDialog(self)
        if dialog.exec():
            code, number = dialog.get_input()
            
            try:
                number = int(number)
            except ValueError:
                DBG_logger.logger.warning(f"Invalid input for number: {number}. Must be an integer.")
                return

            DBG_logger.logger.info(f"QuantityControlDialog Code: {code}, Number: {number}")
            self.inventoryManager.update_quantity(code, int(number))

        inventory_dict = self.inventoryManager.get_inventory_dict()
        self.inventory_table.update_table(inventory_dict)

    def inventory_table_scan_clicked(self):
        DBG_logger.logger.debug("inventory_table_scan_clicked")
        self.app.scan_btn_state = not self.app.scan_btn_state
        self.app.scan_status_label.setText("Scan ON" if self.app.scan_btn_state else "Scan OFF")

    def inventory_table_plus_clicked(self):
        DBG_logger.logger.debug("inventory_table_plus_clicked")
        self.scan_mode = 0
        self.app.scan_mode_status_label.setText("+")

    def inventory_table_minus_clicked(self):
        DBG_logger.logger.debug("inventory_table_minus_clicked")
        self.scan_mode = 1
        self.app.scan_mode_status_label.setText("-")

    def inventory_table_write_clicked(self):
        DBG_logger.logger.debug("inventory_table_write_clicked")
        index = self.app.tab_widget.currentIndex()
        tab_name = self.app.tab_widget.tabText(index)
        self.inventoryManager.save_inventory_to_file(tab_name)

    def setup_link(self):
        self.quantity_control_button.clicked.connect(self.show_dialog)
        self.refresh_btn.clicked.connect(self.refresh_btn_clicked)
        self.inventory_table_scan_btn.clicked.connect(self.inventory_table_scan_clicked)
        self.inventory_table_plus_btn.clicked.connect(self.inventory_table_plus_clicked)
        self.inventory_table_minus_btn.clicked.connect(self.inventory_table_minus_clicked)
        self.inventory_table_write_btn.clicked.connect(self.inventory_table_write_clicked)