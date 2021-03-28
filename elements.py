import pymunk
import pygame
import numpy as np 

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

class Environment():
    def __init__(self,space,screen):
        self.space = space
        self.screen = screen
        self.dot = Dot(1,20,space,screen)
    
    def draw_env(self):
        self.dot.draw_dot()

    def step(self,angle_h,angle_v):
        self.dot.circle_body.position = (translate(angle_h,20,-20,0,800),translate(angle_v,20,-20,0,800))


class Dot():
    def __init__(self,mass,radius,space,screen):
        self.mass = mass
        self.radius  = radius
        self.screen = screen
        self.circle_moment = pymunk.moment_for_circle(self.mass,0,self.radius)
        self.circle_body = pymunk.Body(self.mass,self.circle_moment,pymunk.Body.KINEMATIC)
        self.circle_body.position = 400,400
        self.circle_shape = pymunk.Circle(self.circle_body,self.radius)

        space.add(self.circle_body, self.circle_shape)
        
    def draw_dot(self):
        pos_x = int(self.circle_body.position.x)
        pos_y = int(self.circle_body.position.y)
        pygame.draw.circle(self.screen,(0,0,0),(pos_x,pos_y),30)