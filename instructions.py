import pygame as pg
from PIL import Image
import os

def load_gif_with_pillow(gif_path, target_width, target_height):
    """
    Load GIF bằng Pillow và chuyển đổi thành các frame Pygame.
    """
    frames = []
    try:
        gif = Image.open(gif_path)
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_surface = pg.image.fromstring(gif.tobytes(), gif.size, gif.mode)
            resized_frame = pg.transform.scale(frame_surface, (target_width, target_height))
            frames.append(resized_frame)
        return frames
    except Exception as e:
        print(f"Lỗi khi tải GIF: {e}")
        return []

def show_instructions(surface, game_font, WIDTH, HEIGHT):
    """Hiển thị hướng dẫn chơi."""
    instructions = [
        "How to Play Sudoku:",
        "1. Fill the grid with numbers 1 to 9.",
        "2. Each row, column, and 3x3 grid must",
        "   contain all numbers without repetition.",
        "Press ESC to return."
    ]
    BACKGROUND_COLOR = (30, 30, 30)
    WHITE = (255, 255, 255)

    # Load GIF bằng Pillow
    gif_path = os.path.join(os.getcwd(), "sudoku.gif")
    gif_frames = load_gif_with_pillow(gif_path, target_width=200, target_height=200)

    clock = pg.time.Clock()
    frame_index = 0  # Chỉ số frame hiện tại

    while True:
        surface.fill(BACKGROUND_COLOR)

        # Vẽ hướng dẫn
        for i, line in enumerate(instructions):
            render_text(surface, line, game_font, WHITE, (WIDTH // 2, 50 + i * 40))
        
        # Hiển thị GIF nếu có
        if gif_frames:
            gif_frame = gif_frames[frame_index]
            surface.blit(gif_frame, (WIDTH // 2 - gif_frame.get_width() // 2, 250))
            frame_index = (frame_index + 1) % len(gif_frames)

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
        
        clock.tick(2)  # Tốc độ phát GIF (10 FPS)

def render_text(surface, text, font, color, position):
    """Vẽ văn bản lên màn hình."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    surface.blit(text_surface, text_rect)
