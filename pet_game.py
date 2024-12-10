import pygame
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 105, 180)

# Font definition
font = pygame.font.SysFont('Courier', 24)

# Screen setup
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
        super().__init__("Sleepy", "images/sleepy_cat.png")


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

    def draw(self, feeding_menu):
        """Draw the current sprite and instructions on the screen"""
        
        screen.fill(WHITE)
        self.curr_sprite.draw(screen, (SCREEN_WIDTH - self.curr_sprite.image.get_width()) // 2, (SCREEN_HEIGHT - self.curr_sprite.image.get_height()) // 2)
        
        if feeding_menu:
            feed_text = font.render('Press B to feed the pet bread', True, PINK)
        else:
            feed_text = font.render('Press F to feed the pet', True, PINK)
            
        screen.blit(feed_text, (20, 20))
        
        pygame.display.flip()



### EVENTS ###
hungertick = pygame.USEREVENT + 1
pygame.time.set_timer(hungertick, 20000)  # Hunger decreases every 20 seconds

boredomtick = pygame.USEREVENT + 2
pygame.time.set_timer(boredomtick, 10000)  # Boredom increases every 10 seconds

fatiguetick = pygame.USEREVENT + 3
pygame.time.set_timer(fatiguetick, 100000)  # Fatigue increases every 100 seconds


### GAME LOOP ###
running = True
clock = pygame.time.Clock()
cat = Cat()
bread = Bread()

feeding_menu = False

while running:
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
            if event.key == pygame.K_f:  # If player presses F show feed menu
                feeding_menu = True
            
            elif event.key == pygame.K_b and feeding_menu:  # Feed the pet bread
                bread.feed_pet(cat)
                feeding_menu = False 

    cat.checkState()
    cat.draw(feeding_menu)
    clock.tick(60)

pygame.quit()
