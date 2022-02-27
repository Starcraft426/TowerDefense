import pygame
import os


class Animation(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.number = number
        self.current_image = 0
        self.orient = 1
        self.image = pygame.image.load(f"assets/png/autoload/{number}/1/1.png")
        self.images = animations[f"{number}"]

    def animate(self):
        if self.images is not None:
            self.current_image += 1
            if self.current_image > len(self.images[self.orient-1]):
                self.current_image = 1
            self.image = self.images[self.orient-1][self.current_image]


def load(file_dir):
    images = dict()
    images2 = []
    os.chdir(file_dir)
    for file in os.listdir():
        os.chdir(file_dir)
        if not file[0] == ".":
            try:
                images2.append(load(f"{os.getcwd()}/{file}"))
            except NotADirectoryError:
                key = int(file.split('.')[0])
                images[key] = pygame.image.load(f"{file_dir}/{file}")
    if not images:
        return images2
    else:
        return images


try:
    animations["1"]
except NameError:
    old_path = os.getcwd()
    animations = dict()
    names = []
    directory = f"{os.getcwd()}/assets/png/autoload/"
    os.chdir(directory)
    for path in os.listdir():
        if not path[0] == ".":
            animations[path] = load(directory+path)
    os.chdir(old_path)
