import pygame as pg
import os
from grid import Grid, grid_size
from menu import main_menu
from instructions import show_instructions
from solve import solve_sudoku

# Khởi tạo các thông số
os.environ['SDL_VIDEO_WINDOWS_POS'] = "%d, %d" % (400, 100)
WIDTH, HEIGHT = 600, 600
surface = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Sudoku")

icon_path = os.path.join(os.getcwd(), "icon.svg")
if os.path.exists(icon_path):
    icon = pg.image.load(icon_path)  # Tải ảnh icon
    pg.display.set_icon(icon)

pg.init()
pg.font.init()
game_font = pg.font.SysFont(name='Comic Sans MS', size=30)
menu_font = pg.font.SysFont(name='Comic Sans MS', size=50)

def show_message(surface, message, font, color, position):
    pg.draw.rect(surface, (0, 0, 0), (position[0], position[1], 300, 50))
    text_surface = font.render(message, True, color)
    surface.blit(text_surface, position)

def play_game():
    countdown_time = 600  # Thời gian đếm ngược tính theo giây
    clock = pg.time.Clock()

    grid = Grid(game_font)
    running = True
    current_message = ""  # Lưu thông báo hiện tại
    message_timer = 0  # Đếm thời gian hiển thị thông báo

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # Phím ESC được nhấn
                    return "menu"  # Quay lại menu chính và làm mới Sudoku
            elif event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()

                # Kiểm tra nếu nhấn nút Solve
                if grid_size * grid.cell_size + 20 <= x <= grid_size * grid.cell_size + 120 and 5 * grid.cell_size + 140 <= y <= 5 * grid.cell_size + 190:
                    board = [[grid.get_cell(i, j) for i in range(9)] for j in range(9)]
                    if solve_sudoku(board):
                        for j in range(9):
                            for i in range(9):
                                grid.set_cell(i, j, board[j][i])
                        grid.update_status_message("Solved successfully!")
                        message_timer = 3  # Hiển thị thông báo trong 3 giây
                    else:
                        grid.update_status_message("Failed to solve Sudoku.")
                        message_timer = 3  # Hiển thị thông báo trong 3 giây

                # Kiểm tra nếu nhấn nút Check
                elif grid_size * grid.cell_size + 20 <= x <= grid_size * grid.cell_size + 120 and 5 * grid.cell_size + 200 <= y <= 5 * grid.cell_size + 250:
                    if grid.is_valid_grid():
                        grid.update_status_message("Sudoku is valid!")
                        message_timer = 3  # Hiển thị thông báo trong 3 giây
                    else:
                        grid.update_status_message("Sudoku is invalid!")
                        message_timer = 3  # Hiển thị thông báo trong 3 giây
                # Xử lý click vào lưới Sudoku
                else:
                    grid.handle_mouse_click((x, y))


        surface.fill((0, 0, 0))
        grid.draw(surface)

        # Vẽ nút Solve
        solve_rect = pg.Rect(grid_size * grid.cell_size + 20, 5 * grid.cell_size + 130, 100, 50)
        pg.draw.rect(surface, (0, 0, 0), solve_rect)  # Màu xanh cho nút Solve
        pg.draw.rect(surface, (255, 255, 255), solve_rect, 3)  # Viền màu trắng
        solve_text = game_font.render("Solve", True, (255, 255, 255))
        solve_text_rect = solve_text.get_rect(center=solve_rect.center)
        surface.blit(solve_text, solve_text_rect)

        # Vẽ nút Check
        check_rect = pg.Rect(grid_size * grid.cell_size + 20, 5 * grid.cell_size + 200, 100, 50)
        pg.draw.rect(surface, (0, 0, 0), check_rect)  # Màu xanh cho nút Check
        pg.draw.rect(surface, (255, 255, 255), check_rect, 3)  # Viền màu trắng
        check_text = game_font.render("Check", True, (255, 255, 255))
        check_text_rect = check_text.get_rect(center=check_rect.center)
        surface.blit(check_text, check_text_rect)

        clear_button = pg.Rect(grid_size * grid.cell_size + 20, 5 * grid.cell_size + 270, 100, 50)
        pg.draw.rect(surface, (0, 0, 0), clear_button)
        pg.draw.rect(surface, (255, 255, 255), clear_button, 3)
        clear_text = game_font.render("Clear", True, (255, 255, 255))
        clear_text_rect = clear_text.get_rect(center=clear_button.center)
        surface.blit(clear_text, clear_text_rect)

        # Hiển thị thời gian đếm ngược
        countdown_time -= 1 / 60
        minutes = int(countdown_time) // 60
        seconds = int(countdown_time) % 60
        time_text = f"{minutes:02}:{seconds:02}"
        time_surface = game_font.render(time_text, True, (0, 255, 0))
        surface.blit(time_surface, (grid_size * grid.cell_size + 20, 5 * grid.cell_size + 20 + 60))

        # Hiển thị thông báo
        if current_message:
            show_message(surface, current_message, game_font, (255, 255, 255), (80, 450))
            message_timer -= 1 / 60  # Giảm thời gian còn lại
            if message_timer <= 0:
                current_message = ""  # Ẩn thông báo khi hết thời gian

        pg.display.update()
        clock.tick(60)

    pg.quit()

# Chạy menu chính và điều hướng giữa các lựa chọn
if __name__ == "__main__":
    while True:
        try:
            choice = main_menu(surface, WIDTH, HEIGHT)
            if choice == "play":
                # Nếu từ game quay lại menu, sẽ lặp lại menu chính
                game_state = play_game()
                if game_state == "menu":
                    continue
                elif game_state == "quit":
                    break
            elif choice == "instructions":
                show_instructions(surface, game_font, WIDTH, HEIGHT)
            elif choice == "quit":
                pg.quit()
                break
        except SystemExit:
            break
    pg.quit()

