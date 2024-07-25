import sqlite3, os
from datetime import datetime

class InventoryManager():
    def __init__(self, db_name="inventory.db"):
        super().__init__()
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.inventory_dict = {}
        self.create_table()
        self.load_inventory()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE,
            price REAL,
            quantity INTEGER NOT NULL DEFAULT 0
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_item(self, name, code, price, quantity=0):
        try:
            query = 'INSERT INTO inventory (name, code, price, quantity) VALUES (?, ?, ?, ?)'
            self.conn.execute(query, (name, code, price, quantity))
            self.conn.commit()
            print(f"{name} (Code: {code}, Price: {price}, Quantity: {quantity}) added to inventory.")
            self.inventory_dict[code] = {
                'name': name,
                'quantity': quantity,
                'price': price
            }
            self.update_inventory_Table.emit()
        except sqlite3.IntegrityError:
            print(f"Item with code {code} already exists. Use update_item to modify details.")

    def update_item(self, name, code, price):
        query = 'UPDATE inventory SET name = ?, price = ? WHERE code = ?'
        self.conn.execute(query, (name, price, code))
        self.conn.commit()
        print(f"{name} (Code: {code}, Price: {price}) updated in inventory.")
        if code in self.inventory_dict:
            self.inventory_dict[code]['name'] = name
            self.inventory_dict[code]['price'] = price
            self.update_inventory_Table.emit()

    def remove_item(self, code):
        query = 'DELETE FROM inventory WHERE code = ?'
        self.conn.execute(query, (code,))
        self.conn.commit()
        print(f"Item with code {code} removed from inventory.")
        if code in self.inventory_dict:
            del self.inventory_dict[code]
            self.update_inventory_Table.emit()

    def update_quantity(self, code, quantity):
        query = '''
        UPDATE inventory
        SET quantity = CASE
            WHEN quantity + ? < 0 THEN 0
            ELSE quantity + ?
        END
        WHERE code = ?
        '''
        self.conn.execute(query, (quantity, quantity, code))
        self.conn.commit()
        if code in self.inventory_dict:
            new_quantity = max(0, self.inventory_dict[code]['quantity'] + quantity)
            self.inventory_dict[code]['quantity'] = new_quantity
            print(f"Quantity for item code {code} updated. New quantity is {self.inventory_dict[code]['quantity']}.")
            self.load_inventory()

    def load_inventory(self):
        query = 'SELECT name, code, quantity, price FROM inventory'
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        self.inventory_dict = {}
        for row in rows:
            self.inventory_dict[row[1]] = {
                'name': row[0],
                'quantity': row[2],
                'price': row[3]
            }

    def view_inventory(self):
        if not self.inventory_dict:
            print("Inventory is empty.")
        else:
            for code, details in self.inventory_dict.items():
                print(f"Name: {details['name']}, Code: {code}, Quantity: {details['quantity']}, Price: {details['price']}")

    def print_inventory_dict(self):
        if not self.inventory_dict:
            print("Inventory dictionary is empty.")
        else:
            for code, details in self.inventory_dict.items():
                print(f"Code: {code}, Details: {details}")

    def save_inventory_to_file(self, type):
        folder_name = "CoffeeLion_Inventory"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        filename = datetime.now().strftime(f"%Y%m%d_%H%M%S_{type}.txt")
        file_path = os.path.join(folder_name, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            for code, details in self.inventory_dict.items():
                line = f"Code: {code}, Name: {details['name']}, Quantity: {details['quantity']}, Price: {details['price']}\n"
                f.write(line)
        print(f"Inventory saved to {file_path}")

    def get_inventory_dict(self):
        return self.inventory_dict

    def __del__(self):
        self.conn.close()

if __name__ == '__main__':
    inventory = InventoryManager()

    product_list = [
        {"Name": "綜合水果凍乾(30g)", "Code": "10101001", "Price": 219.00},
        {"Name": "草莓凍乾(30g)", "Code": "10101012", "Price": 199.00},
        {"Name": "香蕉凍乾(30g)", "Code": "10101003", "Price": 199.00},
        {"Name": "鳳梨凍乾(30g)", "Code": "10101014", "Price": 199.00},
        {"Name": "蘋果凍乾(25g)", "Code": "10101005", "Price": 199.00},
        {"Name": "火龍果凍乾(30g)", "Code": "10101007", "Price": 199.00},
        {"Name": "哈密瓜凍乾(30g)", "Code": "10101006", "Price": 199.00},
        {"Name": "蔓越梅凍乾(20g)", "Code": "10101008", "Price": 250.00},
        {"Name": "奇異果凍乾(30g)", "Code": "10101009", "Price": 250.00},
        {"Name": "莓果組合(30g)", "Code": "10101010", "Price": 280.00},
        {"Name": "芭樂凍乾(20g)", "Code": "10101011", "Price": 199.00},
        {"Name": "綜合蔬菜凍乾(20g)", "Code": "10102001", "Price": 219.00},
        {"Name": "花椰菜凍乾(10g)", "Code": "10102002", "Price": 169.00},
        {"Name": "南瓜凍乾(30g)", "Code": "10102003", "Price": 189.00},
        {"Name": "櫛瓜凍乾(10g)", "Code": "10102004", "Price": 189.00},
        {"Name": "玉米筍凍乾(20g)", "Code": "10102005", "Price": 189.00},
        {"Name": "球芽甘藍凍乾(20g)", "Code": "10102006", "Price": 189.00},
        {"Name": "紅蘿蔔凍乾(30g)", "Code": "10102007", "Price": 169.00},
        {"Name": "雙色地瓜凍乾(50g)", "Code": "10102008", "Price": 169.00},
        {"Name": "雞里肌凍乾(30g)", "Code": "10103001", "Price": 119.00},
        {"Name": "司目魚柳凍乾(30g)", "Code": "10103002", "Price": 119.00},
        {"Name": "折扣 10", "Code": "", "Price": -10},
    ]

    for product in product_list:
        name = product["Name"]
        code = product["Code"]
        price = product["Price"]
        if code:  # 如果有商品編號
            try:
                inventory.add_item(name, code, price)
            except sqlite3.IntegrityError:
                inventory.update_item(name, code, price)
        else:
            print(f"Product {name} has no code and cannot be added to the inventory.")

    # 更新某些產品的數量
    inventory.update_quantity("10101001", 10)  # 添加10個 "綜合水果凍乾(30g)"
    inventory.update_quantity("10101012", 5)   # 添加5個 "草莓凍乾(30g)"

    # 查看庫存
    inventory.view_inventory()
    inventory.print_inventory_dict()

    # inv_dict = inventory.get_inventory_dict()
    # print(inv_dict)

    # 保存库存到文件
    inventory.save_inventory_to_file()