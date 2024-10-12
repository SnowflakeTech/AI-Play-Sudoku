import pygame as pg
import os
from grid import Grid

os.environ['SDL_VIDEO_WINDOWS_POS'] = "%d, %d" % (400, 100)
WIDTH, HEIGHT = 600, 450  # Tăng chiều rộng để thêm bảng chọn số
surface = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Sudoku")

pg.init()  # Khởi tạo pygame
pg.font.init()
game_font = pg.font.SysFont(name='Comic Sans MS', size=30)  # Giảm kích thước font chữ

grid = Grid(game_font)  # Khởi tạo lưới với font chữ
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            grid.handle_mouse_click(pg.mouse.get_pos())  # Xử lý khi click chuột
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_v:  # Nhấn phím 'V' để kiểm tra lưới Sudoku
                if grid.is_valid_grid():
                    print("Sudoku hợp lệ!")
                else:
                    print("Sudoku không hợp lệ!")
    
    # Cập nhật hover mỗi lần chuột di chuyển
    grid.handle_mouse_hover(pg.mouse.get_pos())
    
    surface.fill((0, 0, 0))  # Xóa màn hình với màu đen
    grid.draw_lines(pg, surface)  # Vẽ các đường lưới
    grid.draw_numbers(surface)  # Vẽ các số
    grid.draw_number_selection_menu(surface)  # Vẽ bảng chọn số
    pg.display.update()  # Cập nhật màn hình sau khi vẽ

pg.quit()  # Thoát pygame sau khi vòng lặp kết thúc
