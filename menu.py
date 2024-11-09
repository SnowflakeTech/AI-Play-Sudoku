import pygame as pg

# Initialize fonts
pg.font.init()
game_font = pg.font.SysFont(name='Comic Sans MS', size=30)
menu_font = pg.font.SysFont(name='Comic Sans MS', size=50)


def main_menu(surface, WIDTH, HEIGHT):
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

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Chỉ thoát khỏi vòng lặp nếu cần thoát chương trình
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                # Check if Play is clicked
                if WIDTH // 2 - play_text.get_width() // 2 <= x <= WIDTH // 2 + play_text.get_width() // 2 and 250 <= y <= 250 + play_text.get_height():
                    return "play"
                # Check if Instructions is clicked
                if WIDTH // 2 - instructions_text.get_width() // 2 <= x <= WIDTH // 2 + instructions_text.get_width() // 2 and 350 <= y <= 350 + instructions_text.get_height():
                    return "instructions"
                # Check if Quit is clicked
                if WIDTH // 2 - quit_text.get_width() // 2 <= x <= WIDTH // 2 + quit_text.get_width() // 2 and 450 <= y <= 450 + quit_text.get_height():
                    pg.quit()
                    exit()
