# Sudoku-Solver-Main
Sudoku game with complete functionalities

## Running the program: 
Due to issues with Heroku (payment problem) and other factors, run the Sudoku-Solver-Temp file for a illustration of how the sudoku program would work.

### Requirements:
To run the app.py file, flask and python need to be installed.

### Backtracking Algorithm (How it works)

1. Pick an empty square
2. Try all possible numbers
3. Identify one that works (based on Sudoku rules e.g. only 1 unique number per row, column, square/grid)
4. Repeat above steps for the next empty square
5. When reached a square where number is invalid, backtrack to previous square and exhaust remaining numbers.
6. If number is still invalid, backtrack again and repeat

Essentially, we are completing one square at a time and recursively checking if the solution works until we reach one that works. Backtrack to previous one if it is invalid. More efficient and effective than the naive approach of forcifully checking every square and manually repeating entire sudoku to solve it.
