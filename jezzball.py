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
        self.last_move = (0, 0)
        self.is_safe = False

    def update(self):
        self.last_move = self.rect.topleft
        move = [n * self.speed for n in self.move]
        self.rect.move_ip(move)
        self.rect = self.rect.clamp(SCREENRECT)


class Atom(pygame.sprite.Sprite):
    speed = 8
    images = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.move = (random.choice((-1, 1)), random.choice((-1, 1)))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.__rand_pos()

    def __rand_pos(self):
        x = random.randint(0, SCREENRECT.width - self.rect.width)
        y = random.randint(0, SCREENRECT.width - self.rect.height)
        return (x, y)

    def update(self):
        move = [n * self.speed for n in self.move]
        self.rect.move_ip(move)


class SafeWall(pygame.sprite.Sprite):
    images = []

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        pass


class UnsafeWall(pygame.sprite.Sprite):
    images = []

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        pass

def main():
    pygame.init()
    
    # Display 
    winstyle = 0
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle)

    # Load images and assign to Sprite class
    Player.images = [load_image('player.png')]
    Atom.images = [load_image('atom.png')]
    SafeWall.images = [load_image('safe.png')]
    UnsafeWall.images = [load_image('unsafe.png')]

    # Create background
    background = pygame.Surface(SCREENRECT.size)
    background.fill(Color('black'))

    # Initialize Groups
    atoms = pygame.sprite.Group()
    safewalls = pygame.sprite.Group()
    unsafewalls = pygame.sprite.Group()
    inactive = pygame.sprite.RenderUpdates()
    active = pygame.sprite.RenderUpdates()

    # Assign default groups to each Sprite class
    Atom.containers = atoms, active
    SafeWall.containers = safewalls, inactive
    UnsafeWall.containers = unsafewalls, inactive
    Player.containers = active

    # Starting values
    clock = pygame.time.Clock()

    # Initialize starting Sprites
    player = Player()
    Atom()
    for x in xrange(0, SCREENRECT.width, 10):
        SafeWall((x, 0))
        SafeWall((x, SCREENRECT.height- 10))
    for y in xrange(0, SCREENRECT.height, 10):
        SafeWall((0, y))
        SafeWall((SCREENRECT.width - 10, y))

    while player.alive():
        # User input -- quitting
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
        # Input
        keystate = pygame.key.get_pressed()

        # Clear last drawn sprites
        inactive.clear(screen, background)
        active.clear(screen, background)

        # Update sprites
        active.update()

        # Handle user input
        x_dir = keystate[K_RIGHT] - keystate[K_LEFT]
        y_dir = keystate[K_DOWN] - keystate[K_UP]
        if x_dir or y_dir:
            player.move = (x_dir, y_dir)

        if not player.is_safe and player.rect.topleft != player.last_move:
            UnsafeWall(player.last_move)

        if pygame.sprite.spritecollideany(player, safewalls):
            for wall in unsafewalls:
                SafeWall(wall.rect.topleft)
                wall.kill()

        for atom in pygame.sprite.groupcollide(atoms, safewalls, 0, 0):
            # TODO: Correct Atom bouncing
            
            atom.move = [-n for n in atom.move] 

        # Draw scene
        dirty = inactive.draw(screen)
        pygame.display.update(dirty)
        dirty = active.draw(screen)
        pygame.display.update(dirty)

        # Frame rate
        clock.tick(40)

    pygame.quit()

if __name__ == "__main__":
    main()