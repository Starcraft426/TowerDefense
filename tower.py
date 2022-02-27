from math import sqrt
from projectile import *


class Tower(pygame.sprite.Sprite):
    def __init__(self, coord, tower_type, game):
        self.towers = None
        super().__init__()
        self.game = game
        self.target = None
        self.assigned = 0
        self.position = list(coord)
        self.tower_type = tower_type
        self.inmenu = False
        self.mage = pygame.image.load("assets/png/{}mage.png".format(self.tower_type))
        self.image = self.mage
        self.placetrue = pygame.image.load("assets/png/{}placetrue.png".format(self.tower_type))
        self.placefalse = pygame.image.load("assets/png/{}placefalse.png".format(self.tower_type))
        if tower_type == "fire":
            self.attributs = [2, 2, game.frame_rate*2]
        elif tower_type == "water":
            self.attributs = [2, 5, game.frame_rate*2]
        elif tower_type == "plant":
            self.attributs = [1, 2, game.frame_rate/2]
        elif tower_type == "electric":
            self.attributs = [3, 3, game.frame_rate*3]
        self.rect = self.image.get_rect()
        self.clock = self.attributs[2]
        self.currentspeed = 1

    def newpos(self, pos):
        self.towers = [a for a in self.game.towers if a is not self]
        self.position = pos
        self.rect.x, self.rect.y = pos
        if self.assigned:
            self.image = self.mage
        elif self.rect.collidelist(self.game.towerless) > -1 or self.rect.collidelist(self.towers) > -1:
            self.image = self.placefalse
        else:
            self.image = self.placetrue

    def listmodifier(self, elem):
        return(elem.distancewalked)

    def tick(self):
        enemies = list(self.game.all_enemies)
        enemies.sort(key=self.listmodifier, reverse=True)
        if self.assigned:
            if self.game.alive_robots > 0 and [self.listmodifier(a) for a in self.game.all_enemies]:
                for enemy in enemies:
                    totaldamage = 0
                    if sqrt((enemy.position[0]-self.position[0])**2+(enemy.position[1]-self.position[1])**2) < \
                            (self.attributs[1]+1)*32 and not self.target:
                        for a in [tower.attributs for tower in self.game.towers if tower.target is enemy]:
                            totaldamage += a
                            if totaldamage < enemy.vie:
                                self.target = enemy
                        if not [tower.attributs for tower in self.game.towers if tower.target is enemy]:
                            self.target = enemy

                    if self.target:
                        if self.target.camo and self.tower_type != "plant":
                            self.target = None
                        elif not sqrt((self.target.position[0]-self.position[0])**2+(self.target.position[1] -
                                self.position[1])**2) < (self.attributs[1]+1)*32 or self.target.vie < 1:
                            self.target = None
                        else:
                            self.attack(self.target)
                self.clock += 1
                self.target = None

    def attack(self, target):
        if self.clock >= self.attributs[2]:
            self.game.projectiles.add(Projectile(list(self.target.position), self.tower_type, self.game))
            target.vie -= self.attributs[0]
            self.clock = 0
