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
import threading

val = 0
lock = threading.Lock()
################ FIND A WAY TO CALL AI ACTION AGENT ###########################

"""
class Box(QWidget):

    is_clicked = pyqtSignal()
    is_clickedby_human = pyqtSignal()
    is_clickedby_AI = pyqtSignal()

    # -1 for not clickedby_human
    # 0 for clicked by human
    # 1 for clicked by AI

    global lock

    def __init__(self):

        super().__init__()

        self.topmost_filled = -1
        self.record_clicked = [-1, -1, -1, -1]
        self.color_list = ["grey", "green", "red"]
        self.mouseReleaseEvent = self.clickedby_human

    def clickedby_human(self, event):


        if self.topmost_filled == 3:
            print("This column is already filled")
            return


        self.topmost_filled = self.topmost_filled + 1
        self.record_clicked[self.topmost_filled] = 0
        #turn.toggle_turn()
        #self.setEnabled = False
        self.update()
        lock.release()


    def is_clickedby_AI(self):

        if self.topmost_filled == 3:
            print("This column is already filled")
            return -1

        self.topmost_filled = self.topmost_filled + 1
        self.record_clicked[self.topmost_filled] = 1
        print("AI DID ITS JOB")
        #turn.toggle_turn()
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
                pane.setBrush(Qt.red)

            pane.drawRect(0, i * width, width, width)

"""

class Game(QMainWindow):

    def __init__(self):
        super().__init__()

        self.topmost_filled = [-1, -1, -1, -1]
        self.record_clicked = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]

        self.color_list = ["grey", "green", "red"]
        self.mouseReleaseEvent = self.clickedby_human

        self.setWindowTitle(f"AI Game")
        self.window = QWidget()
        #layout = QHBoxLayout()
        #self.setCentralWidget(window)

        #self.layout = QHBoxLayout()
        #self.layout.setSpacing(0)
        """
        for r in range(4):
            box = make_box()
            self.layout.addWidget(box)
        """

        #window.setLayout(self.layout)
        self.setCentralWidget(self.window)
        self.resize(360, 360)

        self.update()
        self.show()
        #self.turn_decider()

    def determine_clicked_column(self, event):

        x = int(event.pos().x() / 90)
        return x

    def clickedby_human(self, event):

        col = self.determine_clicked_column(event)

        if self.topmost_filled[col] == 3:
            print("This column is already filled")
            return


        self.topmost_filled[col] = self.topmost_filled[col] + 1
        self.record_clicked[col][self.topmost_filled[col]] = 0
        #turn.toggle_turn()
        #self.setEnabled = False
        self.update()

        ######Check for goal here################
        self.action_by_AI()



    def is_clickedby_AI(self, col):

        #col = self.determine_clicked_column(event)

        if self.topmost_filled[col] == 3:
            print("This column is already filled")
            return -1

        self.topmost_filled[col] = self.topmost_filled[col] + 1
        self.record_clicked[col][self.topmost_filled[col]] = 1
        print("AI DID ITS JOB")
        #turn.toggle_turn()
        self.update()



    def paintEvent(self, event):

        print("bfrb")
        pane = QPainter(self)
        pane.setRenderHint(QPainter.Antialiasing)

        width = 90
        for j in range(4):
            for i in range(4):

                if self.record_clicked[i][j] == -1:
                    pane.setBrush(Qt.gray)
                elif self.record_clicked[i][j] == 0:
                    pane.setBrush(Qt.green)
                else:
                    pane.setBrush(Qt.red)

                pane.drawRect(i * width, j * width, width, width)


    def action_by_AI(self):

        # call minimax algorithm for calculating number
        number = 1
        self.is_clickedby_AI(number)

            #self.action_by_human()

"""


    def test(self, num):
        self.turn_decider()

    def turn_decider(self):

        global lock


        #human = threading.Thread(target=, args=(lock,))
        ai = threading.Thread(target=self.action_by_AI, args=(lock,))
        #human = threading.Thread(target=self.action_by_human, args=(lock,))

        ai.start()
        human.start()

        ai.join()
        human.join()

"""


app = QApplication(sys.argv)
ex = Game()
sys.exit(app.exec_())

# turn = 0 means human's turn`
# turn = 1 means AI's turn
