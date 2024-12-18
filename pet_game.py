import pygame
import time
from functions import choose_word, draw_game_state, check_match, display_message, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, BLUE, GRAY, LIVES, FPS
import sys


# Initialize Pygame
pygame.init()


# Font definition
font = pygame.font.SysFont('Verdana', 24)

# Screen setup
background_image = pygame.image.load("images/background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sayo's Pet Game")


### SPRITES ###
class Sprites(object):
    """Parent class of the different sprites"""
    def __init__(self, s_type, image_path):
        self.s_type = s_type
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (200, 200))  # Resize image to fit screen

    def draw(self, surface, x, y):
        """Draw the sprite image on the surface"""
        surface.blit(self.image, (x, y))


class HappyCat(Sprites):
    def __init__(self):
        super().__init__("Happy", "images/happy_cat.png")


class SadCat(Sprites):
    def __init__(self):
        super().__init__("Sad", "images/sad.png")


class HungryCat(Sprites):
    def __init__(self):
        super().__init__("Hungry", "images/hungry_cat.png")


class SleepyCat(Sprites):
    def __init__(self):
        super().__init__("Sleepy", "images/sad.png")


class AngryCat(Sprites):
    def __init__(self):
        super().__init__("Angry", "images/angry_cat.png")


class PlayfulCat(Sprites):
    def __init__(self):
        super().__init__("Playful", "images/playful_cat.png")


### FOOD ###
class Food(object):
    def __init__(self, hunger_points=0.0, boredom_bonus=0.0, fatigue_bonus=0.0):
        self.hunger_points = hunger_points
        self.boredom_bonus = boredom_bonus
        self.fatigue_bonus = fatigue_bonus


class Bread(Food):
    def __init__(self):
        super().__init__(hunger_points=3, boredom_bonus=0, fatigue_bonus=0)

    def feed_pet(self, pet):
        pet.hunger += self.hunger_points
        if pet.hunger > 10:  # Cap hunger at 10
            pet.hunger = 10


### GAMES ###

class Games:
    def __init__(self, boredom_points = 1):
        self.boredom_points = boredom_points
    
    def wordgame(self):
        

        """Main game loop for the word game"""
        word = choose_word()
        player_word = [None] * len(word)
        for i in range(0,len(player_word)):
            player_word[i] = "_"
            
        incorrect_guesses = []
        lives_left = 8

        running = True
        while running:
            draw_game_state(screen, word, player_word, incorrect_guesses, lives_left)
            correct = False
            cont = True

            for event in pygame.event.get():    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha() and len(event.unicode) == 1:
                        player_guess = event.unicode.lower()
                        for i, char in enumerate(word):
                            if char == player_guess:
                                player_word[i] = char
                                cont = display_message(screen, "Correct!", GREEN)
                                correct = True
                                if not cont:
                                    return
                        if correct == False:
                            incorrect_guesses.append(player_guess)
                            cont = display_message(screen, "Wrong!", RED)
                            lives_left -= 1
                            if not cont:
                                return

            if check_match(word, player_word):
                draw_game_state(screen, word, player_word, incorrect_guesses, lives_left)
                display_message(screen, "You win!", GREEN)
                running = False
                
            
            if lives_left <= 0:
                draw_game_state(screen, word, player_word, incorrect_guesses, lives_left)
                display_message(screen, f"You lost! The word was: {word}", RED)
                running = False

    def play(self, pet):
        
        pet.boredom = pet.boredom + self.boredom_points
        
        if pet.boredom > 10:
            pet.boredom = 10
        
        

### CAT ###
class Cat:
    """Class for cats"""
    def __init__(self, hunger=5, tiredness=5, boredom=5):
        self.hunger = hunger
        self.tiredness = tiredness
        self.boredom = boredom
        self.curr_sprite = HappyCat()

    def behappy(self):
        """Makes your sprite happy"""
        self.curr_sprite = HappyCat()

    def besad(self):
        self.curr_sprite = SadCat()

    def behungry(self):
        self.curr_sprite = HungryCat()

    def besleepy(self):
        self.curr_sprite = SleepyCat()

    def beangry(self):
        self.curr_sprite = AngryCat()

    def beplayful(self):
        self.curr_sprite = PlayfulCat()

    def checkState(self):
        is_hungry, is_tired, is_bored, is_fine, is_sad, is_angry = "hunger", "fatigue", "boredom", "happiness", "default", "anger"
        status = {is_hungry: False, is_tired: False, is_bored: False, is_fine: False, is_sad: False, is_angry: False}

        below_threshold = 0

        if self.hunger < 5:
            status[is_hungry] = True
            below_threshold += 1

        if self.tiredness < 5:
            status[is_tired] = True
            below_threshold += 1

        if self.boredom < 5:
            status[is_bored] = True
            below_threshold += 1

        if below_threshold >= 3:
            self.beangry()
            status[is_angry] = True
            return
        elif below_threshold > 1:
            self.besad()
            status[is_sad] = True
            return
        elif below_threshold == 0:
            self.behappy()
            status[is_fine] = True
            return

        if not status[is_sad] or status[is_angry]:
            if status[is_hungry]:
                self.behungry()
            if status[is_tired]:
                self.besleepy()
            if status[is_bored]:
                self.besad()
            if not status[is_bored] and self.boredom > 6:
                self.beplayful()

    def draw(self, feeding_menu, game_menu, homescreen_state):
        """Draw the current sprite and instructions on the screen"""
        
        
        self.curr_sprite.draw(screen, (SCREEN_WIDTH - self.curr_sprite.image.get_width()) // 2, (SCREEN_HEIGHT - self.curr_sprite.image.get_height()) // 2)
        
        if homescreen_state == True:
            if homescreen_state:
                instructions_text_1 = font.render("Press P to play a game", True, BLACK)
                instructions_text_2 = font.render("Press F to feed the pet", True, BLACK)
                hunger_stat = font.render(f'Hunger: {cat.hunger}', True, BLUE)
                tiredness_stat = font.render(f'Tiredness: {cat.tiredness}', True, BLUE)
                boredom_stat = font.render(f'Boredom: {cat.boredom}', True, BLUE)

                # Blit (draw) the text onto the screen
                screen.blit(hunger_stat, (20, 490))
                screen.blit(tiredness_stat, (20, 520))
                screen.blit(boredom_stat, (20, 550))
                screen.blit(instructions_text_1, (SCREEN_WIDTH // 2 - instructions_text_1.get_width() // 2, 500))
                screen.blit(instructions_text_2, (SCREEN_WIDTH // 2 - instructions_text_2.get_width() // 2, 550))
        else:
            if feeding_menu:
                instructions_text = font.render('Press B to feed the pet bread', True, BLACK)
                screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, 500))

            
            if game_menu:
                instructions_text = font.render('Press W to play a word game', True, BLACK)
                screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, 500))

            
                    
        pygame.display.flip()



### EVENTS ###
hungertick = pygame.USEREVENT + 1
pygame.time.set_timer(hungertick, 15000)  

boredomtick = pygame.USEREVENT + 2
pygame.time.set_timer(boredomtick, 10000)  

fatiguetick = pygame.USEREVENT + 3
pygame.time.set_timer(fatiguetick, 100000)  


### GAME LOOP ###
running = True
clock = pygame.time.Clock()

feeding_menu = False
game_menu = False
homescreen_state = True
cat = Cat()
bread = Bread()
games = Games()

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