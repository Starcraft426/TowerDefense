import pygame
import os
import animation


# définition de la classe ennemy
class Enemy(animation.Animation):
    def __init__(self, coord, force, game):
        super().__init__(force)

        # récupération du jeu pour le nombre de robots cf ligne 39
        self.game = game

        # création des variables du robot
        self.position, self.force = list(coord), force
        if force == 6:
            self.force = 2
        self.speed = 0.5*force
        self.camo = force > 5
        self.vie = self.force
        self.argent = 5*force
        self.clock = 0
        self.orientation = 1
        self.image = pygame.image.load(f"assets/png/autoload/{force}/1/1.png")
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        self.currentspeed = 1
        self.distancewalked = 0

    # animation du robot
    def tick(self):
        self.clock += 1
        if self.clock > (self.game.frame_rate/3)/(self.force+4*self.camo):
            self.animate()
            self.clock = 1
        if self.vie < 1:
            self.game.alive_robots -= 1
            self.game.argent += self.argent
            self.kill()
        self.move()

    # avancée du robot
    def move(self):
        if self.orientation == 1:
            self.position[0] += self.speed
        elif self.orientation == 2:
            self.position[1] -= self.speed
        elif self.orientation == 3:
            self.position[0] -= self.speed
        else:
            self.position[1] += self.speed
        self.distancewalked += self.speed
        self.rect.x, self.rect.y = self.position
        self.hitbox.x, self.hitbox.y = self.position
