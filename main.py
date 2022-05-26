# import pygame as pg
from Snake import *

pg.init()

pg.display.set_caption('Snake Game :]')
ICON = pg.image.load(os.path.join('Assets', 'snake_head.png'))
pg.display.set_icon(ICON)

clock = pg.time.Clock()
FPS = 60

WHITE, BLACK = (240, 240, 240), (25, 40, 25)
GREEN = (87, 138, 52)
LIGHT_GREEN, DARK_GREEN = (170, 215, 81), (162, 209, 73)
BLUE = (78, 124, 246)
RED = (231, 71, 29)
NEW_BG_GREEN = (101, 146, 113)

block_size = 30

UPDATE_MOVE = pg.USEREVENT + 1
EAT = pg.USEREVENT + 2
GAME_OVER = pg.USEREVENT + 3

pg.time.set_timer(UPDATE_MOVE, 150)

GRASS_PNG = pg.image.load(os.path.join('Assets', 'grass.png'))
grass_image = pg.transform.scale(GRASS_PNG, (block_size - 2, block_size - 2))

class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 600, 600
        self.display = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.WINDOW = pg.Surface((self.WIDTH, self.HEIGHT))
        self.block_size = block_size
        self.snake = Snake(self)
        self.head_rect = pg.Rect(self.snake.body[0].x * self.block_size,
                                 self.snake.body[0].y * self.block_size,
                                 self.block_size,
                                 self.block_size
                                 )
        self.vector_queue = []
        self.fruits = [Fruit(self, self.snake.body)]
        self.game_over = False

    # MAIN GAME LOOP ----------------------------------------------------

    def main(self):
        running = True
        while running:
            clock.tick(FPS)
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    running = False

                self.check_input(event)

                if event.type == UPDATE_MOVE:
                    self.snake.movement()
                    self.vector_queue = []

                if self.game_over:
                    self.snake.direction = Vector2(0, 0)

                    if pg.mouse.get_pressed()[0] or event.type == pg.KEYDOWN:
                        window_rect = self.WINDOW.get_rect()
                        mouse_pos = pg.mouse.get_pos()

                        if window_rect.collidepoint(mouse_pos):
                            self.fruits = [Fruit(self, self.snake.body)]
                            self.snake.reset_snake()
                            self.game_over = False

            self.snake.snake_collision()
            self.screen_limit()
            self.draw_game()

    # ---------------------------------------------------------------------

    def draw_game(self):
        self.WINDOW.fill(NEW_BG_GREEN)
        self.draw_grid()

        for fruit in self.fruits:
            snake_body = self.snake.body[1:]
            if self.fruits[0].pos in snake_body:
                while True:
                    self.fruits[0].randomize()
                    if self.fruits[0].pos not in snake_body:
                        break

            fruit.draw_fruit()

        self.eat()
        self.snake.draw_snake()
        self.display_text(str(self.snake.fruits_eaten),
                          25, WHITE,
                          (3.15 * self.block_size / 2),
                          (2.82 * self.block_size / 2)
                          )

        if self.game_over:
            self.display_text('GAME OVER', 40, WHITE,
                              (self.WIDTH / 2),
                              (self.HEIGHT / 2)
                              )

            self.display_text('Press any button to restart', 12, WHITE,
                              (self.WIDTH / 2),
                              (self.HEIGHT / 2) + 100
                              )

        self.display.blit(self.WINDOW, (0, 0))
        pg.display.update()

    def draw_grid(self):
        for x in range(0, self.WIDTH, block_size):
            for y in range(0, self.HEIGHT, block_size):
                grass_block = pg.Rect(x, y, block_size, block_size)
                self.WINDOW.blit(grass_image, (x, y))

    def display_text(self, text, size, color, x, y):
        # try:
        #     font = pg.font.Font('Quinquefive-0Wonv.ttf', size)
        # except FileNotFoundError:
        font = pg.font.Font(os.path.join('Assets', 'Quinquefive-0Wonv.ttf'), size)

        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        text_rect.center = (x, y)
        self.WINDOW.blit(text_surf, text_rect)

    def eat(self):
        for fruit in self.fruits:
            if fruit.pos == self.snake.body[0]:
                fruit.randomize()
                self.snake.grow = True
                self.snake.fruits_eaten += 1

    def check_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and self.snake.direction != Vector2(0, 1):
                self.snake.direction = Vector2(0, -1)

            if event.key == pg.K_DOWN and self.snake.direction != Vector2(0, -1):
                self.snake.direction = Vector2(0, 1)

            if event.key == pg.K_LEFT and self.snake.direction != Vector2(1, 0):
                self.snake.direction = Vector2(-1, 0)

            if event.key == pg.K_RIGHT and self.snake.direction != Vector2(-1, 0):
                self.snake.direction = Vector2(1, 0)

            self.vector_queue.append(self.snake.direction)

    def screen_limit(self):
        if self.snake.body[0].x < 0:
            self.snake.body[0].x = 0
            self.game_over = True

        if self.snake.body[0].y < 0:
            self.snake.body[0].y = 0
            self.game_over = True

        if self.snake.body[0].x > self.WIDTH / self.block_size - 1:
            self.snake.body[0].x = self.WIDTH / self.block_size - 1
            self.game_over = True

        if self.snake.body[0].y > self.HEIGHT / self.block_size - 1:
            self.snake.body[0].y = self.HEIGHT / self.block_size - 1
            self.game_over = True


game = Game()
if __name__ == '__main__':
    game.main()

# carregar sons
# adcionar tela de iniciar e game over

# BUGS:
# cobra deveria congelar no game over