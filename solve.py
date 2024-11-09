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
