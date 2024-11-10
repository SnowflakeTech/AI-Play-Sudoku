import unittest
from grid import Grid, create_grid, remove_numbers, grid_size, sub_grid_size
import pygame as pg

class TestSudoku(unittest.TestCase):
    def setUp(self):
        pg.font.init()
        self.font = pg.font.SysFont("Comic Sans MS", 30)
        self.grid = Grid(self.font)

    def test_grid_creation(self):
        """Kiểm tra lưới được tạo đúng kích thước và giá trị."""
        sudoku_grid = create_grid(sub_grid_size)
        self.assertEqual(len(sudoku_grid), grid_size)
        for row in sudoku_grid:
            self.assertEqual(len(row), grid_size)

    def test_remove_numbers(self):
        """Kiểm tra các ô bị khóa được đánh dấu đúng."""
        sudoku_grid = create_grid(sub_grid_size)
        occupied_cells = remove_numbers(sudoku_grid)
        empty_count = sum([row.count(0) for row in sudoku_grid])
        self.assertGreater(empty_count, 0)
        for y in range(grid_size):
            for x in range(grid_size):
                if sudoku_grid[y][x] == 0:
                    self.assertFalse(occupied_cells[y][x])

    def test_clear_grid(self):
        """Kiểm tra chức năng xóa lưới."""
        self.grid.clear_grid()
        for y in range(grid_size):
            for x in range(grid_size):
                if not self.grid.occupied_cells[y][x]:
                    self.assertEqual(self.grid.grid[y][x], 0)

    def test_valid_grid(self):
        """Kiểm tra lưới có hợp lệ không."""
        self.assertTrue(self.grid.is_valid_grid())

    def test_set_cell(self):
        """Kiểm tra việc đặt số vào ô."""
        self.grid.set_cell(0, 0, 5)
        if not self.grid.occupied_cells[0][0]:
            self.assertEqual(self.grid.grid[0][0], 5)

    def test_invalid_number(self):
        """Kiểm tra việc phát hiện số không hợp lệ."""
        self.assertFalse(self.grid.is_number_valid(10, 0, 0))  # 10 là số không hợp lệ

    class TestSudokuUI(unittest.TestCase):
        def setUp(self):
            pg.init()
            pg.font.init()
            self.font = pg.font.SysFont("Comic Sans MS", 30)
            self.grid = Grid(self.font)
            self.surface = pg.Surface((600, 600))

        def test_clear_button(self):
            """Kiểm tra nút Clear hoạt động đúng."""
            # Mô phỏng nhấn nút Clear
            clear_x, clear_y = grid_size * self.grid.cell_size + 30, 5 * self.grid.cell_size + 280
            event = pg.event.Event(pg.MOUSEBUTTONDOWN, {"pos": (clear_x, clear_y)})
            self.grid.handle_mouse_click(event.pos)

            # Kiểm tra lưới đã được xóa
            for y in range(grid_size):
                for x in range(grid_size):
                    if not self.grid.occupied_cells[y][x]:
                        self.assertEqual(self.grid.grid[y][x], 0)

        def test_number_selection(self):
            """Kiểm tra chọn số từ bảng chọn số."""
            number_x, number_y = grid_size * self.grid.cell_size + 40, 40
            event = pg.event.Event(pg.MOUSEBUTTONDOWN, {"pos": (number_x, number_y)})
            self.grid.handle_mouse_click(event.pos)

            # Kiểm tra số được chọn
            self.assertEqual(self.grid.selected_number, 1)

if __name__ == "__main__":
    unittest.main()
