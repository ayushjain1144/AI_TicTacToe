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

        """
        -1: not clicked
        0: clicked by human
        1: clicked by AI
        """
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

    def is_horizontal_mapping(self):
        """Returns -1 if no mapping, 0 if mapping for AI, 1 if mapping for AI"""

        for i in range(4):
            for j in range(2):
                if min(record_clicked[i][j:j+3]) == max(record_clicked[i][j:j+3]) and record_clicked[i][j] != -1:
                    return record_clicked[i][j]

        return -1

    def is_vertical_mapping(self):
        """Returns -1 if no mapping, 0 if mapping for AI, 1 if mapping for AI"""

        for i in range(2):
            for j in range(4):
                if min(list(record_clicked[i][j], record_clicked[i+1][j], record_clicked[i+2][j])) == max(min(list(record_clicked[i][j], record_clicked[i+1][j], record_clicked[i+2][j]))) and record_clicked[i][j] != -1:
                    return record_clicked[i][j]

        return -1

    def is_diagonal_mapping(self):
        """Returns -1 if no mapping, 0 if mapping for AI, 1 if mapping for AI"""

        for i in range(2):
            for j in range(4):
                if record_clicked[i][j] != -1:
                    if int(j / 2) < 0:
                        if min(list(record_clicked[i][j], record_clicked[i+1][j+1], record_clicked[i+2][j+2])) == max(min(list(record_clicked[i][j], record_clicked[i+1][j+1], record_clicked[i+2][j+2]))):
                            return record_clicked[i][j]
                    else:
                        if min(list(record_clicked[i][j], record_clicked[i+1][j-1], record_clicked[i+2][j-2])) == max(min(list(record_clicked[i][j], record_clicked[i+1][j-1], record_clicked[i+2][j-2]))):
                            return record_clicked[i][j]
        return -1



    def utility_value_for_terminal(self):

        if self.is_terminal_state():
            val = max(list(self.is_diagonal_mapping(), self.is_horizontal_mapping(), self.is_vertical_mapping()))

            # No Mapping: draw
            if val == -1:
                return 0
            # Human Wins
            elif val == 0:
                return -1
            # AI Wins
            else:
                return 1

    def is_terminal_state(self):

        # Either complete mapping or completely filled

        val = max(list(self.is_diagonal_mapping(), self.is_horizontal_mapping(), self.is_vertical_mapping()))

        if val != -1:
            return True

        else:
            for i in range(4):
                for j in range(4):
                    if record_clicked[i][j] != -1:

                        return False
        return True


    def minimax(state):
        """Returns the action"""

        return

    def maxvalue(state):
        """Returns a utility value"""

        return

    def minvalue(state):
        """Returns a utility value"""

        return

            #self.action_by_human()







app = QApplication(sys.argv)
ex = Game()
sys.exit(app.exec_())

# turn = 0 means human's turn`
# turn = 1 means AI's turn
