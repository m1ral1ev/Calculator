import sys
from typing import Union, Optional
from operator import add, sub, mul, truediv

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase

from Design import Ui_MainWindow

operations = {
    '+': add,
    '-': sub,
    'x': mul,
    '/': truediv
}


class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QFontDatabase.addApplicationFont("fonts/Rubik-Regular.ttf")

        # digits
        self.ui.button_0.clicked.connect(lambda: self.add_digit('0'))
        self.ui.button_1.clicked.connect(lambda: self.add_digit('1'))
        self.ui.button_2.clicked.connect(lambda: self.add_digit('2'))
        self.ui.button_3.clicked.connect(lambda: self.add_digit('3'))
        self.ui.button_4.clicked.connect(lambda: self.add_digit('4'))
        self.ui.button_5.clicked.connect(lambda: self.add_digit('5'))
        self.ui.button_6.clicked.connect(lambda: self.add_digit('6'))
        self.ui.button_7.clicked.connect(lambda: self.add_digit('7'))
        self.ui.button_8.clicked.connect(lambda: self.add_digit('8'))
        self.ui.button_9.clicked.connect(lambda: self.add_digit('9'))

        # actions
        self.ui.button_clear.clicked.connect(lambda: self.clear_all())
        self.ui.button_ce.clicked.connect(lambda: self.clear_entry())
        self.ui.button_point.clicked.connect(lambda: self.add_point())

        # math
        self.ui.button_equal.clicked.connect(self.calculate)
        self.ui.button_plus.clicked.connect(lambda: self.math_operation('+'))
        self.ui.button_minus.clicked.connect(lambda: self.math_operation('-'))
        self.ui.button_mult.clicked.connect(lambda: self.math_operation('x'))
        self.ui.button_div.clicked.connect(lambda: self.math_operation('/'))

    def add_digit(self, btn_text: str) -> None:
        if self.ui.le_entry.text() == '0':
            self.ui.le_entry.setText(btn_text)
        else:
            self.ui.le_entry.setText(self.ui.le_entry.text() + btn_text)

    def add_point(self) -> None:
        if '.' not in self.ui.le_entry.text():
            self.ui.le_entry.setText(self.ui.le_entry.text() + '.')

    def clear_all(self) -> None:
        self.ui.le_entry.setText('0')
        self.ui.lbl_temp.clear()

    def clear_entry(self) -> None:
        self.ui.le_entry.setText('0')

    @staticmethod
    def remove_trailing_zeros(num: str) -> str:
        n = str(float(num))
        return n[:-2] if n[-2:] == '.0' else n

    def add_temp(self, math_sign: str):
        if not self.ui.lbl_temp.text() or self.get_math_sign() == '=':
            self.ui.lbl_temp.setText(self.remove_trailing_zeros(self.ui.le_entry.text()) + f' {math_sign} ')
            self.ui.le_entry.setText('0')

    def get_entry_num(self) -> Union[int, float]:
        entry = self.ui.le_entry.text().strip('.')

        return float(entry) if '.' in entry else int(entry)

    def get_temp_num(self) -> Union[int, float, None]:
        if self.ui.lbl_temp.text():
            temp = self.ui.lbl_temp.text().strip('.').strip()[0]
            return float(temp) if '.' in temp else int(temp)

    def get_math_sign(self) -> Optional[str]:
        if self.ui.lbl_temp.text():
            return self.ui.lbl_temp.text().strip('.').split()[-1]

    def calculate(self) -> Optional[str]:
        entry = self.ui.le_entry.text()
        temp = self.ui.lbl_temp.text()

        if temp:
            result = self.remove_trailing_zeros(
                str(operations[self.get_math_sign()](self.get_temp_num(), self.get_entry_num()))
            )
            self.ui.lbl_temp.setText(temp + self.remove_trailing_zeros(entry) + ' =')
            self.ui.le_entry.setText(result)
            return result

    def math_operation(self, math_sign: str):
        temp = self.ui.lbl_temp.text()

        if not temp:
            self.add_temp(math_sign)
        else:
            if self.get_math_sign() != math_sign:
                if self.get_math_sign() == '=':
                    self.add_temp(math_sign)
                else:
                    self.ui.lbl_temp.setText(temp[:-2] + f'{math_sign}')
            else:
                self.ui.lbl_temp.setText(self.calculate() + f'{math_sign}')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()

    sys.exit(app.exec())
