import pymunk
import pygame
from elements import Environment
import random

import firebase_admin
from firebase_admin import db

cred_object = firebase_admin.credentials.Certificate('....json')
default_app = firebase_admin.initialize_app(cred_object, {
	"databaseURL":'enter url'
	})

ref = db.reference("/")

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
space = pymunk.Space()

env = Environment(space,screen)

done = False
while not done:
    data = ref.get()
    x = data['h_val']
    y = data['v_val']
    env.step(x,y)
    screen.fill((50,50,50))
    env.draw_env()
    space.step(1/50)
    pygame.display.update()
    clock.tick(120)
    
