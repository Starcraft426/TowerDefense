import pygame
import pytmx
import pyscroll

from enemy import Enemy
from tower import Tower


class Game:
    def __init__(self):
        # initialisation de l'espace de jeu
        self.screen = pygame.display.set_mode((1088, 512))
        pygame.display.set_caption("Tower defense")

        # création de la page d'accueil
        homepage_tmx = pytmx.util_pygame.load_pygame("assets/tmx/homepage.tmx")
        homepage_data = pyscroll.data.TiledMapData(homepage_tmx)
        homepage_layer = pyscroll.orthographic.BufferedRenderer(homepage_data, self.screen.get_size())
        self.homepage = pyscroll.PyscrollGroup(map_layer=homepage_layer, default_layer=1)

        # données de la carte initialisés après le choix de carte
        self.map_group = None
        self.collid1 = []
        self.collid2 = []
        self.collid3 = []
        self.collid4 = []
        self.towerless = []
        self.spawn_coord = None
        self.end_rect = None

        # création de la police des varibles in-game
        self.varfont = pygame.font.SysFont("Comic Sans MS Normal", 25)
        self.wavefont = pygame.font.SysFont("Comic Sans MS Normal", 35)
        self.pausefont = pygame.font.SysFont("Comic Sans MS Normal", 50)

        # création du bouton jouer
        self.play_button = pygame.image.load("assets/png/playbutton.png")
        self.quit_button = pygame.image.load("assets/png/quitbutton.png")

        # création des tours du menu
        self.towerbutton1 = pygame.image.load("assets/png/firemage.png")
        self.towerbutton2 = pygame.image.load("assets/png/watermage.png")
        self.towerbutton3 = pygame.image.load("assets/png/plantmage.png")
        self.towerbutton4 = pygame.image.load("assets/png/electricmage.png")

        # création des minimaps, des cadres
        self.minimaps = [pygame.image.load(f"assets/png/minimaps/{n + 1}.png") for n in range(6)]
        self.frames = [pygame.image.load(f"assets/png/frame{n + 1}.png") for n in range(3)]

        # création des différents sprites du jeu
        self.menubar = pygame.image.load("assets/png/menubar.png")
        self.start = pygame.image.load("assets/png/play2.png")
        self.pausebutton = pygame.image.load("assets/png/pause.png")
        self.waitstart = pygame.image.load("assets/png/play.png")
        self.icone_coeur = pygame.image.load("assets/png/coeur.png")
        self.icone_piece = pygame.image.load("assets/png/piece.png")
        self.pauseframe = pygame.image.load("assets/png/pauseframe.png")
        self.fast1 = pygame.image.load("assets/png/fast0.png")
        self.fast2 = pygame.image.load("assets/png/fast1.png")
        self.fast3 = pygame.image.load("assets/png/fast2.png")
        self.fastbutton = self.fast1

        # création de l'orloge du jeu, qui va permettre de fixer le nombre d'images par secondes
        self.clock = pygame.time.Clock()

        # création des variables principales du jeu
        self.vague = 0
        self.vies = 150
        self.argent = 650
        # organisation d'une vague (<niveau>, <nombre>, <délai>, <envoyer apres>)
        self.vagues = {
            1: [[1, 5, 2, 0]],
            2: [[1, 10, 1.5, 0]],
            3: [[1, 10, 1.5, 0], [1, 10, 0.5, 7.5]],
            4: [[1, 15, 1, 0], [1, 15, 0.5, 15], [2, 1, 1, 15]],
            5: [[1, 20, 0.5, 0]],
            6: [[1, 10, 1, 0], [2, 3, 2, 10]],
            7: [[1, 10, 1, 0], [1, 10, 0.5, 5], [2, 5, 1, 15]],
            8: [[1, 20, 1, 0], [2, 5, 1, 10], [1, 20, 0.5, 5], [3, 2, 3, 25]],
            9: [[1, 10, 0.5, 0], [2, 7, 1, 3], [3, 4, 2, 7]],
            10: [[2, 5, 1, 2], [2, 5, 0.5, 7], [3, 3, 1, 7]],
            11: [[2, 8, 1, 0], [4, 1, 1, 10]],
            12: [[2, 25, 0.5, 0]],
            13: [[3, 5, 1, 0], [4, 3, 1, 6], [5, 1, 1, 7]],
            14: [[5, 5, 2, 0]],
            15: [[3, 10, 0.5, 0], [4, 10, 1, 0], [5, 3, 1, 3]],
            16: [[5, 10, 2, 0], [6, 3, 2, 5]],
            17: [[4, 10, 0.5, 0], [3, 15, 1, 0], [5, 10, 1, 0], [6, 5, 2, 5]],
            18: [[1, 20, 0.5, 0], [2, 20, 0.5, 7.5], [3, 20, 0.5, 15], [4, 20, 0.5, 22.5], [5, 10, 0.5, 30]],
            19: [[1, 1, 1, 0], [6, 20, 1, 10]],
            20: [[5, 20, 0.5, 0], [6, 20, 0.5, 5]]
        }
        self.frame_rate = 60
        self.tick = 0
        self.wave_tick = 0
        self.wave_second = 0
        self.alive_robots = 0
        self.max_alive_robots = 0
        self.is_spawning = False
        self.spawned_robots = 0
        self.onlpacingtower = 0
        self.towernotassigned = None
        self.letspawn = False
        self.pause = False
        self.spawn_ended = 0
        self.towermenu = None
        self.speed = 1
        self.spawnspeed = 1
        self.displaycost = (0, (0, 0))

        # création du groupe d'ennemis et des tours
        self.all_enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.menu = pygame.sprite.Group()

        # lancement du jeu
        self.run()

    def startpage(self):
        # ajout du bouton jouer sur l'ecran
        self.homepage.draw(self.screen)
        self.screen.blit(self.play_button, (449, 169))
        self.screen.blit(self.quit_button, (449, 289))

        # attente d'une entrée de type bouton de souris sur le bouton play pour lancer le jeu
        broken = False
        mousereleased = True
        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 449 < x < 649 and 169 < y < 244:
                        broken = True
                    if 449 < x < 649 and 289 < y < 364:
                        pygame.quit()
                        return 0
                    mousereleased = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    return 0
                elif event.type == pygame.MOUSEBUTTONUP:
                    mousereleased = True
            if broken and mousereleased:
                break
        self.choosemap()

    def choosemap(self):
        a, b, x, y = 0, 0, 0, 0
        mousereleased = False

        while True:
            self.homepage.draw(self.screen)
            for c in range(6):
                x1, y1 = (224 * (c % 3) + 30 * (c % 3) + 178, 113 + 128 * (c % 2) + 30 * (c % 2))
                self.screen.blit(self.frames[(c % 3)], (x1 - 2, y1 - 4))
                self.screen.blit(self.minimaps[c], (x1, y1))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 113 < y < 241:
                        b = 0
                    elif 271 < y < 346:
                        b = 1
                    else:
                        b = -1
                    if 178 < x < 402:
                        a = 1
                    elif 432 < x < 656:
                        a = 3
                    elif 686 < x < 910:
                        a = 5
                    else:
                        a = 0
                    mousereleased = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    mousereleased = True
            if a != 0 and b != -1 and mousereleased:
                break
        # initialisation de la carte et de ses données
        tmx_data = pytmx.util_pygame.load_pygame(f"assets/tmx/map{a + b}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        for obj in tmx_data.objects:
            if obj.type == "1":
                self.collid1.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "2":
                self.collid2.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "3":
                self.collid3.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "4":
                self.collid4.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "towerless":
                self.towerless.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            # récupération des coordonnées de spawn des robots
            spawn = tmx_data.get_object_by_name("spawn")
            self.spawn_coord = (spawn.x, spawn.y)
            end = tmx_data.get_object_by_name("end")
            self.end_rect = [pygame.Rect(end.x, end.y, end.width, end.height)]
        self.towerless.append(
            pygame.Rect(896, 0, self.menubar.get_rect().width, self.menubar.get_rect().height))
        self.game()

    def game(self):
        # script principal du jeu
        while True:
            # fixage du nombre d'images par secondes
            self.clock.tick(self.frame_rate)

            # mise a jour des ennemis et des tours
            if not self.pause:
                for enemy in self.all_enemies:
                    if enemy.hitbox.collidelist(self.collid1) > -1:
                        enemy.orientation = 1
                        enemy.orient = 1
                    elif enemy.hitbox.collidelist(self.collid2) > -1:
                        enemy.orientation = 2
                    elif enemy.hitbox.collidelist(self.collid3) > -1:
                        enemy.orientation = 3
                        enemy.orient = 2
                    elif enemy.hitbox.collidelist(self.collid4) > -1:
                        enemy.orientation = 4
                    if enemy.hitbox.collidelist(self.end_rect) > -1:
                        self.vies -= enemy.vie
                        enemy.vie = 0
                    enemy.tick()
                for tower in self.towers:
                    tower.tick()
                for projectile in self.projectiles:
                    projectile.tick()

            # dessin de la carte, des ennemis et des tours
            self.map_group.draw(self.screen)
            self.all_enemies.draw(self.screen)
            self.towers.draw(self.screen)
            self.projectiles.draw(self.screen)

            # dessin du menu et des boutons
            self.screen.blit(self.menubar, (896, 0))
            if self.pause:
                self.screen.blit(self.waitstart, (960, 420))
                self.screen.blit(self.pauseframe, (200, 100))
                self.screen.blit(self.pausefont.render("Jeu mis en pause", True, (0, 0, 0)), (300, 225))
            elif self.letspawn:
                self.screen.blit(self.pausebutton, (960, 420))
            else:
                self.screen.blit(self.start, (960, 420))
            self.screen.blit(self.icone_coeur, (910, 10))
            self.screen.blit(self.varfont.render(f"{self.vies}", True, (0, 0, 0)), (930, 11))
            self.screen.blit(self.icone_piece, (910, 35))
            self.screen.blit(self.varfont.render(f"{self.argent}", True, (0, 0, 0)), (930, 36))
            self.screen.blit(self.towerbutton1, (920, 100))
            self.screen.blit(self.towerbutton2, (1004, 100))
            self.screen.blit(self.towerbutton3, (920, 184))
            self.screen.blit(self.towerbutton4, (1004, 184))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(920, 100, 64, 64), 2)
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(1004, 100, 64, 64), 2)
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(920, 184, 64, 64), 2)
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(1004, 184, 64, 64), 2)
            self.screen.blit(self.wavefont.render("Vague:", True, (0, 0, 0)), (985, 15))
            self.screen.blit(self.wavefont.render(f"{self.vague}/20", True, (0, 0, 0)), (1000, 45))
            if self.speed == 1:
                self.fastbutton = self.fast1
            elif self.speed == 2:
                self.fastbutton = self.fast2
            else:
                self.fastbutton = self.fast3
            self.screen.blit(self.fastbutton, (800, 10))

            # vérification du nombre de robots vivants
            try:
                if not self.alive_robots and self.spawn_ended == len(self.vagues[self.vague]):
                    self.letspawn = False
            except KeyError:
                pass

            # lecture des entrées
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.onlpacingtower:
                        if pygame.Rect(920, 100, self.towerbutton1.get_rect().width, self.towerbutton1.get_rect() \
                                .height).collidepoint(event.pos) and self.argent > 250:
                            self.towers.add(Tower(event.pos, "fire", self))
                            self.onlpacingtower = True
                        elif pygame.Rect(1004, 100, self.towerbutton2.get_rect().width, self.towerbutton2.get_rect() \
                                .height).collidepoint(event.pos) and self.argent > 400:
                            self.towers.add(Tower(event.pos, "water", self))
                            self.onlpacingtower = True
                        elif pygame.Rect(920, 184, self.towerbutton2.get_rect().width, self.towerbutton2.get_rect() \
                                .height).collidepoint(event.pos) and self.argent > 500:
                            self.towers.add(Tower(event.pos, "plant", self))
                            self.onlpacingtower = True
                        elif pygame.Rect(1004, 184, self.towerbutton2.get_rect().width, self.towerbutton2.get_rect() \
                                .height).collidepoint(event.pos) and self.argent > 350:
                            self.towers.add(Tower(event.pos, "electric", self))
                            self.onlpacingtower = True
                        changedtower = 0
                        for tower in self.towers:
                            if not tower.assigned:
                                self.towernotassigned = tower
                                self.towernotassigned.newpos([a // 32 * 32 for a in event.pos])
                            if tower.rect.collidepoint(event.pos):
                                self.towermenu = tower
                                changedtower = 1
                        if not changedtower:
                            self.towermenu = None
                    elif event.button == 3:
                        self.towernotassigned.kill()
                        self.onlpacingtower = False
                        self.towermenu = None
                    elif event.button == 1 and self.towernotassigned.placefalse is not self.towernotassigned.image:
                        self.towernotassigned.assigned = 1
                        self.towernotassigned.newpos([a // 32 * 32 for a in self.towernotassigned.position])
                        if self.towernotassigned.tower_type == "fire":
                            self.argent -= 250
                        elif self.towernotassigned.tower_type == "water":
                            self.argent -= 400
                        elif self.towernotassigned.tower_type == "plant":
                            self.argent -= 500
                        else:
                            self.argent -= 350
                        self.towernotassigned = None
                        self.onlpacingtower = False

                    if pygame.Rect(960, 420, self.start.get_rect().width, self.start.get_rect().height) \
                            .collidepoint(event.pos):
                        if not self.letspawn:
                            self.letspawn = True
                        else:
                            self.pause = not self.pause

                    if pygame.Rect(800, 10, self.fastbutton.get_rect().width, self.fastbutton.get_rect().height) \
                            .collidepoint(event.pos):
                        self.speed += 1
                        if self.speed > 3:
                            self.speed = 1



                if event.type == pygame.MOUSEMOTION:
                    if self.onlpacingtower:
                        self.towernotassigned.newpos([a // 32 * 32 for a in event.pos])
                    if pygame.Rect(920, 100, 64, 64).collidepoint(event.pos):
                        self.displaycost = (1, event.pos)
                    else:
                        self.displaycost = (0, event.pos)

            if self.displaycost[0] == 1:
                if self.argent < 250:
                    self.screen.blit(self.varfont.render("250", True, (230, 0, 0)), self.displaycost[1])
                else:
                    self.screen.blit(self.varfont.render("250", True, (0, 230, 0)), self.displaycost[1])

            # mise a jour de l'orloge des vagues
            if not self.pause:
                self.wave_tick += 1

            # spawn des monstres
            if self.letspawn:
                if not self.is_spawning and not self.alive_robots:
                    self.is_spawning = True
                    self.vague += 1
                    self.spawn_ended = 0
                    self.wave_tick = 0
                if self.vague == 21:
                    break
                # organisation d'une vague (<niveau>, <nombre>, <délai>, <envoyer apres>)
                elif self.is_spawning:
                    for b in self.vagues[self.vague]:
                        if self.wave_tick > b[3]/self.speed * self.frame_rate and b[1] > 0:
                            if b[-1] is b[3]:
                                b.append(self.wave_tick)
                            if not (self.wave_tick - b[4]) % (b[2]/self.speed * self.frame_rate):
                                self.all_enemies.add(Enemy(self.spawn_coord, b[0], self))
                                b[1] -= 1
                                self.alive_robots += 1
                        if not b[1] and len(b) == 5:
                            self.spawn_ended += 1
                            b.append(0)
                if self.spawn_ended == len(self.vagues[self.vague]):
                    self.is_spawning = False
            self.menu.draw(self.screen)
            if self.towermenu:
                pygame.draw.circle(self.screen, (235, 235, 235), tuple([a + 32 for a in self.towermenu.position]),
                                   self.towermenu.attributs[1] * 32, 5)

            # correction de la vitesse
            for tower in self.towers:
                if tower.currentspeed != self.speed:
                    tower.attributs[2] *= tower.currentspeed / self.speed
                    tower.clock *= tower.currentspeed / self.speed
                    tower.currentspeed = self.speed
            for enemy in self.all_enemies:
                if enemy.currentspeed != self.speed:
                    enemy.clock *= self.speed / enemy.currentspeed
                    enemy.speed *= self.speed / enemy.currentspeed
                    enemy.currentspeed = self.speed
            for projectile in self.projectiles:
                if projectile.currentspeed != self.speed:
                    projectile.lifetime *= projectile.currentspeed/self.speed
                    projectile.clock *= projectile.currentspeed/self.speed

            # mise a jour de l'ecran
            pygame.display.flip()

    def run(self):
        self.startpage()

        pygame.quit()
