import pygame as pg
import random as rd
from pygame.math import Vector2
import os

EAT = pg.USEREVENT + 1
GAME_OVER = pg.USEREVENT + 3

block_size = 30

SNAKE_BODY_PNG = pg.image.load(os.path.join('Assets', 'snake_body.png'))
snake_body_image = pg.transform.scale(SNAKE_BODY_PNG, (block_size - 2, block_size - 2))

FRUIT_PNG = pg.image.load(os.path.join('Assets', 'fruit.png'))
fruit_image = pg.transform.scale(FRUIT_PNG, (block_size - 2, block_size - 2))

class Snake:
    def __init__(self, game):
        self.game = game
        self.init_pos = []
        self.size = 3
        for x in reversed(range(5, 5 + self.size)):
            self.init_pos.append(Vector2(x, 9))

        self.body = self.init_pos
        self.direction = Vector2(1, 0)
        self.fruits_eaten = 0
        self.grow = False

    def draw_snake(self):
        for body in self.body:
            snake_rect = pg.Rect(body.x * self.game.block_size,
                                 body.y * self.game.block_size,
                                 self.game.block_size,
                                 self.game.block_size)

            self.game.WINDOW.blit(snake_body_image, (snake_rect.x, snake_rect.y))

    def movement(self):
        if not self.game.game_over:
            if len(self.game.vector_queue) > 0:
                self.direction = self.game.vector_queue[0]

            if self.grow:
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.grow = False

            else:
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]


    def reset_snake(self):
        self.body = self.init_pos
        self.direction = Vector2(1, 0)
        self.fruits_eaten = 0
        self.game.level = 0

    def snake_collision(self):
        for pos in self.body:
            if self.body.count(pos) > 1:
                self.game.game_over = True


class Fruit:
    def __init__(self, game, body):
        self.y = None
        self.x = None
        self.pos = None
        self.game = game
        self.snake_body = body
        self.randlist = []
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pg.Rect(self.game.block_size * self.pos.x - 1,
                             self.game.block_size * self.pos.y - 1,
                             self.game.block_size + 2,
                             self.game.block_size + 2
                             )

        self.game.WINDOW.blit(fruit_image, (fruit_rect.x, fruit_rect.y))

    def randomize(self):
        self.x = rd.randint(0, int(600 / block_size) - 1)
        self.y = rd.randint(0, int(600 / block_size) - 1)

        self.pos = Vector2(self.x, self.y)
