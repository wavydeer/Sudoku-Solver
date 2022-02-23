#!/usr/bin/env python
# coding:utf-8


"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import time

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

# This function searched through the board and see if there are any empty number i.e zeros


def find_empty(board, pos):
    for key in board.keys():
        if board[key] == 0:
            pos.append(str(key)[0])
            pos.append(str(key)[1])
            return True
    return False

# This function goes through the validity of the rows, columns and squares to
# check if the the numbers only appear once in each


def isValid(board, empty, num):

    # Check each row for duplicate number
    row_pos = []
    for i in range(1, 10):
        row_pos.append(empty[0] + str(i))
    for key in row_pos:
        if board[key] == num:
            return False

    # Check each column for duplicate number
    col_pos = []
    for i in list(ROW):
        col_pos.append(str(i) + str(empty[1]))
    for key in col_pos:
        if board[key] == num:
            return False

    # Check each square for duplicate number
    column = int(empty[1]) - 1
    col_index = int(column) - (int(column) % 3)
    columns_to_check = [col_index + 1,
                        col_index + 2, col_index + 3]

    row_index = list(ROW).index(empty[0])
    row_index = row_index - row_index % 3
    rows_to_check = [list(ROW)[row_index], list(ROW)[row_index + 1],
                     list(ROW)[row_index + 2]]

    for r in rows_to_check:
        for c in columns_to_check:
            if board[r + str(c)] == num:
                return False
    return True

# Method to check an empty space apply a number and continue but if
# an error appears it will keep going back until something applies


def backtracking(board):
    """Takes a board and returns solved board."""
    e = []
    find = find_empty(board, e)
    if find is False:
        return True

    for i in range(1, 10):
        if isValid(board, e, i):
            board["".join(e)] = i

            if backtracking(board):
                board_solved = board
                return board_solved

            board["".join(e)] = 0
    return False


if __name__ == '__main__':
    #  Read boards from source.
    src_filename = 'sudoku_boards.txt'

    try:
        srcfile = open(src_filename, "r")
        sudoku_list = srcfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")

    # count is the number of boards that it parsed throw
    count = 1
    # this is the timing for the entire function to return the seconds it takes to run the
    start = time.time()
    # Solve each board using backtracking
    for line in sudoku_list.split("\n"):
        print("---------------------")
        print("Solving Board:", count)

        if len(line) < 9:
            continue

        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(line[9*r+c])
                 for r in range(9) for c in range(9)}

        # Print starting board. TODO: Comment this out when timing runs.
        # print_board(board)

        internal_start = time.time()
        # Solve with backtracking
        solved_board = backtracking(board)

        internal_finish = time.time() - internal_start
        i_format = "{:.2f}".format(internal_finish)
        print("Time: ", i_format, "seconds")

        # Print solved board. TODO: Comment this out when timing runs.
        # print_board(solved_board)

        # Write board to file
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')
        count = count + 1
    finish = time.time()-start
    format = "{:.2f}".format(finish)
    print("---------------------")
    print("Finished solving", count, "boards in",
          format, "seconds\n", "Check output file for solved boards")
