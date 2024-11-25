import unittest
import time
from solve import solve_sudoku

class TestSudokuSolvePerformance(unittest.TestCase):
    def setUp(self):
        self.sudoku_board = [
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

    def test_solve_time(self):
        max_time = 1.0

        for i in range(10):
            with self.subTest(run=i + 1):

                sudoku_board_copy = [row[:] for row in self.sudoku_board]

                # Đo thời gian
                start_time = time.time()
                solved = solve_sudoku(sudoku_board_copy)
                end_time = time.time()

                elapsed_time = end_time - start_time

                # Kiểm tra kết quả và in chi tiết
                self.assertTrue(solved, f"Run {i + 1}: Sudoku could not be solved.")
                self.assertLess(elapsed_time, max_time, f"Run {i + 1}: Took too long.")
                print(f"Run {i + 1}: Thời gian giải Sudoku: {elapsed_time:.4f} giây")

if __name__ == "__main__":
    unittest.main()
