"""
#######################
NAME: AYUSH JAIN
ID: 2017A7PS0093P
######################
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from copy import deepcopy
import random
import sys
import time
import turn
import threading

val = 0
lock = threading.Lock()
inf = float('inf')

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
        self.count_recursive = 0
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
        print(col)
        if self.topmost_filled[col] == 3:
            print("This column is already filled")
            return


        self.topmost_filled[col] = self.topmost_filled[col] + 1
        self.record_clicked[self.topmost_filled[col]][col] = 0
        #turn.toggle_turn()
        #self.setEnabled = False
        self.update()

        if self.is_terminal_state(self.record_clicked):
            print("Human Won")
            sys.exit()
        self.action_by_AI()
        if self.is_terminal_state(self.record_clicked):
            print("AI Won")
            sys.exit()



    def is_clickedby_AI(self, col):

        #col = self.determine_clicked_column(event)

        if self.topmost_filled[col] == 3:
            print("This column is already filled")
            return -1

        self.topmost_filled[col] = self.topmost_filled[col] + 1
        self.record_clicked[self.topmost_filled[col]][col] = 1
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

                if self.record_clicked[j][i] == -1:
                    pane.setBrush(Qt.gray)
                elif self.record_clicked[j][i] == 0:
                    pane.setBrush(Qt.green)
                else:
                    pane.setBrush(Qt.red)

                pane.drawRect(i * width, j * width, width, width)


    def action_by_AI(self):

        # call minimax algorithm for calculating number
        state = deepcopy(self.record_clicked)
        topmost_filled_state = deepcopy(self.topmost_filled)
        number = self.minimax(state, topmost_filled_state)
        #print(f"Count Recursion: {self.count_recursive}")
        self.is_clickedby_AI(number)
        #print(self.topmost_filled)


    def is_horizontal_mapping(self, state):
        """Returns -1 if no mapping, 0 if mapping for human, 1 if mapping for AI"""

        record_clicked = state
        for i in range(4):
            for j in range(2):
                if min(record_clicked[i][j:j+3]) == max(record_clicked[i][j:j+3]) and record_clicked[i][j] != -1:
                    return record_clicked[i][j]

        return -1

    def is_vertical_mapping(self, state):
        """Returns -1 if no mapping, 0 if mapping for human, 1 if mapping for AI"""

        record_clicked = state
        for i in range(2):
            for j in range(4):
                if min(list((record_clicked[i][j], record_clicked[i+1][j], record_clicked[i+2][j]))) == max(list((record_clicked[i][j], record_clicked[i+1][j], record_clicked[i+2][j]))) and record_clicked[i][j] != -1:
                    return record_clicked[i][j]

        return -1

    def is_diagonal_mapping(self, state):
        """Returns -1 if no mapping, 0 if mapping for human, 1 if mapping for AI"""

        record_clicked = state
        #print(record_clicked)
        for i in range(2):
            for j in range(4):
                if record_clicked[i][j] != -1:
                    if int(j / 2) == 0:
                        if min(list((record_clicked[i][j], record_clicked[i+1][j+1], record_clicked[i+2][j+2]))) == max(list((record_clicked[i][j], record_clicked[i+1][j+1], record_clicked[i+2][j+2]))):
                            return record_clicked[i][j]
                    else:
                        if min(list((record_clicked[i][j], record_clicked[i+1][j-1], record_clicked[i+2][j-2]))) == max(list((record_clicked[i][j], record_clicked[i+1][j-1], record_clicked[i+2][j-2]))):
                            return record_clicked[i][j]
        return -1



    def utility_value_for_terminal(self, state):

        record_clicked = state
        if self.is_terminal_state(state):
            val = max(list((self.is_diagonal_mapping(state), self.is_horizontal_mapping(state), self.is_vertical_mapping(state))))

            # No Mapping: draw
            if val == -1:
                return 0
            # Human Wins
            elif val == 0:
                return -1
            # AI Wins
            else:
                return 1

    def is_terminal_state(self, state):

        # Either complete mapping or completely filled

        record_clicked = state
        val = max(list((self.is_diagonal_mapping(state), self.is_horizontal_mapping(state), self.is_vertical_mapping(state))))

        if val != -1:
            return True

        else:
            for i in range(4):
                for j in range(4):
                    if record_clicked[i][j] != -1:

                        return False
        return True


    # state passed through self
    def minimax(self, state, topmost_filled_state):
        """Returns the action"""

        win = -1
        number = 0
        for a in self.valid_moves(topmost_filled_state):
            new_state, new_topmost_filled_state = self.nextState(state, topmost_filled_state, a, 1)
            v = self.minvalue(new_state, new_topmost_filled_state)
            if v > win:
                win = v
                number = a

        return number

    def valid_moves(self, topmost_filled_state):

        list = []

        counter = 0
        for i in topmost_filled_state:
            if i != 3:
                list.append(counter)
            counter = counter + 1
        return list

    def maxvalue(self, state, topmost_filled_state):
        """Returns a utility value"""

        self.count_recursive = self.count_recursive + 1
        if self.is_terminal_state(state):
            return self.utility_value_for_terminal(state)
        v = -1
        for a in self.valid_moves(topmost_filled_state):
            new_state, new_topmost_filled_state = self.nextState(state, topmost_filled_state, a, 1)
            v = max(v, self.minvalue(new_state, new_topmost_filled_state))

        #print(f"maxvalue: {v}")
        return v

    def minvalue(self, state, topmost_filled_state):
        """Returns a utility value"""
        self.count_recursive = self.count_recursive + 1
        if self.is_terminal_state(state):
            return -self.utility_value_for_terminal(state)
        v = 1
        for a in self.valid_moves(topmost_filled_state):
            new_state, new_topmost_filled_state = self.nextState(state, topmost_filled_state, a, 0)
            v = min(v, self.maxvalue(new_state, new_topmost_filled_state))
        #print(f"minvalue: {v}")
        return v

    def nextState(self, state, topmost_filled_state, a, val):

        new_state = deepcopy(state)
        new_topmost_filled_state = deepcopy(topmost_filled_state)

        if new_topmost_filled_state[a] == 3:
            print(f"This column: {a} is already filled")
            return


        new_topmost_filled_state[a] = new_topmost_filled_state[a] + 1
        new_state[new_topmost_filled_state[a]][a] = val

        #print(f"inside nextState: {new_state}")
        #print(f"inside nextState topmost_filled: {new_topmost_filled_state}")
        return (new_state, new_topmost_filled_state)


            #self.action_by_human()

    ###############################################################################

    def minimax_ab(self, state, topmost_filled_state):
        """Returns the action"""

        win = -1
        number = 0

        beta = inf

        for a in self.valid_moves(topmost_filled_state):
            new_state, new_topmost_filled_state = self.nextState(state, topmost_filled_state, a, 1)
            v = self.minvalue_ab(new_state, new_topmost_filled_state, win, beta)
            if  v > win:
                win = v
                number = a

        return number

    def minvalue_ab(self, state, topmost_filled_state, alpha, beta):
        """Returns a utility value"""
        self.count_recursive = self.count_recursive + 1
        if self.is_terminal_state(state):
            return -self.utility_value_for_terminal(state)
        v = 1
        for a in self.valid_moves(topmost_filled_state):
            new_state, new_topmost_filled_state = self.nextState(state, topmost_filled_state, a, 0)
            v = min(v, self.maxvalue_ab(new_state, new_topmost_filled_state, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        #print(f"minvalue: {v}")
        return v

    def maxvalue_ab(self, state, topmost_filled_state, alpha, beta):
        """Returns a utility value"""

        self.count_recursive = self.count_recursive + 1
        if self.is_terminal_state(state):
            return self.utility_value_for_terminal(state)
        v = -1
        for a in self.valid_moves(topmost_filled_state):
            new_state, new_topmost_filled_state = self.nextState(state, topmost_filled_state, a, 1)
            v = max(v, self.minvalue_ab(new_state, new_topmost_filled_state, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        #print(f"maxvalue: {v}")
        return v


class FirstWidget(QMainWindow):

    def __init__(self):
        super().__init__()


        self.setWindowTitle(f"AI Game")
        window = QWidget()




        self.normal_button = QPushButton()
        self.normal_button.setFixedSize(QSize(100, 100))
        self.normal_button.setText("Without a/b")
        self.normal_button.pressed.connect(self.open_game)
        self.ab_button = QPushButton()
        self.ab_button.setFixedSize(QSize(100, 100))
        self.ab_button.setText("With a/b")

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.label.setText("Choose Algorithm")
        font = self.label.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label.setFont(font)

        layout =QHBoxLayout()
        layout.addWidget(self.normal_button)
        layout.addWidget(self.ab_button)

        vert_layout = QVBoxLayout()
        vert_layout.addWidget(self.label)
        vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        self.resize(360, 360)
        self.show()

    def open_game(self):

        self.win = Game()
        self.win.show()
        self.close()





"""

app = QApplication(sys.argv)
ex = Game()
sys.exit(app.exec_())
"""

app = QApplication(sys.argv)
ex = FirstWidget()
sys.exit(app.exec_())
# turn = 0 means human's turn`
# turn = 1 means AI's turn
