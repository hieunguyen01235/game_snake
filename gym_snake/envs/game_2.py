import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym import utils
import numpy as np

# -----------------------------------------------------
from pygame.locals import *
from random import randint
import pygame
from pygame import gfxdraw
import time


# Set options to activate or deactivate the game view, and its speed
display_option = False
speed = 50
size = 20
time_run = 1000.0
pygame.font.init()

def eat(player, food, game):
    if player.x == food.x_food and player.y == food.y_food:
        food.food_coord(game, player)
        player.eaten = True
        game.score = game.score + 1

class Game:

    def __init__(self, game_width, game_height):
        pygame.display.set_caption('SnakeGen')
        self.game_width = game_width
        self.game_height = game_height
        #-------------
        self.gameDisplay = pygame.display.set_mode((game_width, game_height + 60))
        self.bg = pygame.image.load("img/background.png")
        #------------
        self.crash = False
        self.player = Player(self)
        self.food = Food()
        self.score = 0


class Player(object):

    def __init__(self, game,length):
        self.length = length
        # taoj vi tri ban dau
        x = 0.5 * game.game_width
        y = 0.5 * game.game_height

        # Thiet lap vi tri theo quy luat
        self.x = x - x % size
        self.y = y - y % size

        # lay cac vi tri cua con ran
        self.position = []
        self.position.append([self.x, self.y])

        #Tao du lieu phan thuong
        self.food = 1

        # xac dinh co an phan thuong
        self.eaten = False

        self.image = pygame.image.load('img/snakeBody.png')

        # chieu cua ran mac dinh la di theo huong phai moi lan += size
        self.x_change = size
        self.y_change = 0

    def update_position(self, x, y):
        #cap nhat lai cac vi tri khi co thao tac moi

        if self.position[-1][0] != x or self.position[-1][1] != y:
            if self.food > 1:
                for i in range(0, self.food - 1):
                    self.position[i][0], self.position[i][1] = self.position[i + 1]
            self.position[-1][0] = x
            self.position[-1][1] = y

    def do_move(self, move, x, y, game, food, agent):
        move_array = [self.x_change, self.y_change]

        # kiem tra phan thuong va chieu dai
        if self.eaten:
            self.position.append([self.x, self.y])
            self.eaten = False
            self.food = self.food + 1

        if np.array_equal(move, [1, 0, 0]):
            move_array = self.x_change, self.y_change
        elif np.array_equal(move, [0, 1, 0]) and self.y_change == 0:  # right - going horizontal
            move_array = [0, self.x_change]
        elif np.array_equal(move, [0, 1, 0]) and self.x_change == 0:  # right - going vertical
            move_array = [-self.y_change, 0]
        elif np.array_equal(move, [0, 0, 1]) and self.y_change == 0:  # left - going horizontal
            move_array = [0, -self.x_change]
        elif np.array_equal(move, [0, 0, 1]) and self.x_change == 0:  # left - going vertical
            move_array = [self.y_change, 0]

        #update position new
        self.x_change, self.y_change = move_array
        self.x = x + self.x_change
        self.y = y + self.y_change

        # dung tuong
        if self.x < 20 or self.x > game.game_width - 40 or self.y < 20 or self.y > game.game_height - 40 or [self.x,
                                                                                                             self.y] in self.position:
            game.crash = True


        eat(self, food, game)

        self.update_position(self.x, self.y)

    def display_player(self, x, y, food, game):
        self.position[-1][0] = x
        self.position[-1][1] = y

        if game.crash == False:
            for i in range(food):
                x_temp, y_temp = self.position[len(self.position) - 1 - i]
                game.gameDisplay.blit(self.image, (x_temp, y_temp))

            update_screen()
        else:
            pygame.time.wait(time_run)


class Food(object):

    def __init__(self):
        self.x_food = 240
        self.y_food = 200
        self.image = pygame.image.load('img/food2.png')

    def food_coord(self, game, player):
        x_rand = randint(size, game.game_width - 40)
        self.x_food = x_rand - x_rand % size
        y_rand = randint(size, game.game_height - 40)
        self.y_food = y_rand - y_rand % size

        if [self.x_food, self.y_food] not in player.position:
            return self.x_food, self.y_food
        else:
            self.food_coord(game, player)

    def display_food(self, x, y, game):
        game.gameDisplay.blit(self.image, (x, y))
        update_screen()


