"""
#######################
NAME: AYUSH JAIN
ID: 2017A7PS0093P
######################
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import random
import sys
import time

################ ERROR HERE ###########################
class Box(QWidget):

    is_clicked = pyqtSignal()
    is_clickedby_human = pyqtSignal()
    is_clickedby_AI = pyqtSignal()

    def __init__(self):

        super().__init__()

        #self.resize(30, 30)
        self.setText("1")
        self.setStyleSheet("background-color: black")
        self.initialize()
        self.clicked.connect(self.clickedby_human)

    def initialize(self):
        """Contains the state of the button"""

        print("Initializing Button")
        self.is_clicked = False
        self.is_clickedby_AI = False
        self.is_clickedby_human = False
        self.update()

    def clickedby_human(self):

        if self.is_clicked:
            print("Already Clicked")
        else:
            self.is_clickedby_human = True
            self.is_clicked = True
            self.setEnabled = False
            self.update()

    def is_clickedby_AI(self):

        if is_clicked:
            print("Already Clicked")
        else:

            self.is_clickedby_AI = True
            self.is_clicked = True
            self.setEnabled = False
            self.update()

    def paintEvent(self, event):

        pane = QPainter(self)
        pane.setRenderHint(QPainter.Antialiasing)

        if self.is_clickedby_human:
            self.setStyleSheet("background-color: blue")
        elif self.is_clickedby_AI:
            self.setStyleSheet("background-color: red")
        else:
            self.setStyleSheet("background-color: black")



class Game(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"AI Game")
        window = QWidget()
        layout = QHBoxLayout()
        #self.setCentralWidget(window)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        layout.addLayout(self.grid)
        window.setLayout(layout)
        self.setCentralWidget(window)

        self.init_map()


        self.show()

    def init_map(self):
        """Adds boxes on GUI"""

        for r in range(4):
            for c in range(4):
                box = Box()
                self.grid.addWidget(box, r, c)
                print(r, c)


app = QApplication(sys.argv)
ex = Game()
sys.exit(app.exec_())
