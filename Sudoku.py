# imports
import argparse
import pandas as pd
from prettytable import PrettyTable
from rich import print
from rich.console import Console
import sys
from tabulate import tabulate


console = Console()

square_index = [
    [1, 2, 3, 10, 11, 12, 19, 20, 21],
    [4, 5, 6, 13, 14, 15, 22, 23, 24],
    [7, 8, 9, 16, 17, 18, 25, 26, 27],
    [28, 29, 30, 37, 38, 39, 46, 47, 48],
    [31, 32, 33, 40, 41, 42, 49, 50, 51],
    [34, 35, 36, 43, 44, 45, 52, 53, 54],
    [55, 56, 57, 64, 65, 66, 73, 74, 75],
    [58, 59, 60, 67, 68, 69, 76, 77, 78],
    [61,62, 63, 70, 71, 72, 79, 80 ,81]
]


def print_sudoku(puzzle):
    # Convert the puzzle string into a 9x9 list of lists
    grid = [list(puzzle[i*9:(i+1)*9]) for i in range(9)]
    # Replace '0' with '.' for empty cells (optional)
    grid = [['.' if c == '0' else c for c in row] for row in grid]
    # insert a separator row after every third row
    sep = [' ' for _ in range(9)]
    display_grid = []
    for i, row in enumerate(grid):
        row.insert(6, " ")
        row.insert(3, " ")
        display_grid.append(row)
        if i in [2, 5]:
            display_grid.append(sep)
    print(tabulate(display_grid, tablefmt="plain"))
    return


def CreateRows(puzzle):
    return [puzzle[i * 9 : (i + 1) * 9] for i in range(9)]


def CreateColumns(row_list):
    return [''.join([row[i] for row in row_list]) for i in range(9)]


def CreateSquares(puzzle):
    return [''.join([puzzle[i - 1] for i in square]) for square in square_index]


def Non_Zero_Count(segment):
    return sum(1 for c in segment if c != "0")


def No_Duplicates(segment):
    return len(set([c for c in segment if c != "0"]))


def FaultCheck(puzzle):
    # FaultCheck checks for duplicates in rows, columns, and squares
    row_list = CreateRows(puzzle)
    column_list = CreateColumns(row_list)
    square_list = CreateSquares(puzzle)
    for segment in row_list + column_list + square_list:
        if Non_Zero_Count(segment) != No_Duplicates(segment):
            return False
    return True


def PhaseZero(puzzle):
    # Phase Zero checks if the puzzle is complete
    if Non_Zero_Count(puzzle) < 81:
        return False
    else:
        return True


def PhaseOne(puzzle):
    # Phase One looks for row / column / square exactly length eight

    # create a list of rows
    row_list = CreateRows(puzzle)
    # Check each row in row_list for a non-zero_count of eight
    for ndx, each_row in enumerate(row_list):
        if Non_Zero_Count(each_row) == 8:
            # determine index of zero value
            zero_index = each_row.index("0")
            # determine missing value
            missing_value = str((set("123456789") - set(each_row)).pop())
            # print what is being changed
            s = f"\t[dim]1: last value of {missing_value} for row {ndx + 1} at column {zero_index + 1}[/]"
            console.print(s.expandtabs(tabsize=1), highlight = False)
            # replace the missing value in puzzle
            puzzle = puzzle[: ndx * 9 + zero_index] + missing_value + puzzle[ndx * 9 + zero_index + 1 :]
            return puzzle, True
    
    # create a list of columns
    column_list = CreateColumns(row_list)
    # check each column in column_list for a non-zero count of eight
    for ndx, each_column in enumerate(column_list):
        if Non_Zero_Count(each_column) == 8:
            # determine index of zero value
            zero_index = each_column.index("0")
            # determine missing value
            missing_value = str((set("123456789") - set(each_column)).pop())
            # print what is being changed
            s = f"\t[dim]1: last value of {missing_value} for column {ndx + 1} at row {zero_index + 1}[/]"
            console.print(s.expandtabs(tabsize=1), highlight = False)
            # replace the missing value in puzzle
            puzzle = puzzle[: zero_index * 9 + ndx] + missing_value + puzzle[zero_index * 9 + ndx + 1 :]
            return puzzle, True

    # create a list of squares
    square_list = CreateSquares(puzzle)
    # check each square in square_list for a non-zero count of eight
    for ndx, each_square in enumerate(square_list):
        if Non_Zero_Count(each_square) == 8:
            # determine index of zero value
            zero_index = each_square.index("0")
            # determine missing value
            missing_value = str((set("123456789") - set(each_square)).pop())
            # print what is being changed
            location_index = square_index[ndx][zero_index]
            row = int(location_index / 9)
            column = location_index % 9
            # print what is being changed
            s = f"\t[dim]1: last value of {missing_value} for square {ndx+1} at row {row + 1} and column {column}[/]"
            console.print(s.expandtabs(tabsize=1), highlight = False)
            # replace the missing value in puzzle
            puzzle = puzzle[: row * 9 + column - 1] + missing_value + puzzle[row * 9 + column :]
            return puzzle, True
    return puzzle, False


