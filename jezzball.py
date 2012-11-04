#!/usr/bin/env python

import os.path
import random
import pygame
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

SCREENRECT = Rect(0, 0, 800, 500)

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
    images = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midtop=SCREENRECT.midtop)
        self.move = (0, 0)

    def update(self):
        move = [n * self.speed for n in self.move]
        self.rect.move_ip(move)


class Atom(pygame.sprite.Sprite):
    speed = 8
    images = []

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.move = (random.choice(-1, 1), random.choice(-1, 1))

    def update(self):
        move = [n * self.speed for n in self.move]
        self.rect.move_ip(move)


class SafeWall(pygame.sprite.Sprite):
    pass


class UnsafeWall(pygame.sprite.Sprite):
    pass


def main():
    pygame.init()
    
    # Display 
    winstyle = 0
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle)

    # Load images and assign to Sprite class
    Player.images = [load_image('player.png')]
    Atom.images = [load_image('atom.png')]

    # Create background
    background = pygame.Surface(SCREENRECT.size)
    background.fill(Color('black'))

    # Initialize Groups
    atoms = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()

    # Assign default groups to each Sprite class
    Player.containers = all
    Atom.containers = atoms, all

    # Starting values
    clock = pygame.time.Clock()

    # Initialize starting Sprites
    player = Player()

    while 1:
        # Input
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
        keystate = pygame.key.get_pressed()

        # Clear last drawn sprites
        all.clear(screen, background)

        # Update sprites
        all.update()

        # Handle player input
        x_dir = keystate[K_RIGHT] - keystate[K_LEFT]
        y_dir = keystate[K_DOWN] - keystate[K_UP]
        if x_dir or y_dir:
            player.move = (x_dir, y_dir)

        # Draw scene
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        # Frame rate
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()