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
        
    def check_rows(self) -> bool:
        """Kiểm tra các hàng xem có tuân theo quy tắc Sudoku không."""
        for row in self.grid:
            if not self.is_valid_group(row):
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
                if self.get_cell(x, y) != 0:
                    color = (0, 200, 255) if not self.occupied_cells[y][x] else (255, 0, 0)  # Số của các ô preoccupied có màu đỏ
                    text_surface = self.game_font.render(str(self.get_cell(x, y)), True, color)
                    text_rect = text_surface.get_rect(center=(x * self.cell_size + self.cell_size // 2,
                                                              y * self.cell_size + self.cell_size // 2))
                    surface.blit(text_surface, text_rect)  # Vẽ số ở vị trí đã căn giữa

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
        """Xử lý sự kiện khi người chơi click chuột vào một ô."""
        x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
        if x < grid_size and y < grid_size and not self.occupied_cells[y][x]:
            print(f"Clicked on cell ({x}, {y})")
            if self.selected_number is not None:  # Chỉ điền số khi có số được chọn
                self.set_cell(x, y, self.selected_number)
        elif x >= grid_size:  # Nếu click vào khu vực bảng chọn số
            self.handle_number_selection(pos)

    def handle_number_selection(self, pos):
        """Xử lý chọn số từ bảng chọn số."""
        menu_x1 = grid_size * self.cell_size + 20
        menu_x2 = grid_size * self.cell_size + 90
        if menu_x1 <= pos[0] < menu_x1 + 50:  # Cột 1
            selected_index = (pos[1] - 20) // 60 + 1
            if 1 <= selected_index <= 5:
                self.selected_number = selected_index
        elif menu_x2 <= pos[0] < menu_x2 + 50:  # Cột 2
            selected_index = (pos[1] - 20) // 60 + 6
            if 6 <= selected_index <= 9:
                self.selected_number = selected_index

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
            
if __name__ == '__main__':
    pg.font.init()
    game_font = pg.font.SysFont(name='Cascadia Code', size=30)  # Giảm kích thước font chữ
    grid = Grid(game_font)
    grid.show()
