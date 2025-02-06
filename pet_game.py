import pygame
import time
from functions import choose_word, draw_game_state, check_match, display_message, LIVES, FPS
from screen_setup import screen, SCREEN_HEIGHT, SCREEN_WIDTH, RED, BLACK, WHITE, GREEN, BLUE, GRAY, background_image, font
import sys
from myClasses import Sprites, Food, Games, Cat, Bread, HappyCat, SadCat, AngryCat, PlayfulCat, SleepyCat, HungryCat, cat, games, bread, pizza


# Initialize Pygame
pygame.init()



### EVENTS ###
hungertick = pygame.USEREVENT + 1
pygame.time.set_timer(hungertick, 15000)  

boredomtick = pygame.USEREVENT + 2
pygame.time.set_timer(boredomtick, 10500)  

fatiguetick = pygame.USEREVENT + 3
pygame.time.set_timer(fatiguetick, 100000)  


### GAME LOOP ###
running = True
clock = pygame.time.Clock()

feeding_menu = False
game_menu = False
homescreen_state = True


while running:
    
    screen.blit(background_image, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == hungertick:
            cat.hunger = max(0, cat.hunger - 1)
        
        elif event.type == boredomtick:
            cat.boredom = max(0, cat.boredom - 1)
            
        elif event.type == fatiguetick:
            cat.tiredness = max(0, cat.tiredness - 1)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # If player presses F, show feed menu
                feeding_menu = True
                game_menu = False
                homescreen_state = False
                
            elif event.key == pygame.K_b and feeding_menu:  # Feed the pet bread
                bread.feed_pet(cat)
                feeding_menu = False  # Return to homescreen
                homescreen_state = True
                
            elif event.key == pygame.K_p and feeding_menu:  # Feed the pet bread
                pizza.feed_pet(cat)
                feeding_menu = False  # Return to homescreen
                homescreen_state = True
                
            elif event.key == pygame.K_p:
                game_menu = True
                feeding_menu = False
                homescreen_state = False

            elif event.key == pygame.K_w and game_menu:
                game_menu = False
                games.wordgame()
                games.play(cat)
                homescreen_state = True


    cat.checkState()
    cat.draw(feeding_menu, game_menu, homescreen_state)
    clock.tick(60)

pygame.quit()