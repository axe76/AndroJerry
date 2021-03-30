import pymunk
import pygame
from joodle_dump import Ground, Player, Walls, Platform, Environment
import os 

pygame.init()
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,100)

env = Environment(space,screen)

done = False

def coll_post(arbiter,space,data):
    if arbiter.shapes[1].id == 9 and arbiter.shapes[0].id == 2: 
        space.remove(arbiter.shapes[1].body,arbiter.shapes[1])
        env.platforms.pop()
        env.isplatform = False
    
    if arbiter.shapes[0].id == 9 and arbiter.shapes[1].id == 2: 
        space.remove(arbiter.shapes[0].body,arbiter.shapes[0])
        env.platforms.pop()
        env.isplatform = False


handler = space.add_default_collision_handler()
handler.post_solve = coll_post

bg = pygame.image.load(os.path.join("gallery", "space.jpg"))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x1, y1 = pygame.mouse.get_pos() 
        if event.type == pygame.MOUSEBUTTONUP:
            x2, y2 = pygame.mouse.get_pos() 
            env.add_platform(1,x1,y1,x2,y2)
            env.isplatform = True

    screen.blit(bg, (0,0))
    # screen.fill((50,50,50))
    env.step()
    space.step(1/50)
    pygame.display.update()
    clock.tick(120)