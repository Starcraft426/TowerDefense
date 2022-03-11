import pygame
from game import Game
from autoupdate import *

if __name__ == '__main__':
    Updater()
    pygame.init()
    game = Game()