class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array'], 'video.frames_per_second': 50}
    # time_temp = 1000.0

    def __init__(self):
        game = Game(440, 440)
        player1 = game.player
        food1 = game.food

        self._running = True
        self._display_surf = None

        self.state = None
        self.action_space = spaces.Discrete(4)

    def kiemtra(self, direction, action):
        if (action == 0 and direction == 1):
            return direction
        elif (action == 1 and direction == 0):
            return direction
        elif (action == 2 and direction == 3):
            return direction
        elif (action == 3 and direction == 2):
            return direction
        return action

    def step(self, action):
        done = self.get_done()
        self.get_action(action, self.player.direction)
        reward = self.get_reward()
        ob = self.get_state()
        return ob, reward, done, {}

    def get_state(self):
        state = [
            self.player.direction == 1,  # move left
            self.player.direction == 0,  # move right
            self.player.direction == 2,  # move up
            self.player.direction == 3,  # move down
            self.apple.x < self.player.x[0],  # food left
            self.apple.x > self.player.x[0],  # food right
            self.apple.y < self.player.y[0],  # food up
            self.apple.y > self.player.y[0]  # food down
        ]
        for i in range(len(state)):
            if state[i]:
                state[i] = 1
            else:
                state[i] = 0
        return np.asarray(state)

    def get_action(self, action, direction):

        self.player.direction = self.kiemtra(self.player.direction, action[0])

        for i in range(self.player.length - 1, 0, -1):
            self.player.x[i] = self.player.x[i - 1]
            self.player.y[i] = self.player.y[i - 1]

        if self.player.direction == 0:
            self.player.x[0] = self.player.x[0] + size
        if self.player.direction == 1:
            self.player.x[0] = self.player.x[0] - size
        if self.player.direction == 2:
            self.player.y[0] = self.player.y[0] - size
        if self.player.direction == 3:
            self.player.y[0] = self.player.y[0] + size

    def get_reward(self):
        temp = 0
        # self.player.update()
        if self.game.isCollision(self.apple.x, self.apple.y, self.player.x[0], self.player.y[0], size):
            self.apple.x = randint(2, 9) * size
            self.apple.y = randint(2, 9) * size
            self.player.length = self.player.length + 1
            temp = 1
            print("--------------------------------co diem", temp)
        return temp

    def get_done(self):
        temp = False
        for i in range(2, self.player.length):
            if self.game.isCollision(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i], size):
                temp = True
                print("can duoi")
                break
        if (self.player.x[0] >= 440 or self.player.x[0] <= -1 or self.player.y[0] + size > 440 or self.player.y[
            0] < -1):
            print("dung tuong")
            temp = True
        return temp

    def reset(self):
        self.on_cleanup()
        self.player = Player(3)
        self.apple = Apple(10, 5)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self._running = True

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.player.draw(self._display_surf)
        self.apple.draw(self._display_surf)

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def render(self, mode='human', close=False):
        if self.on_init() == False:
            self._running = False
        pygame.event.pump()
        temp = self.get_reward()
        self.on_render()
        time.sleep(self.time_temp / 1000.0)
        # self.on_cleanup()


def display_ui(game, score, record):
    myfont = pygame.font.SysFont('Segoe UI', 20)
    myfont_bold = pygame.font.SysFont('Segoe UI', 20, True)
    text_score = myfont.render('SCORE: ', True, (0, 0, 0))
    text_score_number = myfont.render(str(score), True, (0, 0, 0))
    text_highest = myfont.render('HIGHEST SCORE: ', True, (0, 0, 0))
    text_highest_number = myfont_bold.render(str(record), True, (0, 0, 0))
    game.gameDisplay.blit(text_score, (45, 440))
    game.gameDisplay.blit(text_score_number, (120, 440))
    game.gameDisplay.blit(text_highest, (190, 440))
    game.gameDisplay.blit(text_highest_number, (350, 440))
    game.gameDisplay.blit(game.bg, (10, 10))


def display(player, food, game, record):
    game.gameDisplay.fill((255, 255, 255))
    display_ui(game, game.score, record)
    player.display_player(player.position[-1][0], player.position[-1][1], player.food, game)
    food.display_food(food.x_food, food.y_food, game)


def update_screen():
    pygame.display.update()


# def initialize_game(player, game, food, agent):
#     state_init1 = agent.get_state(game, player, food)  # [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]
#     action = [1, 0, 0]
#     player.do_move(action, player.x, player.y, game, food, agent)
#     state_init2 = agent.get_state(game, player, food)
#     reward1 = agent.set_reward(player, game.crash)
#     agent.remember(state_init1, action, reward1, state_init2, game.crash)
#     agent.replay_new(agent.memory)

