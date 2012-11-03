#!/usr/bin/env python

import os.path

import pygame
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

SCREENRECT = Rect(0, 0, 800, 600)

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'img', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()


def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs


class dummysound:
    def play(self): pass


def load_sound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join(main_dir, 'sound', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()


class Player(pygame.sprite.Sprite):
    speed = 10

    def __init__(self, x, y):
        pygame.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect


class Atom(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.Sprite.__init__(self, self.containers)

class Wall(pygame.sprite.Sprite):
    pass

def main():
    pygame.init()
    
    winstyle = 0
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle)

    Player.images = [load_image('player.png')]
    Atom.images = [load_image('atom.png')]

    background = pygame.Surface(SCREENRECT.size)
    background.fill(Color('black'))

    while 1:
        pass

    pygame.quit()

if __name__ == "__main__":
    main()