import json
from PyQt6.QtCore import QObject, pyqtSignal
from logger import DBG_logger

class ProductManager(QObject):
    updateTable = pyqtSignal()
    def __init__(self, file_path):
        super().__init__()
        self.products_dict = self.load_products(file_path)

    def load_products(self, file_path):
        """
        從 JSON 檔案中讀取產品資訊並建立字典
        """
        with open(file_path, 'r') as file:
            data = json.load(file)

        products_dict = {}
        for product in data['CoffeeLineProduct']:
            product_info = {
                'Code': product['Code'],
                'Price': product['Price'],
                'Numbers': 0  # 初始數量為0
            }
            products_dict[product['Name']] = product_info

        return products_dict

    def increase_quantity(self, product_name, amount=1):
        """
        增加產品數量
        """
        if product_name in self.products_dict:
            self.products_dict[product_name]['Numbers'] += amount
            self.updateTable.emit()
        else:
            DBG_logger.logger.info(f"找不到產品 {product_name}")

    def decrease_quantity(self, product_name, amount=1):
        """
        減少產品數量
        """
        if product_name in self.products_dict:
            if self.products_dict[product_name]['Numbers'] >= amount:
                self.products_dict[product_name]['Numbers'] -= amount
                self.updateTable.emit()
            else:
                DBG_logger.logger.info(f"產品 {product_name} 的數量不足")
        else:
            DBG_logger.logger.info(f"找不到產品 {product_name}")

    def print_current_quantities(self):
        """
        列印當前產品數量
        """
        DBG_logger.logger.info("\n===== 當前產品數量：")
        for product_name, product_info in self.products_dict.items():
            if product_info['Numbers'] > 0:
                DBG_logger.logger.info(f"{product_name}: {product_info['Numbers']}")

    def increase_quantity_from_signal(self, product_name):
        """
        從信號中接收產品名稱，增加產品數量
        """
        self.increase_quantity(product_name)
        self.print_current_quantities()

    def decrease_quantity_from_signal(self, product_name):
        """
        從信號中接收產品名稱，減少產品數量
        """
        self.decrease_quantity(product_name)
        self.print_current_quantities()

if __name__ == '__main__':
    # 初始化 ProductManager 實例，並從 JSON 檔案中讀取產品資訊
    manager = ProductManager('coffeelionProductList.json')

    # 增加手機數量
    manager.increase_quantity('綜合水果凍乾(30g)', 3)
    manager.decrease_quantity('綜合水果凍乾(30g)', 2)

    # 列印當前產品數量
    manager.print_current_quantities()

