import sys
import copy

# Reference:
# The Priority Queue used is from the queue library that is provided by Python


class State:
    # Definition of a state
    def __init__(self, board, parent=None):
        self.board = copy.deepcopy(board)
        self.parent = parent
        if (self.parent != None):
            self.cost = parent.cost+1
        else:
            self.cost = 0

    def __gt__(self, other):
        return get_total(self) > get_total(other)

    def __lt__(self, other):
        return get_total(self) < get_total(other)


def get_empty_cells(state):
    # Get the positions of the two 0 cells
    empty_one_x = -1
    empty_one_y = -1

    for i in range(5):
        for j in range(4):
            if (state.board[i][j] == 0):
                if (empty_one_x == -1):
                    empty_one_x = i
                    empty_one_y = j
                else:
                    return [empty_one_x, empty_one_y, i, j]


def get_cao_cao(state):
    # Get the position of Cao cao
    for i in range(5):
        for j in range(4):
            if (state.board[i][j] == 1):
                return [i, j]


def state_to_key(state):
    # Convert given state to a unique key that contains the board info
    result = ""

    for i in range(5):
        for j in range(4):
            if(state.board[i][j] == 2 or state.board[i][j] == 3
                    or state.board[i][j] == 4 or state.board[i][j] == 5):

                result += "4"
            else:
                result += str(state.board[i][j])
    return result


def state_to_output(state):
    # Convert state to output ready to be printed in file
    result = ""

    for i in range(5):
        for j in range(4):
            result += str(state.board[i][j])
        result += "\n"
    result += "\n"
    return result


def states_to_output(id, algo, init_state, end_state, expanded):
    # Convert the entire solution to output ready to be printed in file
    outfile_name = f"puzzle{id}sol_{algo}.txt"
    outfile = open(outfile_name, "w")

    outfile.write("Initial state:\n")
    outfile.write(state_to_output(init_state))

    outfile.write(f"Cost of the solution: {end_state.cost}\n")
    outfile.write("\n")

    outfile.write(f"Number of states expanded: {expanded}\n")
    outfile.write("\n")

    outfile.write("Solution:\n")
    outfile.write("\n")

    solution = []
    state_count = end_state.cost
    while (end_state != None):
        solution.append(end_state)
        end_state = end_state.parent
    for i in range(state_count+1):
        outfile.write(f"{i}\n")
        outfile.write(state_to_output(solution[state_count-i]))

    outfile.close()


def read_puzzle(id):
    # Read puzzle info from a file
    puzzlefile_name = f"puzzle{id}.txt"
    puzzlefile = open(puzzlefile_name, "r")
    init_state = State([[-1, -1, -1, -1], [-1, -1, -1, -1], [
        -1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]])

    for i in range(5):
        line = puzzlefile.readline()
        for j in range(4):
            chara = line[j]
            init_state.board[i][j] = int(chara)

    puzzlefile.close()
    return init_state


def is_goal(state):
    # Goal test
    if (state.board[3][1] == 1 and state.board[4][1] == 1
            and state.board[3][2] == 1 and state.board[4][2] == 1):
        return True
    else:
        return False


def move_single(state, empty_x, empty_y):
    # Move a 1x1 piece if possible
    children = []

    # Move down
    if (empty_x > 0 and state.board[empty_x-1][empty_y] == 7):
        child = State(state.board, state)
        child.board[empty_x-1][empty_y] = 0
        child.board[empty_x][empty_y] = 7
        children.append(child)

    # Move up
    if (empty_x < 4 and state.board[empty_x+1][empty_y] == 7):
        child = State(state.board, state)
        child.board[empty_x+1][empty_y] = 0
        child.board[empty_x][empty_y] = 7
        children.append(child)

    # Move right
    if (empty_y > 0 and state.board[empty_x][empty_y-1] == 7):
        child = State(state.board, state)
        child.board[empty_x][empty_y-1] = 0
        child.board[empty_x][empty_y] = 7
        children.append(child)

    # Move left
    if (empty_y < 3 and state.board[empty_x][empty_y+1] == 7):
        child = State(state.board, state)
        child.board[empty_x][empty_y+1] = 0
        child.board[empty_x][empty_y] = 7
        children.append(child)

    return children


