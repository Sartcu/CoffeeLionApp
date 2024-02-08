import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox
from PyQt6 import uic

import productManager
import time

class CoffeeLionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.all_item_price = 0
        # init ui
        self.init_ui()
        self.manager = productManager.ProductManager('coffeelionProductList.json')
        # Connect button clicks to functions
        self.order_pushButton.clicked.connect(self.order)
        self.checkout_pushButton.clicked.connect(self.checkout)

        self.i1_add_pushButton.clicked.connect(self.add_chicken)
        self.i1_remove_pushButton.clicked.connect(self.remove_chicken)
        self.i2_add_pushButton.clicked.connect(self.add_fish)
        self.i2_remove_pushButton.clicked.connect(self.remove_fish)
    def order(self):
        self.manager = productManager.ProductManager('coffeelionProductList.json')
        self.update_order_table()
        self.log_textBrowser.clear()

    def checkout(self):
        order_summary = ""  # 初始化订单摘要为空字符串
        for item, product in enumerate(self.manager.products_dict):
            price = self.manager.products_dict[product]['Price']
            nums = self.manager.products_dict[product]['Numbers']
            total_price = price * nums
            # 仅当数量大于0时才将产品信息添加到订单摘要中
            if nums > 0:
                order_summary += f"{product}: {price} * {nums} = {total_price}\n"

        msg_box = QMessageBox()
        msg_box.setWindowTitle("訂購清單")
        msg_box.setText(f"訂購清單: \n{order_summary}\n\n 總價: {self.all_item_price} 元")
        msg_box.exec()

        self.manager = productManager.ProductManager('coffeelionProductList.json')
        self.update_order_table()
        self.log_textBrowser.clear()

    def add_chicken(self):
        self.manager.increase_quantity('綜合水果凍乾(30g)')
        self.log_textBrowser.append(f'{time.strftime("%m-%d %H:%M:%S", time.localtime())} Added 1 chicken to order')
        self.update_order_table()

    def remove_chicken(self):
        self.manager.decrease_quantity('綜合水果凍乾(30g)')
        self.log_textBrowser.append(f'{time.strftime("%m-%d %H:%M:%S", time.localtime())} Removed 1 chicken from order')
        self.update_order_table()

    def add_fish(self):
        self.manager.increase_quantity('草莓凍乾(30g)')
        self.log_textBrowser.append(f'{time.strftime("%m-%d %H:%M:%S", time.localtime())} Added 1 fish to order')
        self.update_order_table()

    def remove_fish(self):
        self.manager.decrease_quantity('草莓凍乾(30g)')
        self.log_textBrowser.append(f'{time.strftime("%m-%d %H:%M:%S", time.localtime())} Removed 1 fish from order')
        self.update_order_table()


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
        self.l1_totalprice.setText(f"總價: {self.all_item_price}")
    def init_ui(self):
        uic.loadUi('coffeelion.ui', self)
        self.setWindowTitle("CoffeeLion")

def main():
    app = QApplication(sys.argv)
    coffeelion_app = CoffeeLionApp()
    coffeelion_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()