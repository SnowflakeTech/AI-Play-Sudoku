import pygame as pg
import os
from grid import Grid, grid_size

# Khởi tạo các thông số
os.environ['SDL_VIDEO_WINDOWS_POS'] = "%d, %d" % (400, 100)
WIDTH, HEIGHT = 600, 600
surface = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Sudoku")

pg.init()
pg.font.init()
game_font = pg.font.SysFont(name='Comic Sans MS', size=30)
menu_font = pg.font.SysFont(name='Comic Sans MS', size=50)

def main_menu():
    """Hiển thị menu chính."""
    while True:
        surface.fill((30, 30, 30))  # Màu nền cho menu
        title_text = menu_font.render("Sudoku", True, (255, 255, 255))
        play_text = game_font.render("Play", True, (0, 255, 0))
        instructions_text = game_font.render("Instructions", True, (0, 255, 0))
        quit_text = game_font.render("Quit", True, (255, 0, 0))

        # Vẽ tiêu đề và các nút
        surface.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        surface.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 250))
        surface.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, 350))
        surface.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 450))

        # Kiểm tra sự kiện click
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()

                # Kiểm tra click vào nút "Play"
                if WIDTH // 2 - play_text.get_width() // 2 <= mouse_x <= WIDTH // 2 + play_text.get_width() // 2 and 250 <= mouse_y <= 250 + play_text.get_height():
                    return  # Bắt đầu trò chơi

                # Kiểm tra click vào nút "Instructions"
                elif WIDTH // 2 - instructions_text.get_width() // 2 <= mouse_x <= WIDTH // 2 + instructions_text.get_width() // 2 and 350 <= mouse_y <= 350 + instructions_text.get_height():
                    print("Instructions: Complete the grid so that every row, column, and 3x3 box contains the numbers 1 to 9 without duplicates.")

                # Kiểm tra click vào nút "Quit"
                elif WIDTH // 2 - quit_text.get_width() // 2 <= mouse_x <= WIDTH // 2 + quit_text.get_width() // 2 and 450 <= mouse_y <= 450 + quit_text.get_height():
                    pg.quit()
                    quit()

        pg.display.update()


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


# Chạy menu chính
main_menu()
# Khi "Play" được chọn, chạy trò chơi
play_game()
