'''
Created on Aug 4, 2011

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

SIZE = 10

class JezzBall:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        # Initialize sprite groups
        self.playersprite = pygame.sprite.RenderPlain()
        self.safe_group = pygame.sprite.RenderPlain()
        self.unsafe_group = pygame.sprite.RenderPlain()
        self.atom_group = pygame.sprite.RenderPlain()
        self.fill_group = pygame.sprite.RenderPlain()
        
        # Score track
        self.level = 1
        self.score = 0
        
    def place_safes(self):
        """
        Puts the initial Safe walls in place.
        """
        # Top wall
        for x in range(0, self.width, SIZE):
            y = 0
            new_safe = Safe(x,y)
            self.safe_group.add(new_safe)
        # Bottom wall
        for x in range(0, self.width, SIZE):
            y = self.height-SIZE
            new_safe = Safe(x,y)
            self.safe_group.add(new_safe)
        # Left wall
        for y in range(10, self.height-SIZE, SIZE):
            x = 0
            new_safe = Safe(x,y)
            self.safe_group.add(new_safe)
        # Right wall
        for y in range(10, self.height-SIZE, SIZE):
            x = self.width-SIZE
            new_safe = Safe(x,y)
            self.safe_group.add(new_safe)
            
    def get_adj_loc(self, x, y, dir):
        """
        Returns an adjacent location. Direction in degrees, with 0 facing up.
        """
        if dir == 0:
            return (x, y-SIZE)
        elif dir == 90:
            return (x+SIZE, y)
        elif dir == 180:
            return (x, y+SIZE)
        elif dir == 270:
            return (x-SIZE, y)
    
    def remove_around(self, (x, y)):
        sprite_at_loc = pygame.sprite.LayeredUpdates.get_sprites_at(self, (x,y))[0]
        if (sprite_at_loc is not Safe and sprite_at_loc is not Player and 
            sprite_at_loc is not Atom):
            if sprite_at_loc is Fill:
                sprite_at_loc.kill()

            sprite = pygame.Sprite.LayeredUpdates
            up = self.get_adj_loc(x, y, 0)
            if sprite.get_sprites_at(up) is not Atom:
                self.remove_around(up)
            right = self.get_adj_loc(x, y, 90)
            if sprite.get_sprites_at(right) is not Atom:
                self.remove_around(right)
            down = self.get_adj_loc(x, y, 180)
            if sprite.get_sprites_at(down) is not Atom:
                self.remove_around(down)
            left = self.get_adj_loc(x, y, 270)     
            if sprite.get_sprites_at(left) is not Atom:
                self.remove_around(left)       
    
    def main(self):
        pygame.display.set_caption("JezzBall")
        
        # Background
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(colors.BLACK)
        
        # Blit screen
        self.screen.blit(background, (0, 0))
        pygame.display.flip()
        
        # Initialize player
        player = Player(self.width/2 - 10, 0)
        player.set_last_loc(player.get_loc()[0], player.get_loc()[1])
        self.playersprite.add(player)
        
        # Initialize atom(s)
        x = random.randrange(10, self.width-10, 10)
        y = random.randrange(10, self.height-10, 10)
        print x, y
        dir = random.randint(1, 4)
        atom = Atom(300, 200, 1) ### TODO: randomize
        self.atom_group.add(atom)
        
        # Place safes
        self.place_safes()
        
        # Caching fills
        '''
        fill_set = set()
        for x in range(0, self.width, SIZE):
            for y in range(0, self.height, SIZE):
                new_fill = Fill(x, y)
                fill_set.add(new_fill)
        '''
        # Initialize clock
        clock = pygame.time.Clock()
        
        while 1:
            clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            
            # Handles player movement
            pygame.event.pump()
            key = pygame.key.get_pressed()
            if key[K_UP] or key[K_w]:
                player.moveup()
            if key[K_DOWN] or key[K_s]:
                player.movedown()       
            if key[K_RIGHT] or key[K_d]:
                player.moveright()      
            if key[K_LEFT] or key[K_a]:
                player.moveleft()
                
            # Player collision test
            if player.collided(self.width, self.height):
                player.stop()
                
            # Atom movement and collision test
            for i in self.atom_group.sprites():
                i.move_vert()
                collided = pygame.sprite.spritecollide(i, self.safe_group, False)
                if len(collided) > 0:
                    i.r_vert()
                    i.move_vert()
                i.move_horiz()
                collided = pygame.sprite.spritecollide(i, self.safe_group, False)
                if len(collided) > 0:
                    i.r_horiz()
                    i.move_horiz()
                
            """
            # Collision debugging printing
            li = pygame.sprite.spritecollide(player, self.unsafe_group, False)
            coll = 0
            for i  in li:
                coll = i.get_loc()
            # print "Player: ", player.get_loc(), " Collision: ", coll
            """
            
            # Unsafes laid down behind player
            new_unsafe = Unsafe(player.get_loc()[0], player.get_loc()[1])
            # Creates unsafe if the current player loc is not at prev loc
            will_add = not player.get_last_loc() == player.get_loc()
            for i in self.unsafe_group.sprites():
                if new_unsafe.get_loc() == i.get_loc():
                    will_add = False
                    break
            if will_add:
                self.unsafe_group.add(new_unsafe)
            player.set_last_loc(player.get_loc()[0], player.get_loc()[1])
            
            
            # Unsafes to safes after player collides with safe
            if (len(pygame.sprite.spritecollide(player, self.safe_group, False)) > 0 \
                and len(self.unsafe_group) > 0):
                for i in self.unsafe_group.sprites():
                    new_safe = Safe(i.get_loc()[0], i.get_loc()[1])
                    self.safe_group.add(new_safe)
                self.unsafe_group.empty()
                self.fill_group.empty()
                
            # Fill boxed area
            
            
            
            """
            for i in fill_set:
                self.fill_group.add(i)
            """
                
            """
            for i in self.atom_group:
                self.remove_around(i.get_loc())
            """               
            
            # Updates
            self.playersprite.update()
            self.atom_group.update()
            self.screen.blit(background, (0, 0))
            self.fill_group.draw(self.screen)
            self.safe_group.draw(self.screen)
            self.unsafe_group.draw(self.screen)
            self.playersprite.draw(self.screen)
            self.atom_group.draw(self.screen)
            pygame.display.flip()
            
    def play(self):
        pass