def move_horizontal(state, empty_one_x, empty_one_y, empty_two_x, empty_two_y):
    # Move a 1x2 or 2x2 piece if possible
    children = []

    # Move down
    if (empty_one_x > 0 and empty_one_x == empty_two_x and abs(empty_one_y - empty_two_y) == 1
            and state.board[empty_one_x-1][empty_one_y] == state.board[empty_two_x-1][empty_two_y]):
        temp = state.board[empty_one_x-1][empty_one_y]
        if (temp != 7):
            child = State(state.board, state)
            if (temp != 1):
                child.board[empty_one_x-1][empty_one_y] = 0
                child.board[empty_two_x-1][empty_two_y] = 0
                child.board[empty_one_x][empty_one_y] = temp
                child.board[empty_two_x][empty_two_y] = temp
            else:
                child.board[empty_one_x-2][empty_one_y] = 0
                child.board[empty_two_x-2][empty_two_y] = 0
                child.board[empty_one_x][empty_one_y] = 1
                child.board[empty_two_x][empty_two_y] = 1
            children.append(child)

    # Move up
    if (empty_one_x < 4 and empty_one_x == empty_two_x and abs(empty_one_y - empty_two_y) == 1
            and state.board[empty_one_x+1][empty_one_y] == state.board[empty_two_x+1][empty_two_y]):
        temp = state.board[empty_one_x+1][empty_one_y]
        if (temp != 7):
            child = State(state.board, state)
            if (temp != 1):
                child.board[empty_one_x+1][empty_one_y] = 0
                child.board[empty_two_x+1][empty_two_y] = 0
                child.board[empty_one_x][empty_one_y] = temp
                child.board[empty_two_x][empty_two_y] = temp
            else:
                child.board[empty_one_x+2][empty_one_y] = 0
                child.board[empty_two_x+2][empty_two_y] = 0
                child.board[empty_one_x][empty_one_y] = 1
                child.board[empty_two_x][empty_two_y] = 1
            children.append(child)

    # Move right
    if (empty_one_y > 1 and state.board[empty_one_x][empty_one_y-1] == state.board[empty_one_x][empty_one_y-2]):
        temp = state.board[empty_one_x][empty_one_y-1]
        if (temp != 1 and temp != 7):
            child = State(state.board, state)
            child.board[empty_one_x][empty_one_y-2] = 0
            child.board[empty_one_x][empty_one_y] = temp
            children.append(child)
    if (empty_two_y > 1 and state.board[empty_two_x][empty_two_y-1] == state.board[empty_two_x][empty_two_y-2]):
        temp = state.board[empty_two_x][empty_two_y-1]
        if (temp != 1 and temp != 7):
            child = State(state.board, state)
            child.board[empty_two_x][empty_two_y-2] = 0
            child.board[empty_two_x][empty_two_y] = temp
            children.append(child)

    # Move left
    if (empty_one_y < 2 and state.board[empty_one_x][empty_one_y+1] == state.board[empty_one_x][empty_one_y+2]):
        temp = state.board[empty_one_x][empty_one_y+1]
        if (temp != 1 and temp != 7):
            child = State(state.board, state)
            child.board[empty_one_x][empty_one_y+2] = 0
            child.board[empty_one_x][empty_one_y] = temp
            children.append(child)
    if (empty_two_y < 2 and state.board[empty_two_x][empty_two_y+1] == state.board[empty_two_x][empty_two_y+2]):
        temp = state.board[empty_two_x][empty_two_y+1]
        if (temp != 1 and temp != 7):
            child = State(state.board, state)
            child.board[empty_two_x][empty_two_y+2] = 0
            child.board[empty_two_x][empty_two_y] = temp
            children.append(child)

    return children


