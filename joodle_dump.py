import pymunk
import pygame
import numpy as np 
import os

class Environment():
    def __init__(self,space,screen):
        self.player = Player(100,30,space,screen)
        self.ground = Ground(1,space,screen)
        self.walls = Walls(1,space,screen)
        self.platforms = []
        self.isplatform = False
        self.done = False
        self.space = space
        self.screen = screen

    def reset(self):
        self.space.remove(self.rock.circle_shape,self.rock.circle_body)
        self.space.remove(self.player.triangle_shape,self.player.triangle_body)
        self.player = Player(100,20,self.space,self.screen)
        self.done = False

    def add_platform(self,mass,x1,y1,x2,y2):
        if not self.isplatform:
            self.platforms.append(Platform(mass,x1,y1,x2,y2,self.space,self.screen))

    def draw_env(self):
        self.player.draw_player()
        self.ground.draw_ground()
        self.walls.draw_walls()
        for platform in self.platforms:
            platform.draw_platform()
        
    def step(self):
        self.draw_env()
        
class Platform():
    def __init__(self,mass,x1,y1,x2,y2,space,screen):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        
        self.mass = mass
        self.screen = screen
        self.segment_moment = pymunk.moment_for_segment(self.mass,(self.x1,self.y1),(self.x2,self.y2),2) #end points and thickness
        self.segment_body = pymunk.Body(self.mass,self.segment_moment,pymunk.Body.STATIC)
        self.segment_body.position = 0,0
        self.segment_shape = pymunk.Segment(self.segment_body,(self.x1,self.y1),(self.x2,self.y2),2)
        self.segment_shape.elasticity = 1
        self.segment_shape.id = 9

        space.add(self.segment_body,self.segment_shape)

    def draw_platform(self):
        pygame.draw.line(self.screen, (0,200,0), (self.x1,self.y1),(self.x2,self.y2),5)

class Player():
    def __init__(self,mass,radius,space,screen):
        self.mass = mass
        self.radius  = radius
        self.elasticity = 1.0
        self.screen = screen
        self.circle_moment = pymunk.moment_for_circle(self.mass,0,self.radius)
        self.circle_body = pymunk.Body(self.mass,self.circle_moment)
        self.circle_body.position = 0,10
        self.circle_shape = pymunk.Circle(self.circle_body,self.radius)
        self.circle_shape.body.velocity = (100,0)
        self.circle_shape.elasticity = self.elasticity
        self.circle_shape.id = 2
        self.img = pygame.transform.scale2x(pygame.image.load(os.path.join("gallery","player.png")))

        space.add(self.circle_body, self.circle_shape)
        
    def draw_player(self):
        pos_x = int(self.circle_body.position.x)
        pos_y = int(self.circle_body.position.y)
        # pygame.draw.circle(self.screen,(0,0,0),(pos_x,pos_y),30)
        self.screen.blit(self.img,(pos_x-60,pos_y-80))

class Ground():
    def __init__(self,mass,space,screen):
        self.mass = mass
        self.screen = screen
        self.segment_moment = pymunk.moment_for_segment(self.mass,(0,750),(1000,750),2) #end points and thickness
        self.segment_body = pymunk.Body(self.mass,self.segment_moment,pymunk.Body.STATIC)
        self.segment_body.position = 0,0
        self.segment_shape = pymunk.Segment(self.segment_body,(0,750),(1000,750),2)
        self.segment_shape.elasticity = 1
        self.segment_shape.id = 4

        space.add(self.segment_body,self.segment_shape)

    def draw_ground(self):
        pygame.draw.rect(self.screen, (0,0,200), pygame.Rect(0, 750, 1000, 0),2)

class Walls():
    def __init__(self,mass,space,screen):
        self.mass = mass
        self.screen = screen
        self.segment1_moment = pymunk.moment_for_segment(mass,(0,0),(0,800),2) #end points and thickness
        self.segment1_body = pymunk.Body(self.mass,self.segment1_moment,pymunk.Body.STATIC)
        self.segment1_body.position = 0,0
        self.segment1_shape = pymunk.Segment(self.segment1_body,(0,0),(0,800),2)
        self.segment1_shape.elasticity = 1
        self.segment2_moment = pymunk.moment_for_segment(self.mass,(1000,0),(1000,800),2) #end points and thickness
        self.segment2_body = pymunk.Body(self.mass,self.segment2_moment,pymunk.Body.STATIC)
        self.segment2_body.position = 0,0
        self.segment2_shape = pymunk.Segment(self.segment2_body,(1000,0),(1000,800),2)
        self.segment2_shape.elasticity = 1
        self.segment1_shape.id = 5
        self.segment2_shape.id = 6

        space.add(self.segment1_body,self.segment1_shape,self.segment2_body,self.segment2_shape)

    def draw_walls(self):
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(0, 0, 0, 800),2)
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(1000, 0, 0, 800),2)
