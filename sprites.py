'''
Created on Aug 19, 2011

@author: Admin
'''

try:
        import sys
        import random
        import math
        import os
        import getopt
        import pygame
        import colors
        import sprites
        import load
        from load import *
        from socket import *
        from pygame.locals import *
except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)

class Player(pygame.sprite.Sprite):
    """The player that is controlled by the arrow key."""
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_img('player.png')
        self.rect.topleft = x, y
        self.safe = True
        self.speed = 10
        self.move = (0,0)
        self.last_move = (0,0)
        # 10p x 10p
        self.size = 10
        
    def moveup(self):
        self.move = (0,-self.speed)
    
    def movedown(self):
        self.move = (0,self.speed)
    
    def moveright(self):
        self.move = (self.speed,0)
    
    def moveleft(self):
        self.move = (-self.speed,0)
        
    def collided(self, x, y):
        if self.rect[0] < 0:
            self.rect[0] = 0
            return True
        elif self.rect[0] > x-self.size:
            self.rect[0] = x-self.size
            return True
        elif self.rect[1] < 0:
            self.rect[1] = 0
            return True
        elif self.rect[1] > y-self.size:
            self.rect[1] = y-self.size
            return True
        else:
            return False
    
    def stop(self):
        self.move = (0, 0)
    
    def update(self):
        self.rect.move_ip(self.move)
    
    def get_loc(self):
        return self.rect.topleft
    
    def set_last_loc(self, x, y):
        self.last_move = (x, y)
    
    def get_last_loc(self):
        return self.last_move
    
    def get_is_safe(self):
        return self.safe
    
class Atom(pygame.sprite.Sprite):
    """Atoms will bounce off the wall. If one hits a player or a wall under
    construction, the player will lose a life."""
    
    def __init__(self, x, y, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_img('atom.png')
        self.rect.topleft = x, y
        self.speed = 8
        self.move = (0, 0)
        # TODO: Make into dictionary
        if dir == 1:
            # Top-right
            self.move = (self.speed, -self.speed)
        elif dir == 2:
            # Bottom-right
            self.move = (self.speed, self.speed)
        elif dir == 3:
            # Bottom-left
            self.move = (-self.speed, self.speed)
        elif dir == 4:
            # Top-left
            self.move = (-self.speed, -self.speed)
        else:
            raise Exception("Incorrect direction int")
        
    def move_vert(self):
        self.rect.move_ip(0, self.move[1])
        
    def move_horiz(self):
        self.rect.move_ip(self.move[0], 0)
        
    def r_vert(self):
        move = list(self.move)
        move[1] = -move[1]
        self.move = tuple(move)
    
    def r_horiz(self):
        move = list(self.move)
        move[0] = -move[0]
        self.move = tuple(move)
        
    def get_loc(self):
        return self.rect.topleft
        
    def update(self):
        pass
    

class Safe(pygame.sprite.Sprite):
    """ Safes are walls that the player can freely move on top of."""
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_img('safe.png')
        self.rect.topleft = x, y
        
    def get_loc(self):
        return self.rect.topleft

class Unsafe(pygame.sprite.Sprite):
    """ Unsafe are walls that the player lays down behind him. Unsafes deduct
    a life upon collision with the player or an Atom. """
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_img('unsafe.png')
        self.rect.topleft = x, y
        
    def equals(self, unsafe):
        return self.get_loc() == unsafe.get_loc()
    
    def get_loc(self):
        return self.rect.topleft
    
class Fill(pygame.sprite.Sprite):
    """ Fills are the "conquered" areas of the game. The Fills are safe to
    the player and contribute to his total points. They cannot be
    traversed."""
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_img('fill.png')
        self.rect.topleft = x, y
        
    def update(self):
        pass