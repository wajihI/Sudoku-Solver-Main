from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False

def valid(bo, num, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)
    return None

def generate_puzzle(difficulty):
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(board)
    attempts = difficulty
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while board[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        backup = board[row][col]
        board[row][col] = 0

        copy_board = [row[:] for row in board]

        if not unique_solution(copy_board):
            board[row][col] = backup
            attempts -= 1
    return board

def fill_board(bo):
    number_list = list(range(1, 10))
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                random.shuffle(number_list)
                for num in number_list:
                    if valid(bo, num, (i, j)):
                        bo[i][j] = num
                        if solve(bo):
                            return True
                        bo[i][j] = 0
                return False
    return True

def unique_solution(bo):
    solution_count = 0

    def solve_and_count(bo):
        nonlocal solution_count
        find = find_empty(bo)
        if not find:
            solution_count += 1
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(bo, i, (row, col)):
                bo[row][col] = i

                if solve_and_count(bo):
                    if solution_count > 1:
                        return True

                bo[row][col] = 0

        return False

    solve_and_count(bo)
    return solution_count == 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    difficulty = int(request.form['difficulty'])
    board = generate_puzzle(difficulty)
    return jsonify(board)

@app.route('/solve', methods=['POST'])
def solve_puzzle():
    board = request.json['board']
    if solve(board):
        return jsonify(board)
    else:
        return jsonify({"error": "No solution exists for this puzzle!"}), 400

if __name__ == '__main__':
    app.run(debug=True)
