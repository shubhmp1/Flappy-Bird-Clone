import pygame
import os
import random
import time

pygame.init()

WIDTH = 600
HEIGHT = 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE= (244,220,180)
CREAM = (180,140,100)
BLACK = (0, 0, 0)

FPS = 60

pygame.font.init()
FONT1 = pygame.font.SysFont("Times New Roman", 100)
FONT2 = pygame.font.SysFont("Times New Roman", 50)



FLAPPY_BIRD_NEUTRAL_IMAGE = pygame.image.load(os.path.join('assets','flappybirdneutral.png'))
#resizes flappy bird image
FLAPPY_BIRD_NEUTRAL_IMAGE = pygame.transform.scale(FLAPPY_BIRD_NEUTRAL_IMAGE, (75, ((125*75)/175)))

PIPE_TOP_IMAGE = pygame.image.load(os.path.join('assets','toppipepart.png'))
PIPE_BOTTEM_IMAGE = pygame.image.load(os.path.join('assets','bottempipepart.png'))
#resizes the pipe images
PIPE_TOP_IMAGE = pygame.transform.scale(PIPE_TOP_IMAGE, (113,((120*113)/250)))
PIPE_BOTTEM_IMAGE = pygame.transform.scale(PIPE_BOTTEM_IMAGE, (104, ((1500*104)/230)))


def draw_window(dimensions,pipes,points,gameOver):

    #value that is the space between the two pipes
    betweenPipe = 280

    WIN.fill(WHITE)
    WIN.blit(FLAPPY_BIRD_NEUTRAL_IMAGE,(dimensions[0],dimensions[1]))

    #will go through all the pipes in the pipes list and put them onto the screen based on the middle rectangle they are accustomend to
    for pipe in pipes:
        #puts the top pipe, and flips around
        #put the top part of the top pipe in the right location
        WIN.blit(pygame.transform.flip((pygame.transform.rotate(PIPE_TOP_IMAGE, 180)), True, False),(pipe[0],pipe[1]))
        #puts the bottem part of the pipe right in the center and above the top pipe
        WIN.blit(pygame.transform.flip((pygame.transform.rotate(PIPE_BOTTEM_IMAGE, 180)), True, False),(pipe[0]+4.5,pipe[1]-((1500*104)/230)))

        #puts the bottem pipe
        #put the top part of the bottem pipe in the right location
        WIN.blit(PIPE_TOP_IMAGE,(pipe[0],pipe[1]+betweenPipe))
        #puts the bottem part of the pipe right in the center and above the bottem pipe
        WIN.blit(PIPE_BOTTEM_IMAGE,(pipe[0]+4.5,pipe[1]+54.24+betweenPipe))
    
    point_surface = FONT1.render(str(points), True, BLACK)
    WIN.blit(point_surface, ((600-point_surface.get_rect().width)/2,50))

    #checks wether the game is over and if it is then the gameover screen shows up
    if gameOver == True:
        
        #draws rectangle in middle of screen
        pygame.draw.rect(WIN, CREAM, pygame.Rect(150,150,300,500))

        #draws score, and then the score underneath it
        score_surface = FONT2.render("SCORE", True, BLACK)
        WIN.blit(score_surface, ((600-score_surface.get_rect().width)/2,250))

        #draws score, and then the score underneath it
        score_surface = FONT1.render(str(points), True, BLACK)
        WIN.blit(score_surface, ((600-score_surface.get_rect().width)/2,300))



    pygame.display.update()



run = True
clock = pygame.time.Clock()

#the default locaiton of the bird
bird_x = 210
bird_y = 350

#starting speed
bird_speed = 0

#value to see if jumped
jumped = False
#counter to count the amount of times the speed is increased by after jump
counter = 0

#value that tracks how long the bird slow falls for before fast falling
slowfall = 0

#value for the pipes being tracked, two things it will have, the top left y of the rectangle that sits in between the two pipes and the  direction of that rectangle in 
pipes = []

#value the tracks how much time until a new pipe has to be added
timer = 60

#value to show how many points I have accumulated
points = 0

#value that checks if the game is still going
gameOver = False


while run:
    clock.tick(FPS)

    #checks if is the correct time to add the pipes,
    if timer == 60:
        #will add a pipe with random height inbetween 50 and 422, and starting x value at 600 being right outside of the map, and if the bird has gone through that specific pipe
        pipes.append([600,random.randint(50,422),False])

        #checks if there are three pipes in the list, if there are now, will remove the first one in the list, the one that is now off screen
        if len(pipes) == 3:
            pipes.pop(0)

        #resets this value
        timer = 0


    #changes location of bird
    draw_window([bird_x,bird_y+bird_speed],pipes,points,gameOver)

    #will do this while the game is not over
    if gameOver == False:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #checks if space bar is pressed, and if it is then the game will give it a predetermined upward speed
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.K_SPACE:
                jumped = True
                #resets the slowfall back to 0
                slowfall = 0


        #increases the speed upwards of the flappy bird, 6 times, then sets it back to gradually decreasing at a normal pace
        #JUMPING
        if jumped == True:
            if counter == 6:
                jumped = False
                counter = 0
            elif counter < 6:
                bird_speed = bird_speed - 25 
                counter = counter + 1

        #if the mouse button is not pressed
        #changes speed naturally to make the bird go down the fast pased version of the fall, when space is not pressed
        #FALLING
        elif jumped == False:
            
            #FAST FALL
            if slowfall == 20:
                bird_speed = bird_speed + 11

            #SLOW FALL
            elif slowfall < 20:
                bird_speed = bird_speed + 6
                slowfall = slowfall + 1 

        #increments the timer value
        timer = timer + 1
        #187 pixel space between the two pipes on screen
        #will cycle through all the pipes and will increment the x value so that it would get out of the screen with only 2 pipes on screen
        
        for i in range(len(pipes)):
            pipes[i][0] = pipes[i][0] - 6.23
            
        
        #will also check if the bird if the bird is in between the current pipe, and if it is the points will increase
        #checks if the birds x value is between the two sides of the inside of the pipes, and if the y value is between the pipes  
        if bird_x+75 >= pipes[0][0] and bird_x <= pipes[0][0] + 113 and bird_y+bird_speed-54 >= pipes[0][1]and bird_y+bird_speed+54 <= pipes[0][1] + 280 and pipes[0][2] == False:
            points = points + 1
            pipes[0][2] = True
        #checks if you hit the pipe, collision tester
        elif bird_x+75 >= pipes[0][0] and bird_x <= pipes[0][0] + 113 and (bird_y+bird_speed <= pipes[0][1] or bird_y+bird_speed+54 >= pipes[0][1] + 280):
            gameOver = True
            
    



pygame.quit()