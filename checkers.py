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
import threading
from functools import partial

val = 0
lock = threading.Lock()
inf = float('inf')

is_ai = 0
is_ab = 0
is_ai_win = 0

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



        #window.setLayout(self.layout)
        self.count_recursive = 0
        self.setCentralWidget(self.window)
        self.resize(360, 360)
        self.center()
        self.update()

        if is_ai == 1:
            self.action_by_AI()

        self.show()
        #self.turn_decider()

    def end_game(self):

        self.setEnabled(False)
        self.win = ThirdWidget()
        self.win.show()
        self.close()


    def determine_clicked_column(self, event):

        x = int(event.pos().x() / 90)
        return x

    def clickedby_human(self, event):

        global is_ai_win
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
            is_ai_win = 0
            self.setWindowTitle("HUMAN WON !!!!")
            self.end_game()
            return
            #sys.exit()
        self.action_by_AI()

        if self.is_terminal_state(self.record_clicked):
            print("AI Won")
            is_ai_win = 1
            self.setWindowTitle("AI WON !!!!")
            self.end_game()
            #sys.exit()



    def is_clickedby_AI(self, col):

        #col = self.determine_clicked_column(event)

        if self.topmost_filled[col] == 3:
            print(f"This column {col} is already filled")
            return -1

        self.topmost_filled[col] = self.topmost_filled[col] + 1
        self.record_clicked[self.topmost_filled[col]][col] = 1
        print("AI DID ITS JOB")
        #turn.toggle_turn()
        self.update()



    def paintEvent(self, event):


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

        pen = QPen(Qt.blue, 6, Qt.SolidLine)
        pane.setPen(pen)

        x1 = 0
        for i in self.topmost_filled:

            y1 = i + 1
            pane.drawLine(x1, y1 * 90, x1 + 90, y1 * 90)
            x1 = x1 + 90


    def action_by_AI(self):

        # call minimax algorithm for calculating number
        state = deepcopy(self.record_clicked)
        topmost_filled_state = deepcopy(self.topmost_filled)

        if is_ab == 0:
            number = self.minimax(state, topmost_filled_state)
        else:
            #print("Here")
            number = self.minimax_ab(state, topmost_filled_state)
            if number == 0:
                print(topmost_filled_state)
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
                    if record_clicked[i][j] == -1:

                        return False
        return True


    # state passed through self
    def minimax(self, state, topmost_filled_state):
        """Returns the action"""

        win = -1
        number = 0

        #print("Here0")
        for a in self.valid_moves(topmost_filled_state):
            new_state, new_topmost_filled_state = self.nextState(state, topmost_filled_state, a, 1)
            v = self.minvalue(new_state, new_topmost_filled_state)
            if v > win:
                win = v
                number = a
        #print("Here1")

        if win == -1:
            while(topmost_filled_state[number] == 3 and number < 3):
                #print("caught")
                number = number + 1

        #print("Here2")

        #if number == 0:
            #print(win, topmost_filled_state)

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
            return self.utility_value_for_terminal(state)
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


        return (new_state, new_topmost_filled_state)


            #self.action_by_human()

    ###############################################################################

    def minimax_ab(self, state, topmost_filled_state):
        """Returns the action"""

        win = -1
        number = 0

        beta = 1

        for a in self.valid_moves(topmost_filled_state):
            new_state, new_topmost_filled_state = self.nextState(state, topmost_filled_state, a, 1)
            v = self.minvalue_ab(new_state, new_topmost_filled_state, win, beta)
            if  v > win:
                win = v
                number = a

        if win == -1:
            while(topmost_filled_state[number] == 3 and number < 3):
                #print("caught")
                number = number + 1

        return number

    def minvalue_ab(self, state, topmost_filled_state, alpha, beta):
        """Returns a utility value"""
        self.count_recursive = self.count_recursive + 1
        if self.is_terminal_state(state):
            return self.utility_value_for_terminal(state)
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

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class FirstWidget(QMainWindow):

    def __init__(self):
        super().__init__()


        self.setWindowTitle(f"AI Game")
        window = QWidget()




        self.normal_button = QPushButton()
        self.normal_button.setFixedSize(QSize(100, 100))
        self.normal_button.setText("Without a/b")
        self.normal_button.pressed.connect(partial(self.open_game, 0))

        self.ab_button = QPushButton()
        self.ab_button.setFixedSize(QSize(100, 100))
        self.ab_button.setText("With a/b")
        self.ab_button.pressed.connect(partial(self.open_game, 1))
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
        self.center()
        self.show()

    def open_game(self, val):

        global is_ab
        is_ab = val
        self.win = SecondWidget()
        self.win.show()
        self.close()

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class SecondWidget(QMainWindow):

    def __init__(self):
        super().__init__()


        self.setWindowTitle(f"AI Game")
        window = QWidget()




        self.normal_button = QPushButton()
        self.normal_button.setFixedSize(QSize(100, 100))
        self.normal_button.setText("Human")
        self.normal_button.pressed.connect(partial(self.open_game, 0))

        self.ab_button = QPushButton()
        self.ab_button.setFixedSize(QSize(100, 100))
        self.ab_button.setText("AI")
        self.ab_button.pressed.connect(partial(self.open_game, 1))
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.label.setText("Choose First Turn")
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
        self.center()
        self.show()

    def open_game(self, val):

        global is_ai
        is_ai = val
        self.win = Game()
        self.win.show()
        self.close()

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class ThirdWidget(QMainWindow):

    def __init__(self):
        super().__init__()


        self.setWindowTitle(f"AI Game")
        window = QWidget()




        self.normal_button = QPushButton()
        self.normal_button.setFixedSize(QSize(100, 100))
        self.normal_button.setText("Yes")
        self.normal_button.pressed.connect(partial(self.open_game, 1))

        self.ab_button = QPushButton()
        self.ab_button.setFixedSize(QSize(100, 100))
        self.ab_button.setText("No")
        self.ab_button.pressed.connect(partial(self.open_game, 0))
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label1 = QLabel()
        self.label1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        global is_ai_win

        if is_ai_win:
            self.label1.setText("AI WON!!")
        else:
            self.label1.setText("Human WON!!")
        font = self.label1.font()
        font.setPointSize(30)
        font.setWeight(65)
        self.label1.setFont(font)

        self.label.setText("Do you want to play again ?")
        font = self.label.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label.setFont(font)

        layout =QHBoxLayout()
        layout.addWidget(self.normal_button)
        layout.addWidget(self.ab_button)

        vert_layout = QVBoxLayout()
        vert_layout.addWidget(self.label1)
        vert_layout.addWidget(self.label)
        vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        self.resize(360, 360)
        self.center()
        self.show()

    def open_game(self, val):

        if val == 0:
            sys.exit()
        else:
            self.win = FirstWidget()
            self.win.show()
            self.close()


    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


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