def move_vertical(state, empty_one_x, empty_one_y, empty_two_x, empty_two_y):
    # Move a 2x1 or 2x2 piece if possible
    children = []

    # Move down
    if (empty_one_x > 1 and state.board[empty_one_x-1][empty_one_y] == state.board[empty_one_x-2][empty_one_y]):
        temp = state.board[empty_one_x-1][empty_one_y]
        if (temp != 1 and temp != 7):
            child = State(state.board, state)
            child.board[empty_one_x-2][empty_one_y] = 0
            child.board[empty_one_x][empty_one_y] = temp
            children.append(child)
    if (empty_two_x > 1 and state.board[empty_two_x-1][empty_two_y] == state.board[empty_two_x-2][empty_two_y]):
        temp = state.board[empty_two_x-1][empty_two_y]
        if (temp != 1 and temp != 7):
            child = State(state.board, state)
            child.board[empty_two_x-2][empty_two_y] = 0
            child.board[empty_two_x][empty_two_y] = temp
            children.append(child)

    # Move up
    if (empty_one_x < 3 and state.board[empty_one_x+1][empty_one_y] == state.board[empty_one_x+2][empty_one_y]):
        temp = state.board[empty_one_x+1][empty_one_y]
        if (temp != 1 and temp != 7):
            child = State(state.board, state)
            child.board[empty_one_x+2][empty_one_y] = 0
            child.board[empty_one_x][empty_one_y] = temp
            children.append(child)
    if (empty_two_x < 3 and state.board[empty_two_x+1][empty_two_y] == state.board[empty_two_x+2][empty_two_y]):
        temp = state.board[empty_two_x+1][empty_two_y]
        if (temp != 1 and temp != 7):
            child = State(state.board, state)
            child.board[empty_two_x+2][empty_two_y] = 0
            child.board[empty_two_x][empty_two_y] = temp
            children.append(child)

    # Move right
    if (empty_one_y > 0 and empty_one_y == empty_two_y and abs(empty_one_x - empty_two_x) == 1
            and state.board[empty_one_x][empty_one_y-1] == state.board[empty_two_x][empty_two_y-1]):
        temp = state.board[empty_one_x][empty_one_y-1]
        if (temp != 7):
            child = State(state.board, state)
            if (temp != 1):
                child.board[empty_one_x][empty_one_y-1] = 0
                child.board[empty_two_x][empty_two_y-1] = 0
                child.board[empty_one_x][empty_one_y] = temp
                child.board[empty_two_x][empty_two_y] = temp
            else:
                child.board[empty_one_x][empty_one_y-2] = 0
                child.board[empty_two_x][empty_two_y-2] = 0
                child.board[empty_one_x][empty_one_y] = 1
                child.board[empty_two_x][empty_two_y] = 1
            children.append(child)

    # Move left
    if (empty_one_y < 3 and empty_one_y == empty_two_y and abs(empty_one_x - empty_two_x) == 1
            and state.board[empty_one_x][empty_one_y+1] == state.board[empty_two_x][empty_two_y+1]):
        temp = state.board[empty_one_x][empty_one_y+1]
        if (temp != 7):
            child = State(state.board, state)
            if (temp != 1):
                child.board[empty_one_x][empty_one_y+1] = 0
                child.board[empty_two_x][empty_two_y+1] = 0
                child.board[empty_one_x][empty_one_y] = temp
                child.board[empty_two_x][empty_two_y] = temp
            else:
                child.board[empty_one_x][empty_one_y+2] = 0
                child.board[empty_two_x][empty_two_y+2] = 0
                child.board[empty_one_x][empty_one_y] = 1
                child.board[empty_two_x][empty_two_y] = 1
            children.append(child)

    return children


def get_successors(state):
    # Get the empty cells of the current board
    empty_cells = get_empty_cells(state)
    empty_one_x = empty_cells[0]
    empty_one_y = empty_cells[1]
    empty_to_x = empty_cells[2]
    empty_two_y = empty_cells[3]

    # Join all the possible movements
    successors = move_single(state, empty_one_x, empty_one_y)
    successors += move_single(state, empty_to_x, empty_two_y)
    successors += move_horizontal(state, empty_one_x,
                                  empty_one_y, empty_to_x, empty_two_y)
    successors += move_vertical(state, empty_one_x,
                                empty_one_y, empty_to_x, empty_two_y)
    return successors


def get_cost(state):
    # Get the g function value
    return state.cost


def get_heuristic(state):
    # Get the heuristic function value
    cao_cao = get_cao_cao(state)
    cao_cao_x = cao_cao[0]
    cao_cao_y = cao_cao[1]

    heuristic = 3*(abs(cao_cao_x-3) + abs(cao_cao_y-1))
    return heuristic


def get_total(state):
    # Get the g function + heuristic function value
    total = get_cost(state)+get_heuristic(state)
    return total
