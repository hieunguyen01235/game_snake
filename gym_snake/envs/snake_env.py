import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym import utils
import numpy as np
from operator import add
# -----------------------------------------------------
from pygame.locals import *
from random import randint
import pygame
from pygame import gfxdraw
import time

# display_option = False
green = (0, 255, 0)
red = (255, 0, 0)
cyan = (255, 128, 0)
time_temp =100.0
size = 20

width = 440
heigth = 440



class Game:
    def __init__(self, game_width, game_height):
        pygame.display.set_caption('SnakeGen')
        self.game_width = game_width
        self.game_height = game_height
        self.gameDisplay = pygame.display.set_mode((game_width, game_height+60))
        self.bg = None
        

        self.display_option = False
        self.crash = False
        self.player = Player(self)
        self.food = Apple()
        self.score = 0
    # def isCollision(self,x1,y1,x2,y2,bsize):
    #     if (x2 >= x1 and x2 < x1 + bsize):
    #         if (y2 >= y1 and y2 < y1 + bsize):
    #             return True
    #     return False


class Apple(object):
    x = 0
    y = 0
    step = size

    def __init__(self):
        self.x = 10 * size
        self.y = 10 * size
        self.image = None

    def food_coord(self, game, player):

        x_rand = randint(size, game.game_width - 40)
        self.x = x_rand - x_rand % size

        y_rand = randint(size, game.game_height - 40)

        self.y = y_rand - y_rand % size
        # print("co vao cho nay ", x_rand, y_rand)
        if [self.x, self.y] not in player.position:
            return self.x, self.y
            # print("co nha --------------------=")

        else:
            self.food_coord(game, player)


    def draw(self, x, y, game):
        if (game.display_option):
            game.gameDisplay.blit(self.image, (x, y))
        else:
            pygame.gfxdraw.box(game.gameDisplay, (self.x, self.y, size, size), red)
        update_screen()


class Player(object):

    def __init__(self, game):
        # tao vi tri ban dau moi lan khoi tao
        x = 0.5 * game.game_width
        y = 0.5 * game.game_height
        self.x = x - x % size
        self.y = y - y % size

        self.position = []
        self.position.append([self.x, self.y])


        self.food = 1
        self.eaten = False

        self.image = None
        # chieu cua ran mac dinh la di theo huong phai moi lan += size
        self.direction = 0
        self.x_change = 20
        self.y_change = 0
        # self.position.append([self.x - self.x_change, self.y- self.y_change])
        # self.position.append([self.x- 2 * self.x_change, self.y- 2 * self.y_change])

    def update_position(self, x, y):
        # print(self.position[-1][0])
        #| | | | | | | | | | | | |   x
        #| | | | | | | | | | | | |   y
        if self.position[-1][0] != x or self.position[-1][1] != y:
            if self.food > 1:
                for i in range(0, self.food  - 1):
                    self.position[i][0], self.position[i][1] = self.position[i + 1]
            self.position[-1][0] = x
            self.position[-1][1] = y

    def do_move(self, action, x, y, game, food):
        move_array = [self.x_change, self.y_change]

        # kiem tra phan thuong va chieu dai
        if self.eaten:
            self.position.append([self.x, self.y])
            self.eaten = False
            self.food = self.food + 1
        # print("direction", self.direction)
        if action == self.direction or ((action + self.direction) == 0):
            # print("____")
            move_array = self.x_change, self.y_change
        elif action == -2 :      # going horizontal
            move_array = [0, - size]                     # up
            self.direction = -2
        elif action == -1:      # going vertical
            move_array = [-size, 0]                    # left
            self.direction = -1
        elif action == 2:      #  going horizontal
            move_array = [0,  size]                    # down
            self.direction = 2
        elif action == 1:      # going vertical
            move_array = [size, 0]                     # rigth
            self.direction = 1

        #update position new
        self.x_change, self.y_change = move_array
        self.x = x + self.x_change
        self.y = y + self.y_change

        # dung tuong
        if self.x < 20 or self.x > game.game_width - 40 or self.y < 20 or \
                self.y > game.game_height - 40 or [self.x, self.y] in self.position:
            game.crash = True

        eat(self, food, game)
        self.update_position(self.x, self.y)

    def draw(self,x,y, food, game):
        self.position[-1][0] = x
        self.position[-1][1] = y
        if game.crash == False:
            # temp = food +2
            for i in range(food):
                x_temp, y_temp = self.position[len(self.position) - 1 - i]
                if(game.display_option):
                    game.gameDisplay.blit(self.image, (x_temp, y_temp))
                else:
                    pygame.gfxdraw.box(game.gameDisplay, (x_temp, y_temp, size, size), green)

            update_screen()
        # else:
            # pygame.time.wait(time_temp/1000.0)

def eat(player, food, game):
    if player.x == food.x and player.y == food.y:
        food.food_coord(game, player)
        player.eaten = True
        game.score = game.score + 1

def update_screen():
    pygame.display.update()

