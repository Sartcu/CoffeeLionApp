from PyQt6.QtWidgets import QVBoxLayout, QDialog, QLineEdit, QDialogButtonBox

class QuantityControlDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Quantity Control")
        layout = QVBoxLayout(self)
        
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Enter Code")
        layout.addWidget(self.code_input)
        
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Enter Number")
        layout.addWidget(self.number_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        layout.addWidget(self.button_box)

    def get_input(self):
        code = self.code_input.text()
        number = self.number_input.text()
        return code, number
