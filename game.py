from classes import *
import pygame
pygame.init()

clock = pygame.time.Clock()
window = pygame.display.set_mode((1920,1000))


a = Player(vector(500,500),1,(150,200,200),5,500,(100,750),0.001,(200,200,200),0.01,0.1,0.001*5,0.001/2,100,100)

pygame.mouse.set_visible(False)
reset = False
timer = 100
flag = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset = True
        if event.type == pygame.MOUSEBUTTONDOWN:

            flag = True
    if flag == True:
        if timer == 0:
            timer = 100
            flag = False
        else:
            timer -=1

    clock.tick(50)
    window.fill((0,0,0))
    a.PlayerUpdate(window,reset,flag)
    reset = False
    #pygame.draw.circle(window,(50,50,0),pygame.mouse.get_pos(),150,width=1)
    pygame.display.update()