# def get_record(score, record):
#     if score >= record:
#         return score
#     else:
#         return record

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array'], 'video.frames_per_second' : 50}
    time_temp = 100.0
    def __init__(self):
        self.game = Game(width,heigth)
        self.player = self.game.player
        self.food = self.game.food
        # self.apple = Apple(10, 5)
        self.time_temp = 100.0
        self._running = True
        self._display_surf = None

        # self.img = pygame.image.load('snakeBody.png')
        # self.game = Game()
        # self.player = Player(3)
        # self.apple = Apple(10,5)
        
        self.state = None
        self.action_space = spaces.Discrete(4)

    def step(self, action):
        done = self.game.crash
        # self.get_action(action, self.player.direction)
        self.player.do_move(action,self.player.x,self.player.y,self.game, self.food)
        reward = self.get_reward(self.player, self.game.crash)
        ob = self.get_state(self.game, self.player)
        return ob, reward, done ,{}

    # lay gia tri cho trang thai lam thong tin huan luye

    def get_state(self,game, player):
        state = [
            (player.x_change == 20 and player.y_change == 0 and ((list(map(add, player.position[-1], [20, 0])) in player.position) or
            player.position[-1][0] + 20 >= (game.game_width - 20))) or
            (player.x_change == -20 and player.y_change == 0 and ((list(map(add, player.position[-1], [-20, 0])) in player.position) or
            player.position[-1][0] - 20 < 20)) or
            (player.x_change == 0 and player.y_change == -20 and ((list(map(add, player.position[-1], [0, -20])) in player.position) or
            player.position[-1][-1] - 20 < 20)) or
            (player.x_change == 0 and player.y_change == 20 and ((list(map(add, player.position[-1], [0, 20])) in player.position) or
            player.position[-1][-1] + 20 >= (game.game_height-20))),  # danger straight

            (player.x_change == 0 and player.y_change == -20 and ((list(map(add,player.position[-1],[20, 0])) in player.position) or
            player.position[ -1][0] + 20 > (game.game_width-20))) or (player.x_change == 0 and player.y_change == 20 and ((list(map(add,player.position[-1],
            [-20,0])) in player.position) or player.position[-1][0] - 20 < 20)) or (player.x_change == -20 and player.y_change == 0 and ((list(map(
            add,player.position[-1],[0,-20])) in player.position) or player.position[-1][-1] - 20 < 20)) or (player.x_change == 20 and player.y_change == 0 and (
            (list(map(add,player.position[-1],[0,20])) in player.position) or player.position[-1][
             -1] + 20 >= (game.game_height-20))),  # danger right

             (player.x_change == 0 and player.y_change == 20 and ((list(map(add,player.position[-1],[20,0])) in player.position) or
             player.position[-1][0] + 20 > (game.game_width-20))) or (player.x_change == 0 and player.y_change == -20 and ((list(map(
             add, player.position[-1],[-20,0])) in player.position) or player.position[-1][0] - 20 < 20)) or (player.x_change == 20 and player.y_change == 0 and (
            (list(map(add,player.position[-1],[0,-20])) in player.position) or player.position[-1][-1] - 20 < 20)) or (
            player.x_change == -20 and player.y_change == 0 and ((list(map(add,player.position[-1],[0,20])) in player.position) or
            player.position[-1][-1] + 20 >= (game.game_height-20))), #danger left

            self.player.x_change == -size,  # move left
            self.player.x_change == size,  # move right
            self.player.y_change == -size,  # move up
            self.player.y_change == size,  # move down

            self.food.x < self.player.x,  # food left
            self.food.x > self.player.x,  # food right
            self.food.y < self.player.y,  # food up
            self.food.y > self.player.y  # food down
        ]
        for i in range(len(state)):
            if state[i]:
                state[i]=1
            else:
                state[i]=0
        return np.asarray(state)

    def get_reward(self, player,crash):
        self.reward = 0

        # if crash:
        #     self.reward = -1
        #     return self.reward
        if player.eaten:
            self.reward = 1
        return self.reward

    def reset(self):
        self.game = Game(width, heigth)
        self.player = self.game.player
        self.food = self.game.food

        self._running = True
        self._display_surf = None
        self.game.crach = False
        self.game.food =1
        self.state = None


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((width,heigth), pygame.HWSURFACE)
        self._running = True
    def diplay_image(self):
        self.game.display_option = True
    def on_render(self,player, food, game):
        # b_g
        game.gameDisplay.fill((255, 255, 255))
        pygame.gfxdraw.rectangle(game.gameDisplay, (20,20, 400, 400), green)
        # game.gameDisplay.blit(game.bg, (10, 10))

        player.draw(player.position[-1][0],
                              player.position[-1][1],
                              player.food, game)
        food.draw(food.x, food.y, game)
        # display_ui(game, game.score, record)
        # self._display_surf.fill((255,255,255))
        # self.player.draw(self._display_surf,self.img)
        # self.apple.draw(self._display_surf)
        # pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()

    def render(self, mode='human', close=False):
        if self.on_init() == False:
            self._running = False
        pygame.init()

        self.on_render(self.player, self.food, self.game)

        # time.sleep(self.time_temp / 1000.0)
        pygame.event.pump()
        # temp = self.get_reward()


