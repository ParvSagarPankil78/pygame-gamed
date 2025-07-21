import pygame as pg
import random

#initialize pygame
pg.init()

#set display surface
win_width=800
win_height=600
display_surface=pg.display.set_mode((win_width,win_height))
pg.display.set_caption('Burger Dog')

#set fps and clock
fps=60
clock=pg.time.Clock()

#set game values
player_starting_lives=3
player_normal_velocity=5

player_boost_velocity=10
starting_boost_level=100

starting_burger_velocity=3
burger_acceleration=.5

score=0
burger_points=0
burgers_eaten=0

player_lives=player_starting_lives
player_velocity=player_normal_velocity

boost_level=starting_boost_level

burger_velocity=starting_burger_velocity

buffer_distance=100

#set colors
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
yellow=(255,255,0)
cyan=(0,255,255)
magenta=(255,0,255)
orange=(246,170,54)

#set fonts
font=pg.font.SysFont('monotypecorsiva',30)

#set text
points_text=font.render('Burger Points: '+str(burger_points),True,orange)
points_rect=points_text.get_rect()
points_rect.topleft=(10,10)

score_text=font.render('Score: '+str(score),True,orange)
score_rect=score_text.get_rect()
score_rect.topleft=(10,50)

title_text=font.render('Burger Dog',True,magenta)
title_rect=title_text.get_rect()
title_rect.centerx=win_width//2
title_rect.y=10

eaten_text=font.render('Burgers Eaten: '+str(burgers_eaten),True,orange)
eaten_rect=eaten_text.get_rect()
eaten_rect.centerx=win_width//2
eaten_rect.y=50

lives_text=font.render('Lives: '+str(player_lives),True,orange)
lives_rect=lives_text.get_rect()
lives_rect.topright=(win_width-10,10)

boost_text=font.render('Boost: '+str(boost_level),True,orange)
boost_rect=boost_text.get_rect()
boost_rect.topright=(win_width-10,50)

game_over_text=font.render('Final Score: '+str(score),True,orange)
game_over_rect=game_over_text.get_rect()
game_over_rect.center=(win_width//2,win_height//2)

continue_text=font.render('Press any key to play again',True,orange)
continue_rect=continue_text.get_rect()
continue_rect.center=(win_width//2,win_height//2+64)

#set sounds and music
bark_sound=pg.mixer.Sound('catch.wav')
miss_sound=pg.mixer.Sound('miss.wav')
pg.mixer.music.load('bgmusic.wav')

#set images
player_image_right=pg.image.load('dog right.png')
player_image_left=pg.image.load('dog left.png')
player_image=player_image_left

player_rect=player_image.get_rect()
player_rect.centerx=win_width//2
player_rect.bottom=win_height


burger_image=pg.image.load('burger.png')
burger_rect=burger_image.get_rect()
burger_rect.topleft=(random.randint(0,win_width-32),-buffer_distance)


#main
pg.mixer.music.play(-1,0,0)
running=True
while running:
    #check if user want to quit
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=False

    #move the player
    keys=pg.key.get_pressed()
    if keys[pg.K_LEFT] and player_rect.left>0:
        player_rect.x-=player_velocity
        player_image=player_image_left
    if keys[pg.K_RIGHT] and player_rect.right<win_width:
        player_rect.x+=player_velocity
        player_image=player_image_right
    if keys[pg.K_UP] and player_rect.top>100:
        player_rect.y-=player_velocity
    if keys[pg.K_DOWN] and player_rect.bottom<win_height:
        player_rect.y+=player_velocity

    #booster
    if keys[pg.K_SPACE] and boost_level>0:
        player_velocity=player_boost_velocity
        boost_level-=1
    else:
        player_velocity=player_normal_velocity
    
    #move the burger and update burger points
    burger_rect.y+=burger_velocity
    burger_points=int(burger_velocity*(win_height-burger_rect.y+100))
    
    #player miss the burger
    if burger_rect.y>win_height:
        player_lives-=1
        miss_sound.play()

        burger_rect.topleft=(random.randint(0,win_width-32),-buffer_distance)
        burger_velocity=starting_burger_velocity

        player_rect.centerx=win_width//2
        player_rect.bottom=win_height
        boost_level=starting_boost_level

    
    #collisions
    if player_rect.colliderect(burger_rect):
        score+=burger_points
        burgers_eaten+=1
        bark_sound.play()

        burger_rect.topleft=(random.randint(0,win_width-32),-buffer_distance)
        burger_velocity+=burger_acceleration

        boost_level+=25
        if boost_level>starting_boost_level:
            boost_level=starting_boost_level

    #update hud
    points_text=font.render('Burger Points: '+str(burger_points),True,orange)
    score_text=font.render('Score: '+str(score),True,orange)
    eaten_text=font.render('Burgers Eaten: '+str(burgers_eaten),True,orange)
    lives_text=font.render('Lives: '+str(player_lives),True,orange)
    boost_text=font.render('Boost: '+str(boost_level),True,orange)

    #check for game over
    if player_lives==0:
        game_over_text=font.render('Final Score: '+str(score),True,orange)
        display_surface.blit(game_over_text,game_over_rect)
        display_surface.blit(continue_text,continue_rect)
        pg.display.update()

        #pause game until a key is pressed then reset
        pg.mixer.music.stop()
        is_pause=True
        while is_pause:
            for event in pg.event.get():
                #player wants to play again
                if event.type==pg.KEYDOWN:
                    score=0
                    burgers_eaten=0
                    player_lives=player_starting_lives
                    boost_level=starting_boost_level
                    burger_velocity=starting_burger_velocity
                    
                    pg.mixer.music.play()
                    is_pause=False

                #quit
                if event.type==pg.QUIT:
                    is_pause=False
                    running=False

    #fill surface
    display_surface.fill(black)

    #blit hud
    display_surface.blit(points_text,points_rect)
    display_surface.blit(score_text,score_rect)
    display_surface.blit(title_text,title_rect)
    display_surface.blit(eaten_text,eaten_rect)
    display_surface.blit(lives_text,lives_rect)
    display_surface.blit(boost_text,boost_rect)
    pg.draw.line(display_surface,white,(0,100),(win_width,100),3)

    #blit assets
    display_surface.blit(player_image,player_rect)
    display_surface.blit(burger_image,burger_rect)

    #update display and tick the clock
    pg.display.update()
    clock.tick(fps)

#end the game
pg.quit()