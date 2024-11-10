import pygame as pg
from random import sample

def create_lines_coordinates(cell_size: int):
    points = []

    # Vẽ các đường ngang và dọc
    for i in range(1, 9):  # Đường ngang
        y = i * cell_size
        points.append(((0, y), (cell_size * 9, y)))  # Điều chỉnh chiều rộng của lưới

    for i in range(1, 10):  # Đường dọc
        x = i * cell_size
        points.append(((x, 0), (x, cell_size * 9)))  # Điều chỉnh chiều cao của lưới

    return points


sub_grid_size = 3
grid_size = sub_grid_size * sub_grid_size

def pattern(row_num: int, col_num: int):
    return (sub_grid_size * (row_num % sub_grid_size) + row_num // sub_grid_size + col_num) % grid_size

def shuffle(samp: range) -> list:
    return sample(samp, len(samp))

def create_grid(sub_grid: int) -> list[list]:
    """Tạo lưới 9x9 với số random

    Args:
        sub_grid (int): lưới con

    Returns:
        list[list]: lưới
    """
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]

def remove_numbers(grid: list[list]) -> list[list]:
    """Xóa số khỏi lưới và đánh dấu các ô bị occupied."""
    num_of_cells = grid_size * grid_size
    empties = num_of_cells * 3 // 7
    occupied_cells = [[True for _ in range(grid_size)] for _ in range(grid_size)]  # Ban đầu tất cả ô đều preoccupied
    for i in sample(range(num_of_cells), empties):
        grid[i // grid_size][i % grid_size] = 0
        occupied_cells[i // grid_size][i % grid_size] = False  # Đánh dấu ô trống
    return occupied_cells

class Grid:
    def __init__(self, font) -> None:
        self.cell_size = 50  # Kích thước ô lưới
        self.line_coordinates = create_lines_coordinates(self.cell_size)
        self.grid = create_grid(sub_grid_size)
        self.game_font = font
        self.occupied_cells = remove_numbers(self.grid)  # Đánh dấu các ô preoccupied
        self.selected_cell = None  # Vị trí ô được chọn để điền số
        self.selected_number = None  # Số đang được chọn để điền vào ô
        self.hovered_number = None  # Số nào đang được hover
        self.highlighted_cells = []  # Danh sách các ô cần làm nổi bật
        self.status_message = ""

    def check_rows(self) -> bool:
        """Kiểm tra các hàng xem có tuân theo quy tắc Sudoku không."""
        for row in self.grid:
            if not self.is_valid_group(row):
                return False
        return True

    def check_columns(self) -> bool:
        """Kiểm tra các cột xem có tuân theo quy tắc Sudoku không."""
        for col in range(grid_size):
            column = self.get_column(col)
            if not self.is_valid_group(column):
                return False
        return True

    def check_subgrids(self) -> bool:
        """Kiểm tra các vùng 3x3 xem có tuân theo quy tắc Sudoku không."""
        for box_row in range(0, grid_size, sub_grid_size):
            for box_col in range(0, grid_size, sub_grid_size):
                subgrid = []
                for r in range(box_row, box_row + sub_grid_size):
                    for c in range(box_col, box_col + sub_grid_size):
                        subgrid.append(self.grid[r][c])
                if not self.is_valid_group(subgrid):
                    return False
        return True

    def is_valid_group(self, group: list) -> bool:
        """Kiểm tra xem một nhóm số (hàng, cột hoặc vùng 3x3) có hợp lệ không."""
        numbers = [num for num in group if num != 0]  # Bỏ qua các ô trống
        return len(numbers) == len(set(numbers))  # Nếu số lượng các số không trùng khớp, nhóm không hợp lệ

    def show(self):
        for row in self.grid:
            print(row)

    def is_valid_grid(self) -> bool:
        """Kiểm tra toàn bộ lưới Sudoku xem có hợp lệ không."""
        return self.check_rows() and self.check_columns() and self.check_subgrids()

    def draw_lines(self, pg, surface):
        for index, line in enumerate(self.line_coordinates):
            if index == 2 or index == 5 or index == 10 or index == 13:
                pg.draw.line(surface, (255, 200, 0), line[0], line[1], 5)
            else:
                pg.draw.line(surface, (0, 50, 0), line[0], line[1], 2)

    def draw_numbers(self, surface) -> None:
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                cell_value = self.get_cell(x, y)
                if cell_value != 0:
                    # Kiểm tra màu dựa trên trạng thái của ô
                    if (x, y) == self.selected_cell:
                        color = (200, 255, 200)  # Màu xanh nhạt cho ô được chọn
                    elif not self.occupied_cells[y][x]:
                        # Các ô không bị khóa sẽ có màu xanh nước biển
                        color = (0, 200, 255)
                    else:
                        # Các ô ban đầu (preoccupied) sẽ có màu đỏ
                        color = (255, 0, 0)

                    # Vẽ số vào ô
                    text_surface = self.game_font.render(str(cell_value), True, color)
                    text_rect = text_surface.get_rect(center=(x * self.cell_size + self.cell_size // 2,
                                                              y * self.cell_size + self.cell_size // 2))
                    surface.blit(text_surface, text_rect)

    def get_row(self, row):
        """Trả về danh sách các giá trị trong một hàng."""
        return self.grid[row]

    def get_column(self, col):
        """Trả về danh sách các giá trị trong một cột."""
        return [self.grid[row][col] for row in range(grid_size)]

    def draw_highlighted_cells(self, surface):
        """Làm nổi bật hàng và cột của ô đang được chọn."""
        for x, y in self.highlighted_cells:
            rect = pg.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            pg.draw.rect(surface, (200, 200, 255), rect, 0)  # Màu xanh nhạt cho ô nổi bật

    def draw(self, surface):
        # Gọi vẽ các thành phần
        self.draw_highlighted_cells(surface)  # Vẽ các ô nổi bật trước
        self.draw_lines(pg, surface)
        self.draw_numbers(surface)
        self.draw_number_selection_menu(surface)
        self.draw_highlighted_cells(surface)
        self.draw_lines(pg, surface)
        self.draw_numbers(surface)
        self.draw_number_selection_menu(surface)
        if self.status_message:
            message_surface = self.game_font.render(self.status_message, True, (255, 255, 255))
            surface.blit(message_surface, (50, grid_size * self.cell_size + 50))


    def draw_number_selection_menu(self, surface):
        """Vẽ bảng chọn số với 2 cột bên phải lưới."""
        menu_x1 = grid_size * self.cell_size + 20  # Cột thứ nhất
        menu_x2 = grid_size * self.cell_size + 90  # Cột thứ hai
        menu_y = 20

        for i in range(1, 6):
            # Vẽ cột đầu tiên (số 1 đến 5)
            rect = pg.Rect(menu_x1, menu_y + (i - 1) * 60, 50, 50)
            color = (0, 255, 0) if i == self.selected_number else (255, 255, 255)  # Đổi màu nếu số được chọn
            if i == self.hovered_number:  # Đổi màu khi hover
                pg.draw.rect(surface, (255, 255, 0), rect, 3)
            else:
                pg.draw.rect(surface, color, rect, 3)
            text_surface = self.game_font.render(str(i), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            surface.blit(text_surface, text_rect)

        for i in range(6, 10):
            # Vẽ cột thứ hai (số 6 đến 9)
            rect = pg.Rect(menu_x2, menu_y + (i - 6) * 60, 50, 50)
            color = (0, 255, 0) if i == self.selected_number else (255, 255, 255)  # Đổi màu nếu số được chọn
            if i == self.hovered_number:  # Đổi màu khi hover
                pg.draw.rect(surface, (255, 255, 0), rect, 3)
            else:
                pg.draw.rect(surface, color, rect, 3)
            text_surface = self.game_font.render(str(i), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            surface.blit(text_surface, text_rect)

    def handle_mouse_click(self, pos):
        """Xử lý sự kiện khi người chơi click chuột vào một ô hoặc bảng chọn số."""
        x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
        # Kiểm tra click trong lưới Sudoku
        if x < grid_size and y < grid_size:
            self.selected_cell = (x, y)
            self.highlighted_cells = [(x, i) for i in range(grid_size)] + [(i, y) for i in range(grid_size)]
            if not self.occupied_cells[y][x] and self.selected_number is not None:
                if self.is_number_valid(self.selected_number, x, y):
                    self.set_cell(x, y, self.selected_number)
                    self.status_message = f"Number {self.selected_number} is placed in box ({x}, {y})"
                else:
                    self.status_message = "Error: Number is invalid!"
        # Kiểm tra click trong bảng chọn số
        elif (grid_size * self.cell_size + 20 <= pos[0] <= grid_size * self.cell_size + 140 and
              20 <= pos[1] <= 320):
            self.handle_number_selection(pos)
        else:
            # Click ngoài lưới Sudoku và bảng chọn số
            self.selected_cell = None
            self.status_message = ""  # Xóa thông báo

    def handle_number_selection(self, pos):
        """Xử lý chọn số từ bảng chọn số."""
        menu_x1 = grid_size * self.cell_size + 20
        menu_x2 = grid_size * self.cell_size + 90
        if menu_x1 <= pos[0] < menu_x1 + 50:  # Cột 1
            selected_index = (pos[1] - 20) // 60 + 1
            if 1 <= selected_index <= 5:
                self.selected_number = selected_index
                self.status_message = f"Selected number: {self.selected_number}"
        elif menu_x2 <= pos[0] < menu_x2 + 50:  # Cột 2
            selected_index = (pos[1] - 20) // 60 + 6
            if 6 <= selected_index <= 9:
                self.selected_number = selected_index
                self.status_message = f"Selected number: {self.selected_number}"

    def set_cell(self, x: int, y: int, value: int) -> None:
        """Chỉ cho phép thay đổi giá trị của các ô không bị preoccupied."""
        if not self.occupied_cells[y][x]:
            self.grid[y][x] = value

    def set_selected_number(self, number: int) -> None:
        """Thiết lập số được chọn từ menu số và kiểm tra hợp lệ."""
        self.selected_number = number
        print(f"Selected number: {self.selected_number}")

    def handle_mouse_hover(self, pos):
        """Xử lý hover chuột vào bảng chọn số."""
        menu_x1 = grid_size * self.cell_size + 20
        menu_x2 = grid_size * self.cell_size + 90
        if menu_x1 <= pos[0] < menu_x1 + 50:  # Hover trong cột 1
            self.hovered_number = (pos[1] - 20) // 60 + 1
            if not (1 <= self.hovered_number <= 5):
                self.hovered_number = None
        elif menu_x2 <= pos[0] < menu_x2 + 50:  # Hover trong cột 2
            self.hovered_number = (pos[1] - 20) // 60 + 6
            if not (6 <= self.hovered_number <= 9):
                self.hovered_number = None
        else:
            self.hovered_number = None  # Không hover vào số nào

    def get_cell(self, x: int, y: int) -> int:
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, value: int) -> None:
        """Chỉ cho phép thay đổi giá trị của các ô không bị preoccupied."""
        if not self.occupied_cells[y][x]:
            self.grid[y][x] = value

    def show(self):
        for cell in self.grid:
            print(cell)

    def is_number_valid(self, number, x, y) -> bool:
        """Kiểm tra xem số có hợp lệ tại vị trí x, y không."""
        # Tạm thời lưu số hiện tại trong ô để kiểm tra
        current_value = self.grid[y][x]
        self.grid[y][x] = number

        # Kiểm tra xem số có hợp lệ trong hàng, cột và ô 3x3 không
        is_valid = self.check_rows() and self.check_columns() and self.check_subgrids()

        # Khôi phục giá trị cũ trong ô
        self.grid[y][x] = current_value
        return is_valid



if __name__ == '__main__':
    pg.font.init()
    game_font = pg.font.SysFont(name='Cascadia Code', size=30)  # Giảm kích thước font chữ
    grid = Grid(game_font)
    grid.show()