def PhaseTwo(puzzle):
    # Phase Two is finding the lone numbers
    # check for the presence of a number twice in a row / column / square triplet
    # look for the potential of that number to fill a single cell in the third triplet
    # follow along at row 698 in SudokuSolver.txt

    # create a list of rows, columns, and squares
    row_list = CreateRows(puzzle)
    column_list = CreateColumns(row_list)
    square_list = CreateSquares(puzzle)

    # check row triplets
    for i in range(0, 9, 3):
        for test_val in "123456789":
            # create triplets as a list of three items
            triplet = [test_val in row_list[i + k] for k in range(3)]
            # over test to validate exactly two triplets contain test_val
            if triplet.count(True) == 2 and triplet.count(False) == 1:
                target_row = i + triplet.index(False)
                candidates = []
                for col in range(9):
                    if row_list[target_row][col] == "0" and test_val not in column_list[col]:
                        sq = (target_row // 3) * 3 + (col // 3)
                        if test_val not in square_list[sq]:
                            candidates.append((target_row, col))
                if len(candidates) == 1:
                    r, c = candidates[0]
                    # replace the zero with test_val in the puzzle string
                    puzzle = puzzle[: r * 9 + c] + test_val + puzzle[r * 9 + c + 1 :]
                    # print what is being changed
                    s = f"\t[dim]2: value {test_val} placed in row {r + 1} and column {c + 1}[/]"
                    console.print(s.expandtabs(tabsize=2), highlight = False)
                    return puzzle, True
    # check column triplets
    for i in range(0, 9, 3):
        for test_val in "123456789":
            # create triplets as a list of three items
            triplet = [test_val in column_list[i + k] for k in range(3)]
            # over test to validate exactly two triplets contain test_val
            if triplet.count(True) == 2 and triplet.count(False) == 1:
                target_col = i + triplet.index(False)
                candidates = []
                for row in range(9):
                    if row_list[row][target_col] == "0" and test_val not in row_list[row]:
                        sq = (row // 3) * 3 + (target_col // 3)
                        if test_val not in square_list[sq]:
                            candidates.append((row, target_col))
                if len(candidates) == 1:
                    r, c = candidates[0]
                    puzzle = puzzle[: r * 9 + c] + test_val + puzzle[r * 9 + c + 1 :]
                    # print what is being changed
                    s = f"\t[dim]2: value {test_val} placed in column {c + 1} at row {r + 1}[/]"
                    console.print(s.expandtabs(tabsize=2), highlight = False)
                    return puzzle, True
    return puzzle, False


def PhaseThree(puzzle):
    """
    This phase will look for subsets of length seven.
    The remaining pairs of numbers will be examined relative to rows and columns.
    Returns (puzzle, True) if a placement was made, else (puzzle, False).
    """
    row_list = CreateRows(puzzle)
    column_list = CreateColumns(row_list)
    square_list = CreateSquares(puzzle)

    # --- Check for rows of length 7 ---
    for i, row in enumerate(row_list):
        if Non_Zero_Count(row) == 7:
            potentials = [str(n) for n in range(1, 10) if str(n) not in row]
            if len(potentials) != 2:
                continue
            first_val, second_val = potentials
            for j in range(9):
                if row[j] == "0":
                    col = column_list[j]
                    if (first_val not in col) and (second_val in col):
                        idx = i * 9 + j
                        puzzle = puzzle[:idx] + first_val + puzzle[idx+1:]
                        s = f"\t[dim]3: value {first_val} placed in row {i+1} at column {j+1}[/]"
                        console.print(s.expandtabs(tabsize=3), highlight = False)
                        return puzzle, True
                    elif (first_val in col) and (second_val not in col):
                        idx = i * 9 + j
                        puzzle = puzzle[:idx] + second_val + puzzle[idx+1:]
                        s = f"\t[dim]3: value {second_val} placed in row {i+1} at column {j+1}[/]"
                        console.print(s.expandtabs(tabsize=3), highlight=False)
                        return puzzle, True

    # --- Check for columns of length 7 ---
    for j, col in enumerate(column_list):
        if Non_Zero_Count(col) == 7:
            potentials = [str(n) for n in range(1, 10) if str(n) not in col]
            if len(potentials) != 2:
                continue
            first_val, second_val = potentials
            for i in range(9):
                if row_list[i][j] == "0":
                    row = row_list[i]
                    if (first_val not in row) and (second_val in row):
                        idx = i * 9 + j
                        puzzle = puzzle[:idx] + first_val + puzzle[idx+1:]
                        s = f"\t[dim]3: value {first_val} placed at row {i+1} and column {j+1}[/]"
                        console.print(s.expandtabs(tabsize=3), highlight=False)
                        return puzzle, True
                    elif (first_val in row) and (second_val not in row):
                        idx = i * 9 + j
                        puzzle = puzzle[:idx] + second_val + puzzle[idx+1:]
                        s = f"\t[dim]3: value {second_val} placed at row {i+1} and column {j+1}[/]"
                        console.print(s.expandtabs(tabsize=3), highlight=False)
                        return puzzle, True

    # --- Check for squares of length 7 ---
    for sq_idx, square in enumerate(square_list):
        if Non_Zero_Count(square) == 7:
            potentials = [str(n) for n in range(1, 10) if str(n) not in square]
            if len(potentials) != 2:
                continue
            first_val, second_val = potentials
            for cell_in_sq, val in enumerate(square):
                if val == "0":
                    idx = square_index[sq_idx][cell_in_sq] - 1
                    i, j = divmod(idx, 9)
                    row = row_list[i]
                    col = column_list[j]
                    if (first_val in row) or (first_val in col):
                        puzzle = puzzle[:idx] + second_val + puzzle[idx+1:]
                        s = f"\t[dim]3: Value {second_val} placed at row {i+1}, column {j+1}[/]"
                        console.print(s.expandtabs(tabsize=3), highlight=False)
                        return puzzle, True
                    elif (second_val in row) or (second_val in col):
                        puzzle = puzzle[:idx] + first_val + puzzle[idx+1:]
                        s = f"[dim]\t3: Value {first_val} placed in square {sq_idx} at row {i+1} and column {j+1}[/]"
                        console.print(s.expandtabs(tabsize=3), highlight=False)
                        return puzzle, True

    return puzzle, False


def PhaseFour(puzzle):
    """
    Phase Four looks for subsets of length 5 or 6 in rows, columns, and for hidden singles in squares of length 6.
    Returns (puzzle, True) if a placement was made, else (puzzle, False).
    """
    row_list = CreateRows(puzzle)
    column_list = CreateColumns(row_list)
    square_list = CreateSquares(puzzle)

    # --- Rows of length 5 or 6 ---
    for i, row in enumerate(row_list):
        if Non_Zero_Count(row) in (5, 6):
            potentials = [str(n) for n in range(1, 10) if str(n) not in row]
            for j in range(9):
                if row[j] == "0":
                    cross_potentials = []
                    for val in potentials:
                        sq = (i // 3) * 3 + (j // 3)
                        if (val not in column_list[j]) and (val not in square_list[sq]):
                            cross_potentials.append(val)
                    if len(cross_potentials) == 1:
                        idx = i * 9 + j
                        puzzle = puzzle[:idx] + cross_potentials[0] + puzzle[idx+1:]
                        s = f"\t[dim]4: value {cross_potentials[0]} placed at row {i+1} and column {j+1}[/]"
                        console.print(s.expandtabs(tabsize=4), highlight=False)
                        return puzzle, True

    # --- Columns of length 5 or 6 ---
    for j, col in enumerate(column_list):
        if Non_Zero_Count(col) in (5, 6):
            potentials = [str(n) for n in range(1, 10) if str(n) not in col]
            for i in range(9):
                if row_list[i][j] == "0":
                    cross_potentials = []
                    for val in potentials:
                        sq = (i // 3) * 3 + (j // 3)
                        if (val not in row_list[i]) and (val not in square_list[sq]):
                            cross_potentials.append(val)
                    if len(cross_potentials) == 1:
                        idx = i * 9 + j
                        puzzle = puzzle[:idx] + cross_potentials[0] + puzzle[idx+1:]
                        s = f"[dim]\t4: Value {cross_potentials[0]} placed at row {i+1}, column {j+1}[/]"
                        console.print(s.expandtabs(tabsize=4), highlight=False)
                        return puzzle, True

    # --- Squares of length 6: hidden singles ---
    for sq_idx, square in enumerate(square_list):
        if Non_Zero_Count(square) == 6:
            # For each number 1-9, count possible placements in this square
            for k in range(1, 10):
                val = str(k)
                if val in square:
                    continue
                count = 0
                last_pos = None
                for cell_in_sq, cell_val in enumerate(square):
                    if cell_val == "0":
                        idx = square_index[sq_idx][cell_in_sq] - 1
                        i, j = divmod(idx, 9)
                        if (val not in row_list[i]) and (val not in column_list[j]):
                            count += 1
                            last_pos = (i, j, idx)
                if count == 1 and last_pos:
                    i, j, idx = last_pos
                    puzzle = puzzle[:idx] + val + puzzle[idx+1:]
                    s = f"\t[dim]4: Value {val} placed at row {i+1} and column {j+1}[/]"
                    console.print(s.expandtabs(tabsize=4), highlight=False)
                    return puzzle, True

    return puzzle, False


def PhaseFive(puzzle):
    """
    Converted from VBA PhaseFive:
    - Look for 3x3 squares that have 4 filled cells.
    - If one row inside the square is completely filled and another is empty,
      iterate the digits present in the empty row (outside the square) that are
      also missing from the square (potentials). For each such digit, check the
      two other rows in the square for a single viable column (cell empty and
      column doesn't contain the digit). If exactly one candidate cell exists,
      place the digit and return (puzzle, True).
    """
    row_list = CreateRows(puzzle)
    column_list = CreateColumns(row_list)
    square_list = CreateSquares(puzzle)

    for sx in range(3):
        for sy in range(3):
            sq_idx = sx * 3 + sy
            # square_list element may contain '0' for blanks; consider only filled digits
            square_filled = ''.join(ch for ch in square_list[sq_idx] if ch != '0')
            if len(square_filled) == 4:
                # potentials = digits missing from the square
                potentials = [d for d in "123456789" if d not in square_filled]

                # Count filled cells in each of the 3 rows within this square
                cell_counts = []
                for i in range(3):
                    row_idx = sx * 3 + i
                    count = sum(1 for c in range(sy * 3, sy * 3 + 3) if row_list[row_idx][c] != "0")
                    cell_counts.append(count)

                # If one row is full (3) and another is empty (0), run checks
                if 3 in cell_counts:
                    for i, cnt in enumerate(cell_counts):
                        if cnt == 0:
                            empty_row_idx = sx * 3 + i
                            # iterate digits present in that row (exclude '0')
                            present_digits = [ch for ch in row_list[empty_row_idx] if ch != "0"]
                            for digit in present_digits:
                                if digit in potentials:
                                    # check the other two rows in this square
                                    for offset in (1, 2):
                                        test_row_local = (i + offset) % 3  # 0..2 within square
                                        test_row_idx = sx * 3 + test_row_local
                                        testcells = []
                                        for l in range(3):
                                            col_idx = sy * 3 + l
                                            cell_empty = (row_list[test_row_idx][col_idx] == "0")
                                            col_ok = (digit not in column_list[col_idx])
                                            testcells.append(1 if (cell_empty and col_ok) else 0)
                                        if sum(testcells) == 1:
                                            # find which column within square is the candidate
                                            l = testcells.index(1)
                                            col_idx = sy * 3 + l
                                            idx = test_row_idx * 9 + col_idx
                                            puzzle = puzzle[:idx] + digit + puzzle[idx + 1 :]
                                            s = f"[dim]\t5: value {digit} placed in row {test_row_idx+1} and col {col_idx+1}[/]"
                                            console.print(s.expandtabs(tabsize=5), highlight=False)
                                            return puzzle, True
    return puzzle, False


def PhaseSix(puzzle):
    """
    Phase Six: For squares of length five, find missing numbers.
    If a crossing row and column make one of the numbers fit in a single cell, fill it.
    Also checks columns of length six for unique placements.
    Returns the updated puzzle string and True if a cell was filled, else False.
    """
    row_list = CreateRows(puzzle)
    column_list = CreateColumns(row_list)
    square_list = CreateSquares(puzzle)
    puzzle_changed = False

    # --- Check squares of length 5 ---
    for sq_idx, square in enumerate(square_list):
        if len(square.replace('0', '')) == 5:
            # Find missing numbers
            potentials = [str(n) for n in range(1, 10) if str(n) not in square]
            # Find empty cells in the square
            x = sq_idx // 3
            y = sq_idx % 3
            cell_counts = [0] * len(potentials)
            empty_cells = []
            for i in range(3):
                for j in range(3):
                    row = x * 3 + i
                    col = y * 3 + j
                    idx = row * 9 + col
                    if puzzle[idx] == '0':
                        empty_cells.append((row, col))
                        for k, num in enumerate(potentials):
                            if num not in row_list[row] and num not in column_list[col]:
                                cell_counts[k] += 1
            # If any potential can only go in one cell, place it
            for k, count in enumerate(cell_counts):
                if count == 1:
                    num = potentials[k]
                    for row, col in empty_cells:
                        if num not in row_list[row] and num not in column_list[col]:
                            idx = row * 9 + col
                            puzzle = puzzle[:idx] + num + puzzle[idx + 1:]
                            console.print(f"[dim]Phase 6: Value {num} placed at row {row+1} and col {col+1}[/]", highlight=False)
                            return puzzle, True

    # --- Check columns of length 6 ---
    for col_idx, col in enumerate(column_list):
        if len(col.replace('0', '')) == 6:
            potentials = [str(n) for n in range(1, 10) if str(n) not in col]
            cell_counts = [0] * len(potentials)
            empty_cells = []
            for row in range(9):
                idx = row * 9 + col_idx
                if puzzle[idx] == '0':
                    empty_cells.append(row)
                    for k, num in enumerate(potentials):
                        if num not in row_list[row]:
                            cell_counts[k] += 1
            for k, count in enumerate(cell_counts):
                if count == 1:
                    num = potentials[k]
                    for row in empty_cells:
                        if num not in row_list[row]:
                            idx = row * 9 + col_idx
                            puzzle = puzzle[:idx] + num + puzzle[idx + 1:]
                            s = f"\t[dim]6: Value {num} placed at row {row+1} and col {col_idx+1}[/dim]"
                            console.print(s.expandtabs(tabsize=6), highlight=False)
                            return puzzle, True

    return puzzle, False


def CellCandidates(puzzle):
    """
    Returns a list of sets, where each set contains the possible candidates for each cell in the puzzle.
    Each cell is represented by its index in the puzzle string.
    """
    all_numbers = "123456789"
    row_list = CreateRows(puzzle)
    column_list = CreateColumns(row_list)
    square_list = CreateSquares(puzzle)
    candidates = [[list() for _ in range(9)] for _ in range(9)]

    for x in range(9):
        for y in range(9):
            if row_list[x][y] == "0":
                possible = set(all_numbers)
                possible -= set(row_list[x])
                possible -= set(column_list[y])
                possible -= set(square_list[(x // 3) * 3 + (y // 3)])
                candidates[x][y] = list(possible)

    return candidates


def PhaseSeven(puzzle):
    """
    Fills in cells where only one possible value can go,
    and checks for unique candidates in columns, rows, and squares.
    Returns the updated puzzle string and True if a cell was filled, else False.
    """
    all_numbers = "123456789"
    row_list = CreateRows(puzzle)
    column_list = CreateColumns(row_list)
    square_list = CreateSquares(puzzle)
    candidates = [[set() for _ in range(9)] for _ in range(9)]
    changed = False

    # Step 1: Find all candidates for each empty cell
    for x in range(9):
        for y in range(9):
            if row_list[x][y] == "0":
                possible = set(all_numbers)
                possible -= set(row_list[x])
                possible -= set(column_list[y])
                possible -= set(square_list[(x // 3) * 3 + (y // 3)])
                candidates[x][y] = possible

    # Step 2: Fill cells with only one candidate
    for x in range(9):
        for y in range(9):
            if row_list[x][y] == "0" and len(candidates[x][y]) == 1:
                val = candidates[x][y].pop()
                idx = x * 9 + y
                puzzle = puzzle[:idx] + val + puzzle[idx + 1:]
                s = f"\t[dim]NothingLeft: Placed {val} at row {x+1} and col {y+1}[/]"
                console.print(s.expandtabs(tabsize=7), highlight = False)
                return puzzle, True

    # Step 3: Unique candidate in a column
    for y in range(9):
        col_candidates = [candidates[x][y] for x in range(9)]
        flat = [num for cell in col_candidates for num in cell]
        for num in all_numbers:
            if flat.count(num) == 1:
                for x in range(9):
                    if num in candidates[x][y]:
                        idx = x * 9 + y
                        puzzle = puzzle[:idx] + num + puzzle[idx + 1:]
                        s = f"\t[dim]7: unique {num} in column {y+1} at row {x+1}[/dim]"
                        console.print(s.expandtabs(tabsize=7), highlight = False)
                        return puzzle, True

    # Step 4: Unique candidate in a row
    for x in range(9):
        row_candidates = candidates[x]
        flat = [num for cell in row_candidates for num in cell]
        for num in all_numbers:
            if flat.count(num) == 1:
                for y in range(9):
                    if num in candidates[x][y]:
                        idx = x * 9 + y
                        puzzle = puzzle[:idx] + num + puzzle[idx + 1:]
                        s = f"\t[dim]7: Unique {num} in row {x+1} at col {y+1}[/dim]"
                        console.print(s.expandtabs(tabsize=7), highlight = False)
                        return puzzle, True

    # Step 5: Unique candidate in a square
    for sq in range(9):
        sx, sy = (sq // 3) * 3, (sq % 3) * 3
        square_candidates = [candidates[x][y] for x in range(sx, sx+3) for y in range(sy, sy+3)]
        flat = [num for cell in square_candidates for num in cell]
        for num in all_numbers:
            if flat.count(num) == 1:
                for dx in range(3):
                    for dy in range(3):
                        x, y = sx + dx, sy + dy
                        if num in candidates[x][y]:
                            idx = x * 9 + y
                            puzzle = puzzle[:idx] + num + puzzle[idx + 1:]
                            s = f"\t[dim]NothingLeft: Unique {num} in square {sq+1} at row {x+1}, col {y+1}"
                            console.print(s.expandtabs(tabsize=7), highlight = False)
                            return puzzle, True

    return puzzle, False


def Transpose(rc_list):
    return [[rc_item[i] for rc_item in rc_list] for i in range(9)]


def PhaseEight(puzzle):
    # Placeholder for Phase Eight implementation
    # Phase Eight uses the cell candidates to look for pairs in rows or columns
    candidates = CellCandidates(puzzle)
    # candidates is in row form
    column_candidates = Transpose(candidates)
    candidate_change = True
    puzzle_change = False
    pair_ndx = None

    def SingleValueColumn(puzzle):
        idx = row_index * 9 + col_index
        val = column_candidates[col_index][row_index].pop()
        puzzle = puzzle[:idx] + val + puzzle[idx + 1:]
        s = f"\t[dim]8: value {val} placed at row {row_index+1} and column {col_index+1}[/]"
        console.print(s.expandtabs(tabsize=8), highlight=False)
        return puzzle
    
    def SingleValueRow(puzzle):
        idx = row_index * 9 + col_index
        val = row_candidates[row_index][col_index].pop()
        puzzle = puzzle[:idx] + val + puzzle[idx + 1:]
        s = f"\t[dim]8: value {val} placed at row {row_index+1} and column {col_index+1}[/]"
        console.print(s.expandtabs(tabsize=8), highlight=False)
        return puzzle
        
    while candidate_change == True:
        candidate_change = False
        # look for pairs in columns
        for n,col in enumerate(column_candidates):
            two_candidates = [x for x in col if len(x) == 2]
            # find identical iteams in two_candidates
            pair = [x for x in two_candidates if two_candidates.count(x) == 2]
            # print(f'{two_candidates=}')
            # print(f"{pair=}")
            # find the unique values in candidates
            if pair != []:
                if len(pair) == 2:
                    unique_candidates = [pair[0]]
                else:
                    # unique_candidates = []
                    # for c in col:
                    #     if len(c) == 2:
                    #         if c not in unique_candidates:
                    #             unique_candidates.append(c)
                    unique_candidates = [x for x in two_candidates if two_candidates.count(x) == 1 and len(x)==2]
                # print(f'{unique_candidates=}')
                for uc in unique_candidates:
                    pair_ndx = [[n,i] for i, x in enumerate(col) if x == uc]
                    # print(f'{pair_ndx=}')
                    # for each item in pair[0], drop it from each item in col
                    for val in pair[0]:
                        # print(f"Length of col is {len(col)}")
                        # print(f"{val=}")
                        for i in range(len(col)):
                            # print(f"{i=}")
                            if col[i] != pair[0]:
                                if val in col[i]:
                                    col[i].remove(val)
                                    candidate_change = True
                                    column_candidates[n] = col
                                    if len(col[i])==1:
                                        puzzle_change = True
                                        row_index = i
                                        col_index = n
                                        # print(f"c{n}:{col_index}")
                    # print(f'{candidate_change=}')
                    # if candidate_change:
                    #     break
                    # Need to test if any candidate cell holds a single value
                    # print(f'{puzzle_change=}')
                    if puzzle_change:
                        puzzle = SingleValueColumn(puzzle)
                        return puzzle, True
                    # candidate_change = False
                    # look for pairs in the same square
                    # print(f'{pair_ndx=}')
                    if pair_ndx is not None and isinstance(pair_ndx, list) and len(pair_ndx)==2:
                        # print(f'{pair_ndx=}')
                        if pair_ndx[0][1]//3 == pair_ndx[1][1]//3:
                            square_row = pair_ndx[0][1]//3
                            square_col = pair_ndx[0][0]//3
                            # print(f"Square found at {square_row},{square_col}")
                            # now drop the values from other items in the square
                            for i in range(square_row*3, square_row*3+3):
                                for j in range(square_col*3, square_col*3+3):
                                    if [j,i] != pair_ndx[0] and [j,i] != pair_ndx[1]:
                                        for val in pair[0]:
                                            # print(f'{column_candidates[j][i]=}')
                                            if val in column_candidates[j][i]:
                                                column_candidates[j][i].remove(val)
                                                candidate_change = True
                                                if len(column_candidates[j][i])==1:
                                                    puzzle_change = True
                                                    row_index = i
                                                    col_index = j
                                                    # print(f"cell {i},{j}:{column_candidates[j][i]}")
                                    # if candidate_change:
                                    #     break
                                    # Need to test if any candidate cell holds a single value
                                    if puzzle_change:
                                        puzzle = SingleValueColumn(puzzle)
                                        return puzzle, True
                                        # loop
        # look for pairs in rows
        row_candidates = Transpose(column_candidates)
        for n,row in enumerate(row_candidates):
            two_candidates = [x for x in row if len(x) == 2]
            # find identical iteams in two_candidates
            pair = [x for x in two_candidates if two_candidates.count(x) == 2]
            # print(f'{two_candidates=}')
            # print(f"{pair=}")
            # find the unique values in candidates
            if pair != []:
                if len(pair) == 2:
                    unique_candidates = [pair[0]]
                else:
                    # unique_candidates = []
                    # for c in col:
                    #     if len(c) == 2:
                    #         if c not in unique_candidates:
                    #             unique_candidates.append(c)
                    unique_candidates = [x for x in two_candidates if two_candidates.count(x) == 1 and len(x)==2]
                # print(f'{unique_candidates=}')
                for uc in unique_candidates:
                    pair_ndx = [[n,i] for i, x in enumerate(row) if x == uc]
                    # print(f'{pair_ndx=}')
                    # for each item in pair[0], drop it from each item in col
                    for val in pair[0]:
                        # print(f"Length of col is {len(col)}")
                        # print(f"{val=}")
                        for i in range(len(row)):
                            # print(f"{i=}")
                            if row[i] != pair[0]:
                                if val in row[i]:
                                    row[i].remove(val)
                                    candidate_change = True
                                    row_candidates[n] = row
                                    if len(row[i])==1:
                                        puzzle_change = True
                                        row_index = n
                                        col_index = i
                                        # print(f"r{n}:{col_index}")
                    # print(f'{candidate_change=}')
                    # if candidate_change:
                    #     break
                    # Need to test if any candidate cell holds a single value
                    # print(f'{puzzle_change=}')
                    if puzzle_change:
                        # print(f'{row_candidates=}')
                        puzzle = SingleValueRow(puzzle)
                        return puzzle, True
                    # candidate_change = False
                    # look for pairs in the same square
                    # print(f'{pair_ndx=}')
                    if pair_ndx is not None and isinstance(pair_ndx, list) and len(pair_ndx)==2:
                        # print(f'{pair_ndx=}')
                        if pair_ndx[0][0]//3 == pair_ndx[1][0]//3:
                            square_row = pair_ndx[0][1]//3
                            square_col = pair_ndx[0][0]//3
                            # print(f"Square found at {square_row},{square_col}")
                            # now drop the values from other items in the square
                            for i in range(square_row*3, square_row*3+3):
                                for j in range(square_col*3, square_col*3+3):
                                    if [j,i] != pair_ndx[0] and [j,i] != pair_ndx[1]:
                                        for val in pair[0]:
                                            # print(f'{row_candidates[j][i]=}')
                                            if val in row_candidates[j][i]:
                                                row_candidates[j][i].remove(val)
                                                candidate_change = True
                                                if len(row_candidates[j][i])==1:
                                                    puzzle_change = True
                                                    row_index = j
                                                    col_index = i
                                                    # print(f"cell {i},{j}:{column_candidates[j][i]}")
                                    # if candidate_change:
                                    #     break
                                    # Need to test if any candidate cell holds a single value
                                    if puzzle_change:
                                        puzzle = SingleValueRow(puzzle)
                                        return puzzle, True
                                        # loop
    return puzzle, False


def Completed(puzzle, args):
    # check for completeness
    puzzle_solved = PhaseZero(puzzle)
    if puzzle_solved == True:
        console.rule("[bold green]Conclusion")
        console.print(f"[green reverse]Puzzle {args.book}-{args.puzzle} solved![/]", highlight=False)
        print_sudoku(puzzle)
        if 'Double' in args.book:
            with open("data/output/DoubleSudoku202512.csv", "a") as f:
                f.write(f"{args.puzzle},Solved\n")
        sys.exit(0)
    return


def main(args):
    if args.function == "add":   # add a puzzle that isn't solved to the data/output/Puzzle.csv file
        with open("data/output/Puzzle.csv", "a") as f:
            f.write(f"Dell{args.book},{args.puzzle}\n")
        console.print(f"[green]Puzzle Dell{args.book}-{args.puzzle} added to data/output/Puzzle.csv[/]", highlight=False)
    elif args.function == "delete":  # delete a puzzle from the data/output/Puzzle.csv file
        df = pd.read_csv("data/output/Puzzle.csv")
        # print(df.dtypes, flush = True)
        pre_cut = df.shape[0]
        df = df[~((df["Book"] == f"Dell{args.book}") & (df["Puzzle"] == int(f"{args.puzzle}")))]
        post_cut = df.shape[0]
        df.to_csv("data/output/Puzzle.csv", index = False)
        if pre_cut == post_cut:
            console.print(f"[bold red]Puzzle Dell{args.book}-{args.puzzle} not found in data/output/Puzzle.csv[/]", highlight=False)
        else:
            console.print(f"[green]Puzzle Dell{args.book}-{args.puzzle} deleted from data/output/Puzzle.csv[/]", highlight=False)
    elif args.function == "solve":
        # Load the dataset
        if 'Double' in args.book:
            df = pd.read_csv("../../Puzzles/" + args.book + ".csv")
            print(df.head())
        else:
            df = pd.read_csv("../../Puzzles/Dell" + args.book + ".csv")

        # print the number of puzzles -- this is shape[0]
        console.rule("[bold blue]Foundation")
        console.print(f"There are {df.shape[0]:.0f} puzzles in Dell{args.book}", highlight=False)

        # set the puzzle variable
        if 'Double' in args.book:
            source = int(args.puzzle)
        else:
            source = "Dell" + args.book + "-" + args.puzzle
        puzzle = df[df["Source"] == source]["Puzzle"].iloc[0]
        print_sudoku(puzzle)
        console.print(f"[bold]Puzzle {args.puzzle} has {81 - Non_Zero_Count(puzzle)} zero cells[/]", highlight=False)
        console.rule("[bold blue]Execution")
        puzzle_solved = False
        while puzzle_solved == False:
            Completed(puzzle, args)
            # find any RCS that is exactly 8 in non-zero length
            puzzle_step = False
            puzzle, puzzle_step = PhaseOne(puzzle)
            if puzzle_step == True:
                if FaultCheck(puzzle) == False:
                    console.print(f"[bold red]Fault detected after Phase One on Dell {args.book}-{args.puzzle}[/]", highlight=False)
                    print_sudoku(puzzle)
                    break
            Completed(puzzle, args)
            if puzzle_step == False:
                puzzle, puzzle_step = PhaseTwo(puzzle)
                if puzzle_step == True:
                    if FaultCheck(puzzle) == False:
                        console.print(f"[bold red]Fault detected after Phase Two on Dell {args.book}-{args.puzzle}[/]", highlight=False)
                        print_sudoku(puzzle)
                        break
            Completed(puzzle, args)
            if puzzle_step == False:
                puzzle, puzzle_step = PhaseThree(puzzle)
                if puzzle_step == True:
                    if FaultCheck(puzzle) == False:
                        console.print(f"[bold red]Fault detected after Phase Three on Dell {args.book}-{args.puzzle}[/]", highlight=False)
                        print_sudoku(puzzle)
                        break
            Completed(puzzle, args)
            if puzzle_step == False:
                puzzle, puzzle_step = PhaseFour(puzzle)
                if puzzle_step == True:
                    if FaultCheck(puzzle) == False:
                        console.print(f"[bold red]Fault detected after Phase Four on Dell {args.book}-{args.puzzle}[/]", highlight=False)
                        print_sudoku(puzzle)
                        break
            Completed(puzzle, args)
            if puzzle_step == False:
                puzzle, puzzle_step = PhaseFive(puzzle)
                if puzzle_step == True:
                    if FaultCheck(puzzle) == False:
                        console.print(f"[bold red]Fault detected after Phase Five on Dell {args.book}-{args.puzzle}[/]", highlight=False)
                        print_sudoku(puzzle)
                        break
            Completed(puzzle, args)
            if puzzle_step == False:
                puzzle, puzzle_step = PhaseSix(puzzle)
                if puzzle_step == True:
                    if FaultCheck(puzzle) == False:
                        console.print(f"[bold red]Fault detected after Phase Six on Dell {args.book}-{args.puzzle}[/]", highlight=False)
                        print_sudoku(puzzle)
                        break
            Completed(puzzle, args)
            if puzzle_step == False:
                puzzle, puzzle_step = PhaseSeven(puzzle)
                if puzzle_step == True:
                    if FaultCheck(puzzle) == False:
                        console.print(f"[bold red]Fault detected after Phase Seven on Dell {args.book}-{args.puzzle}[/]", highlight=False)
                        print_sudoku(puzzle)
                        break
            Completed(puzzle, args)
            if puzzle_step == False:
                puzzle, puzzle_step = PhaseEight(puzzle)
                if puzzle_step == True:
                    if FaultCheck(puzzle) == False:
                        console.print(f"[bold red]Fault detected after Phase Eight on Dell {args.book}-{args.puzzle}[/]", highlight=False)
                        print_sudoku(puzzle)
                        break
            Completed(puzzle, args)
            if puzzle_step == False:
                console.rule("[bold red]Conclusion[/bold red]")
                console.print(f"[red reverse]Nothing else to do on Dell {args.book}-{args.puzzle}[/red reverse]", highlight=False)
                print_sudoku(puzzle)
                if 'Double' in args.book:
                    with open("data/output/DoubleSudoku202512.csv", "a") as f:
                        f.write(f"{args.puzzle},Unsolved\n")
                candidates = CellCandidates(puzzle)
                console.print("\t[dim italic]Candidates for each cell:[/dim italic]", highlight=False)
                # write candidates row by row
                table = PrettyTable()
                table.header = False
                with open("data/output/candidates.txt", "w") as f:
                    for i in range(9):
                        row_candidates = [sorted(candidates[i][j]) for j in range(9)]
                        table.add_row([''.join(item) if isinstance(item, list) else item for item in row_candidates])
                        if i==2 or i==5:
                            table.add_divider()
                        f.write(f"row[{i}]={row_candidates}\n")
                print(table)

                # for i in range(9):
                #     row_candidates = [sorted(candidates[i][j]) for j in range(9)]
                #     console.print(f"Row {i+1}: {row_candidates}", highlight=False)
                break
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--book",
        type=str,
        required=True,
        help="Year-month of the Dell puzzle book",
    )
    parser.add_argument(
        "--puzzle",
        type=str,
        required=True,
        help="Individual Sudoku number in 000 format",
    )
    parser.add_argument(
        "--function",
        choices = ["solve", "add", "delete"],
        default = "solve",
        help="Function to perform"
    )
    args = parser.parse_args()
    main(args)


