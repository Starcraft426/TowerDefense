import pygame
import animation
from math import sin, cos, pi


class Projectile(pygame.sprite.Sprite):
    def __init__(self, coords, projectile_type, game):
        super().__init__()
        self.image = pygame.image.load("assets/png/{0}projectile.png".format(projectile_type))
        self.game = game
        self.game.projectiles.add(self)
        self.position = coords
        self.lifetime = 1
        self.clock = 0
        self.rect = self.image.get_rect()
        self.currentspeed = 1
        if projectile_type == "electric":
            self.rect.x, self.rect.y = self.position[0]+12, self.position[1]+8
        else:
            self.rect.x, self.rect.y = self.position[0]+12, self.position[1]+40

    def tick(self):
        self.clock += 1
        if self.clock > self.lifetime*self.game.frame_rate:
            self.kill()
