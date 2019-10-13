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
import turn

################ ERROR HERE ###########################


class Box(QWidget):

    is_clicked = pyqtSignal()
    is_clickedby_human = pyqtSignal()
    is_clickedby_AI = pyqtSignal()

    # -1 for not clickedby_human
    # 0 for clicked by human
    # 1 for clicked by AI


    def __init__(self):

        super().__init__()

        #self.setStyleSheet("background-color: black")
        #self.initialize()
        self.topmost_filled = -1
        self.record_clicked = [-1, -1, -1, -1]
        self.color_list = ["grey", "green", "red"]
        self.mouseReleaseEvent = self.clickedby_human

    def clickedby_human(self, event):

        if turn.val == 0:

            if self.topmost_filled == 3:
                print("This column is already filled")
                return


            self.topmost_filled = self.topmost_filled + 1
            self.record_clicked[self.topmost_filled] = 0
            turn.toggle_turn()
            #self.setEnabled = False
            self.update()

    def is_clickedby_AI(self):

        if turn.val == 1:

            if self.topmost_filled == 3:
                print("This column is already filled")
                return -1

            self.topmost_filled = self.topmost_filled + 1
            self.record_clicked[self.topmost_filled] = 1
            turn.toggle_turn()
            self.update()



    def paintEvent(self, event):

        pane = QPainter(self)
        pane.setRenderHint(QPainter.Antialiasing)

        width = 90
        for i in range(4):

            if self.record_clicked[i] == -1:
                pane.setBrush(Qt.gray)
            elif self.record_clicked[i] == 0:
                pane.setBrush(Qt.green)
            else:
                pane.setBrush(Qt.black)

            pane.drawRect(0, i * width, width, width)    



class Game(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"AI Game")
        window = QWidget()
        #layout = QHBoxLayout()
        #self.setCentralWidget(window)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        for r in range(4):
            box = Box()
            self.layout.addWidget(box)


        window.setLayout(self.layout)
        self.setCentralWidget(window)
        self.resize(360, 360)
        self.show()





app = QApplication(sys.argv)
ex = Game()
sys.exit(app.exec_())

# turn = 0 means human's turn`
# turn = 1 means AI's turn
