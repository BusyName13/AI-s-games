import pygame
import random

# Настройки
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH = WIDTH // BLOCK_SIZE
GRID_HEIGHT = HEIGHT // BLOCK_SIZE

# Определяем фигуры
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 0, 1]],  # L
    [[1, 1, 1], [1, 0, 0]],  # J
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# Colors
COLORS = [
    (0, 255, 255),  # I
    (255, 165, 0),  # L
    (0, 0, 255),    # J
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0)     # Z
]

class Tetris:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.current_pos = (0, GRID_WIDTH // 2 - 1)
        self.score = 0

    def new_piece(self):
        index = random.randint(0, len(SHAPES) - 1)
        return SHAPES[index], COLORS[index]

    def rotate_piece(self):
        new_piece = [list(row) for row in zip(*self.current_piece[0][::-1])]
        if not self.collision((self.current_pos[0], self.current_pos[1]), new_piece):
            self.current_piece = new_piece, self.current_piece[1]  # сохраняем цвет

    def move_piece(self, dx):
        new_pos = (self.current_pos[0], self.current_pos[1] + dx)
        if not self.collision(new_pos):
            self.current_pos = new_pos

    def drop_piece(self):
        new_pos = (self.current_pos[0] + 1, self.current_pos[1])
        if not self.collision(new_pos):
            self.current_pos = new_pos
        else:
            self.place_piece()

    def collision(self, new_pos, piece=None):
        if piece is None:
            piece = self.current_piece[0]
        for i, row in enumerate(piece):
            for j, val in enumerate(row):
                if val:
                    x = new_pos[0] + i
                    y = new_pos[1] + j
                    if x >= GRID_HEIGHT or y < 0 or y >= GRID_WIDTH or self.grid[x][y]:
                        return True
        return False

    def place_piece(self):
        piece, color = self.current_piece
        for i, row in enumerate(piece):
            for j, val in enumerate(row):
                if val:
                    self.grid[self.current_pos[0] + i][self.current_pos[1] + j] = color
        lines_cleared = self.clear_lines()
        self.update_score(lines_cleared)
        self.current_piece = self.new_piece()
        self.current_pos = (0, GRID_WIDTH // 2 - 1)
        if self.collision(self.current_pos):
            self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]  # Очистить поле, если игра закончена

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(val != 0 for val in row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0] * GRID_WIDTH)
        return len(lines_to_clear)

    def update_score(self, lines_cleared):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800

    def draw(self, surface):
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(surface, val, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        # Рисуем текущую фигуру
        piece, color = self.current_piece
        for i, row in enumerate(piece):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(surface, color, ((self.current_pos[1] + j) * BLOCK_SIZE, (self.current_pos[0] + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        # Рисуем счет
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        surface.blit(score_text, (10, 10))

def draw_window(surface, tetris):
    surface.fill((0, 0, 0))
    tetris.draw(surface)
    pygame.display.flip()

def main():
    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    tetris = Tetris()
    run = True
    drop_time = 0

    while run:
        clock.tick(10)  # FPS
        drop_time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move_piece(-1)
                elif event.key == pygame.K_RIGHT:
                    tetris.move_piece(1)
                elif event.key == pygame.K_DOWN:
                    tetris.drop_piece()
                elif event.key == pygame.K_UP:
                    tetris.rotate_piece()
                elif event.key == pygame.K_ESCAPE:
                    run = False  # Выход из игры при нажатии Esc

        if drop_time >= 10:
            tetris.drop_piece()
            drop_time = 0

        draw_window(surface, tetris)

    pygame.quit()

if __name__ == "__main__":
    main()
