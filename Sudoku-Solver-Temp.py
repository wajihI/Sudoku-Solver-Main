import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# Sudoku Solver Functions
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

# Tkinter UI Functions
def update_board(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, str(board[i][j]))
                entries[i][j].config(state='disabled', disabledbackground='light grey')
            else:
                entries[i][j].config(state='normal', bg='white')
                entries[i][j].delete(0, tk.END)

def generate_new_puzzle():
    global current_board, original_board
    difficulty = difficulty_selection()
    if difficulty is not None:
        current_board = generate_puzzle(difficulty)
        original_board = [row[:] for row in current_board]
        update_board(current_board)

def solve_puzzle():
    global current_board, original_board
    current_board = [row[:] for row in original_board]
    if solve(current_board):
        update_board(current_board)
    else:
        messagebox.showerror("Error", "No solution exists for this puzzle!")

def get_board_from_entries():
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            value = entries[i][j].get()
            if value == "":
                row.append(0)
            else:
                row.append(int(value))
        board.append(row)
    return board

def user_solve():
    global current_board
    current_board = get_board_from_entries()
    solve_puzzle()

def validate_input(event):
    entry = event.widget
    value = entry.get()
    if value not in "123456789":
        entry.delete(0, tk.END)

def difficulty_selection():
    difficulty = simpledialog.askinteger("Select Difficulty", "Enter difficulty level (1-10):", minvalue=1, maxvalue=10)
    return difficulty

# Tkinter UI Setup
root = tk.Tk()
root.title("Sudoku Solver")

entries = []
for i in range(9):
    row_entries = []
    for j in range(9):
        entry = tk.Entry(root, width=3, font=('Arial', 18), justify='center', validate='key')
        entry.grid(row=i, column=j, padx=5, pady=5)
        entry.bind('<KeyRelease>', validate_input)
        row_entries.append(entry)
    entries.append(row_entries)

btn_generate = tk.Button(root, text="Generate Puzzle", command=generate_new_puzzle)
btn_generate.grid(row=10, column=0, columnspan=3)

btn_solve = tk.Button(root, text="Solve Puzzle", command=user_solve)
btn_solve.grid(row=10, column=3, columnspan=3)

btn_clear = tk.Button(root, text="Clear Board", command=lambda: update_board([[0]*9 for _ in range(9)]))
btn_clear.grid(row=10, column=6, columnspan=3)

generate_new_puzzle()

root.mainloop()