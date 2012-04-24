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
        from sprites import *
        from socket import *
        from pygame.locals import *
except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)

def load_img(name):
    """Load image and return image object"""
    fullname = os.path.join('img', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
            print "Cannot load image:", fullname
            raise SystemExit, message
    return image, image.get_rect()