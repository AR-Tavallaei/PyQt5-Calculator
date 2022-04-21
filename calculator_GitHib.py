from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QListWidget, QMenuBar, QFrame, QGridLayout, QToolBar
from PyQt5.QtWidgets import QListWidgetItem, QToolButton, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

import sys
from functools import partial
from math import factorial, sqrt


class Calculator (QWidget):
    def __init__(self):
        super().__init__()

        self.window()
        self.make_buttons()
        self.make_entry()
        self.make_history()
        self.make_menus()

    def window(self):
        self.setGeometry(400, 200, 540, 375)
        self.setFixedSize(540, 375)
        self.setWindowTitle('Calculator')
        self.setWindowIcon(
            QIcon('media/calculate.png'))
        self.setStyleSheet('QWidget {background-color : #000070}')
        self.setToolTip('Calculator')

        # QApplication.setOverrideCursor(Qt.WaitCursor)

        self.frame1 = QFrame(self)
        self.frame1.setGeometry(0, 20, 220, 355)

        self.frame2 = QFrame(self)
        self.frame2.setGeometry(220, 75, 310, 310)

        self.frame3 = QFrame(self)
        self.frame3.setGeometry(220, 20, 310, 55)

    def make_buttons(self):
        # make buttons

        lst_buttons = {'^': 1, '√': 2, '!': 3, 'π': 4, 'e': 5, '1': 6, '2': 7, '3': 8, '+': 9, '(': 10, '4': 11, '5': 12,
                       '6': 13, '-': 14, ')': 15, '7': 16, '8': 17, '9': 18, '×': 19, '=': 20, '0': 21, '.': 22, '÷': 23}

        self.grid_layout = QGridLayout(self.frame2)
        self.frame2.setLayout(self.grid_layout)

        for button in lst_buttons:
            exec(
                f"btn{lst_buttons[button]} = QPushButton(text = '{button}', parent = self.frame2)\nlst_buttons['{button}'] = btn{lst_buttons[button]}")

        #############################################################
        # grid buttons

        for button in list(lst_buttons.values()):
            button.setFont(QFont('Tahoma', 15))
            button.setToolTip(f'<b> {button.text()} <b>')
            if button.text() != '=':
                button.clicked.connect(partial(self.on_click, button))
            else:
                button.clicked.connect(self.evaluation)

            if button.text().isdigit() or button.text() == '.':
                button.setStyleSheet(
                    'QPushButton {background : #EEEEEE}' + 'QPushButton::Hover {background-color: lightgray}')
            elif button.text() == '=':
                button.setStyleSheet(
                    'QPushButton {background :#EEB674}' + 'QPushButton::Hover {background-color: #E89E44}')
            else:
                button.setStyleSheet(
                    'QPushButton {background :#FFFFC9}' + 'QPushButton::Hover {background-color: #FEF194}')

            index = list(lst_buttons.values()).index(button)
            row = index // 5
            column = (index % 5) +\
                1 if button.text() in ['.', '÷'] else index % 5

            rowspan = 2 if button.text() == '=' else 1
            columnspan = 2 if button.text() == '0' else 1

            if button.text() != '=':
                self.grid_layout.addWidget(
                    button, row, column, rowspan, columnspan)
            else:
                self.grid_layout.addChildWidget(button)
                button.setGeometry(250, 195, 50, 88)

    def make_entry(self):
        self.expresion = QLineEdit(self.frame3)
        self.expresion.setGeometry(10, 15, 245, 40)
        self.expresion.setStyleSheet(
            'background-color : white; border-radius : 3px; font-family : Tahoma; font-size : 15pt')
        self.expresion.setFont(QFont('Tahoma', 13))
        self.expresion.setToolTip('Expresion')
        self.expresion.returnPressed.connect(self.evaluation)

        self.btn_delete_entry = QPushButton(self.frame3)
        self.btn_delete_entry.setGeometry(250, 15, 50, 40)
        self.btn_delete_entry.setIcon(
            QIcon('media/delete.png'))
        self.btn_delete_entry.setStyleSheet(
            'QPushButton {background-color : white; border-radius : 3px}' + 'QPushButton::Hover {background-color : lightgray}')
        self.btn_delete_entry.setIconSize(QSize(35, 35))
        self.btn_delete_entry.setToolTip('Delete Last Character')
        self.btn_delete_entry.setCursor(Qt.PointingHandCursor)
        self.btn_delete_entry.clicked.connect(self.delete_entry)

        self.btn_clear_entry = QPushButton(self.frame3)
        self.btn_clear_entry.setGeometry(250, 15, 50, 40)
        self.btn_clear_entry.setText('CLR')
        self.btn_clear_entry.setStyleSheet(
            'QPushButton {background-color : white; border-radius : 3px; font-family : Tahoma; font-size : 15pt; font-style : bold}' + 'QPushButton::Hover {background-color : lightgray}')
        self.btn_clear_entry.clicked.connect(self.clear_entry)
        self.btn_clear_entry.setToolTip('Delete Expresion')
        self.btn_clear_entry.setCursor(Qt.PointingHandCursor)
        self.btn_clear_entry.hide()

    def make_history(self):
        self.history = QListWidget(self.frame1)
        self.history.setGeometry(10, 15, 200, 275)
        self.history.setStyleSheet(
            'background-color : #EAEAEA; border-radius : 5px')
        self.history.setToolTip('History')

        toolbar = QToolBar(self)
        toolbar.setGeometry(55, 315, 105, 40)
        toolbar.setStyleSheet('background-color : white; border-radius : 5px')
        toolbar.setToolTip('Tool Bar')
        toolbar.setMovable(False)

        ###########################################################################

        btn_clear = QToolButton(self)
        btn_clear.resize(40, 40)
        btn_clear.setIcon(
            QIcon('media/trash-bin.png'))
        btn_clear.setStyleSheet(
            'QToolButton {background-color : white;}' + 'QToolButton::Hover {background-color : #E4E4E4}')
        btn_clear.setIconSize(QSize(35, 35))
        btn_clear.clicked.connect(lambda: self.history.clear())
        btn_clear.setToolTip('Clear History')
        btn_clear.setCursor(Qt.PointingHandCursor)

        btn_delete = QToolButton(self)
        btn_delete.resize(40, 40)
        btn_delete.setIcon(
            QIcon('media/close.png'))
        btn_delete.setStyleSheet(
            'QToolButton {background-color : white;}' + 'QToolButton::Hover {background-color : #E4E4E4}')
        btn_delete.setIconSize(QSize(35, 35))
        btn_delete.clicked.connect(self.delete_history)
        btn_delete.setToolTip('Delete Selected History Item')
        btn_delete.setCursor(Qt.PointingHandCursor)

        btn_copy = QToolButton(self)
        btn_copy.resize(40, 40)
        btn_copy.setIcon(
            QIcon('media/copy.png'))
        btn_copy.setStyleSheet(
            'QToolButton {background-color : white;}' + 'QToolButton::Hover {background-color : #E4E4E4}')
        btn_copy.setIconSize(QSize(35, 35))
        btn_copy.setToolTip('Copy Selected Item History')
        btn_copy.clicked.connect(self.copy_history)
        btn_copy.setCursor(Qt.PointingHandCursor)

        ###########################################################################

        toolbar.addWidget(btn_clear)
        toolbar.addSeparator()
        toolbar.addWidget(btn_delete)
        toolbar.addSeparator()
        toolbar.addWidget(btn_copy)

    def make_menus(self):
        menubar = QMenuBar(self)
        menubar.setGeometry(0, 0, 540, 20)
        menubar.setStyleSheet(
            'background-color : white')

        menu1 = menubar.addMenu('Edit')
        menu1.setCursor(Qt.PointingHandCursor)
        menu1.setStyleSheet(
            'QMenu {color : black; selection-background-color : lightgray}')

        menu2 = menubar.addMenu('About')
        menu2.setCursor(Qt.PointingHandCursor)
        menu2.setStyleSheet(
            'QMenu {color : black; selection-background-color : lightgray}')

        ##########################################################################

        copy_history_action = menu1.addAction('copy selected history item')
        copy_history_action.triggered.connect(self.copy_history)
        copy_history_action.setShortcut('ctrl+shift+c')

        copy_entry_action = menu1.addAction('copy')
        copy_entry_action.triggered.connect(self.copy_entry)
        copy_entry_action.setShortcut('ctrl+c')

        past_action = menu1.addAction('past')
        past_action.triggered.connect(self.past_entry)
        past_action.setShortcut('ctrl+v')

        menu1.addSeparator()
        clear_action = menu1.addAction('clear history')
        clear_action.triggered.connect(lambda: self.history.clear())
        clear_action.setShortcut('ctrl+shift+delete')

        delete_action = menu1.addAction('delete selected history item')
        delete_action.triggered.connect(self.delete_history)
        delete_action.setShortcut('ctrl+delete')

        about_action = menu2.addAction('About')
        about_action.triggered.connect(lambda: self.about().show())
        about_action.setShortcut('ctrl+a')

    def on_click(self, button):
        self.expresion.setText(self.expresion.text() + button.text())

    def delete_entry(self):
        self.expresion.setText(self.expresion.text()[:-1])

    def clear_entry(self):
        self.expresion.setText('')
        self.btn_clear_entry.hide()
        self.btn_delete_entry.show()

    def delete_history(self):
        if len(self.history.selectedItems()) != 0:
            self.history.takeItem(self.history.row(
                self.history.selectedItems()[0]))

    def copy_history(self):
        clipboard = QApplication.clipboard()
        if len(self.history.selectedItems()) != 0:
            clipboard.setText(self.history.selectedItems()[0].text())

    def copy_entry(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.expresion.text())

    def past_entry(self):
        clipboard = QApplication.clipboard()
        self.expresion.setText(self.expresion.text() + clipboard.text())

    def about(self):
        self.win_about = QWidget()
        self.win_about.setGeometry(500, 300, 300, 200)
        self.win_about.setFixedSize(300, 200)
        self.win_about.setWindowTitle('About')
        self.win_about.setStyleSheet(
            'background-color : #000070; color : white')

        self.lb = QLabel(self.win_about)
        self.lb.setGeometry(10, 10, 280, 180)
        self.lb.setWordWrap(True)
        self.lb.setText("""This software was made by AmirReza Tavallaei and is available for free.\nemail : tavallaei.14@gmail.com\nPhone: 09132692407\n\nAny copying is illegal.\ngood luck ...""")
        self.lb.setAlignment(Qt.AlignLeft)
        self.lb.setFont(QFont('Tahoma', 13))

        btn = QPushButton(self.win_about)
        btn.setGeometry(220, 130, 40, 40)
        btn.setIcon(
            QIcon('media/calculate.png'))
        btn.setIconSize(QSize(40, 40))

        return self.win_about

    def correct_expresion(self):
        final_expresion = self.expresion.text()

        for char in final_expresion:
            index = final_expresion.index(char)
            if char in ['(', '√', 'π'] and final_expresion[index-1].isdigit():
                final_expresion = final_expresion[:index] +\
                    '×' + final_expresion[index:]

        dic_replace = {'×': '*', '÷': '/', '^': '**', 'π': '3.14'}
        for char in dic_replace:
            while char in final_expresion:
                index = final_expresion.find(char)
                final_expresion = final_expresion[:index] +\
                    dic_replace[char] + final_expresion[index+1:]

        #####################################################################################
        while '√' in final_expresion:
            index = final_expresion.index('√')

            num = index+1
            num_digits = 0
            while num <= len(final_expresion)-1 and (final_expresion[num].isdigit() or final_expresion[num] == '.'):
                num_digits += 1
                num += 1

            final_expresion = final_expresion[:index] + \
                'sqrt(' + final_expresion[index+1:index+num_digits +
                                          1] + ')' + final_expresion[index+num_digits+1:]

        #####################################################################################
        while '!' in final_expresion:
            index = final_expresion.index('!')

            num = index-1
            num_digits = 0
            while num >= 0 and (final_expresion[num].isdigit() or final_expresion[num] == '.'):
                num_digits += 1
                num -= 1

            final_expresion = final_expresion[: index-num_digits] + \
                'factorial(' + final_expresion[index -
                                               num_digits: index] + ')' + final_expresion[index+1:]

        return final_expresion

    def evaluation(self):
        try:
            final_expresion = self.correct_expresion()
            self.history.addItem(QListWidgetItem(QIcon('media/matrix.png'),
                                 self.expresion.text() + '=' + str(eval(final_expresion)), self.history))
            self.expresion.setText(str(eval(final_expresion)))
        except:
            self.expresion.setText('Wrong Expresion')
        finally:
            self.btn_delete_entry.hide()
            self.btn_clear_entry.show()


if __name__ == '__main__':
    app = QApplication([])
    window = Calculator()
    window.show()
    sys.exit(app.exec())
