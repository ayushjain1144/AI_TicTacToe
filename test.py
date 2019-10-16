
def is_horizontal_mapping(state):
    """Returns -1 if no mapping, 0 if mapping for human, 1 if mapping for AI"""

    record_clicked = state
    for i in range(4):
        for j in range(2):
            if min(record_clicked[i][j:j+3]) == max(record_clicked[i][j:j+3]) and record_clicked[i][j] != -1:
                return record_clicked[i][j]

    return -1

def is_vertical_mapping(state):
    """Returns -1 if no mapping, 0 if mapping for human, 1 if mapping for AI"""

    record_clicked = state
    for i in range(2):
        for j in range(4):
            if min(list((record_clicked[i][j], record_clicked[i+1][j], record_clicked[i+2][j]))) == max(list((record_clicked[i][j], record_clicked[i+1][j], record_clicked[i+2][j]))) and record_clicked[i][j] != -1:
                return record_clicked[i][j]

    return -1

def is_diagonal_mapping(state):
    """Returns -1 if no mapping, 0 if mapping for human, 1 if mapping for AI"""

    record_clicked = state
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


state = [[-1, -1, -1, -1], [-1, -1, -1, 1], [-1, -1, 1, 1], [-1, -1, 1, -1]]



def valid_moves(topmost_filled_state):

    list = []

    counter = 0
    for i in topmost_filled_state:
        if i != 3:
            list.append(counter)
        counter = counter + 1
    return list

topmost_filled = [3, 2, 2, 1]

print(valid_moves(topmost_filled))
