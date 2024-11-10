def is_valid(board, row, col, num):
    """Kiểm tra xem có thể điền `num` vào ô (row, col) không."""
    # Kiểm tra hàng
    for i in range(9):
        if board[row][i] == num:
            return False

    # Kiểm tra cột
    for i in range(9):
        if board[i][col] == num:
            return False

    # Kiểm tra ô 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True


def solve_sudoku(board):
    """Giải Sudoku bằng thuật toán Backtracking."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Tìm ô trống
                for num in range(1, 10):  # Thử các số từ 1 đến 9
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0  # Quay lui
                return False
    return True

if __name__ == "__main__":
    sudoku_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    if solve_sudoku(sudoku_board):
        print("Sudoku solved successfully!")
        for row in sudoku_board:
            print(row)
    else:
        print("No solution exists.")

