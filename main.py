import pygame as pg
import os
from grid import Grid, grid_size
from menu import main_menu
from instructions import show_instructions

# Khởi tạo các thông số
os.environ['SDL_VIDEO_WINDOWS_POS'] = "%d, %d" % (400, 100)
WIDTH, HEIGHT = 600, 600
surface = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Sudoku")

pg.init()
pg.font.init()
game_font = pg.font.SysFont(name='Comic Sans MS', size=30)
menu_font = pg.font.SysFont(name='Comic Sans MS', size=50)

# Hàm chính để chạy trò chơi
def play_game():
    countdown_time = 600  # Thời gian đếm ngược tính theo giây
    clock = pg.time.Clock()

    grid = Grid(game_font)
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                grid.handle_mouse_click(pg.mouse.get_pos())
            elif event.type == pg.KEYDOWN:
                if pg.K_1 <= event.key <= pg.K_9:
                    number = event.key - pg.K_0
                    grid.set_selected_number(number)
                elif event.key == pg.K_v:
                    if grid.is_valid_grid():
                        print("Sudoku hợp lệ!")
                    else:
                        print("Sudoku không hợp lệ!")

        # Cập nhật hover mỗi lần chuột di chuyển
        grid.handle_mouse_hover(pg.mouse.get_pos())

        # Giảm thời gian đếm ngược
        countdown_time -= 1 / 60
        if countdown_time <= 0:
            print("Hết thời gian!")
            running = False

        # Vẽ giao diện
        surface.fill((0, 0, 0))
        grid.draw(surface)

        # Hiển thị thời gian đếm ngược
        minutes = int(countdown_time) // 60
        seconds = int(countdown_time) % 60
        time_text = f"{minutes:02}:{seconds:02}"
        time_surface = game_font.render(time_text, True, (0, 255, 0))
        surface.blit(time_surface, (grid_size * grid.cell_size + 20, 5 * grid.cell_size + 20 + 60))

        pg.display.update()
        clock.tick(60)

    pg.quit()


# Chạy menu chính và điều hướng giữa các lựa chọn
if __name__ == "__main__":
    while True:
        try:
            choice = main_menu(surface, WIDTH, HEIGHT)
            if choice == "play":
                play_game()
            elif choice == "instructions":
                show_instructions(surface, game_font, WIDTH, HEIGHT)
        except SystemExit:
            break
    pg.quit()

