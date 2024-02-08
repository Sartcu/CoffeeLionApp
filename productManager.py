import json

class ProductManager:
    def __init__(self, file_path):
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
                # 'Name': product['Name'],
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
        else:
            print(f"找不到產品 {product_name}")

    def decrease_quantity(self, product_name, amount=1):
        """
        減少產品數量
        """
        if product_name in self.products_dict:
            if self.products_dict[product_name]['Numbers'] >= amount:
                self.products_dict[product_name]['Numbers'] -= amount
            else:
                print(f"產品 {product_name} 的數量不足")
        else:
            print(f"找不到產品 {product_name}")

    def print_current_quantities(self):
        """
        列印當前產品數量
        """
        print("當前產品數量：")
        for product_name, product_info in self.products_dict.items():
            print(f"{product_name}: {product_info['Numbers']}")



if __name__ == '__main__':
    # 初始化 ProductManager 實例，並從 JSON 檔案中讀取產品資訊
    manager = ProductManager('coffeelionProductList.json')

    # 增加手機數量
    manager.increase_quantity('綜合水果凍乾(30g)', 3)
    manager.decrease_quantity('綜合水果凍乾(30g)', 2)

    # 列印當前產品數量
    manager.print_current_quantities()
    print(manager.products_dict)
    print(manager.products_dict.keys())
    print(f"manager.products_dict.keys(), {len(manager.products_dict.keys())}")
    for index, product in enumerate(manager.products_dict):
        print(f" index {index}, product {product}, {manager.products_dict[product]['Code']}")

    for item, product in enumerate(manager.products_dict):

        price = manager.products_dict[product]['Price']
        nums = manager.products_dict[product]['Numbers']
        total_price = price * nums
        # print(f"price {price} nums {nums} total_price {total_price}")
        order_summary = "\n".join([f"{product}: {price} * {nums} = {total_price}"])
        print(order_summary)
