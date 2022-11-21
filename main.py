## coded by Valentin 

from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

# gameboard = np.array([[False, False, False, False, False, False],
#              [False, False, False, False, False, False],
#              [False, False, True, True, True, False],
#              [False, True, True, True, False, False],
#              [False, False, False, False, False, False],
#              [False, False, False, False, False, False]])


size = 50
gameboard = np.random.randint(0, 2, (size, size))

def reset():
    global gameboard
    gameboard = np.random.randint(0, 2, (size, size))

#gameboard=[ [ False for _ in range(6) ] for _ in range(6)]

def sum_up_neighbors(state, row, col):
    nr_neighbors = 0
    for neighbor_row in [row - 1, row, row + 1]:
        for neighbor_col in [col - 1, col, col + 1]:
            if 0 < neighbor_row <= size - 1 and 0 < neighbor_col <= size - 1:
                if row == neighbor_row and col == neighbor_col:
                    continue
                if state[neighbor_row, neighbor_col]:
                    nr_neighbors += 1
    return nr_neighbors

def are_we_alive(nr_neighbors, currently_alive):
    if nr_neighbors < 2:
        return False
    elif nr_neighbors == 2:
        if currently_alive:
            return True
        else:
            return False
    elif nr_neighbors == 3:
        return True
    else:
        return False


def update_state():
    old_state = gameboard.copy()
    for i in range(size):
        for j in range(size):
            nr_neighbors = sum_up_neighbors(old_state, i, j)
            print(i, j, nr_neighbors)
            gameboard[i, j] = are_we_alive(nr_neighbors, old_state[i, j])
    return gameboard

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        if request.form.get('action2') == "reset":
            reset()
        if request.form.get('action1') == "click here to change":
            update_state()
        return render_template('index.html', board=gameboard, black_square="⬛", white_square="⬜")
    elif request.method == 'GET':
        return render_template('index.html', board=gameboard, black_square="⬛", white_square="⬜")
    
if __name__=='__main__':
    app.debug=True
    app.run()