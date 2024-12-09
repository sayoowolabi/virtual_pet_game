##Sayo's Pet game

import pygame
import time

pygame.init()



### SPRITES ####
class Sprites(object):
    """Parent class of the different sprites"""
    def __init__(self, s_type, art):
        self.s_type = s_type
        self.art = art

    def draw(self, surface, x, y):
        """Draw the sprite art on the surface"""
        lines = self.art.strip().split('\n')
        for i, line in enumerate(lines):
            text = font.render(line, True, BLACK)
            surface.blit(text, (x, y + i * 30))


class HappyCat(Sprites):
    def __init__(self):
        art = r"""
                 /\_/\  
                ( ^.^ ) 
                 > ^ <
                """
        super().__init__("Happy", art)


class SadCat(Sprites):
    def __init__(self):
        art = r"""
                 /\_/\  
                ( T.T ) 
                 >   <
                """
        super().__init__("Sad", art)


class HungryCat(Sprites):
    def __init__(self):
        art = r"""
                 /\_/\  
                ( o.o ) 
                 > m <
                """
        super().__init__("Hungry", art)


class SleepyCat(Sprites):
    def __init__(self):
        art = r"""
                 /\_/\  
                (-.-) Zzz
                 >   <
                """
        super().__init__("Sleepy", art)


class AngryCat(Sprites):
    def __init__(self):
        art = r"""
                 /\_/\  
                ( >.< ) 
                 >   <
                """
        super().__init__("Angry", art)


class PlayfulCat(Sprites):
    def __init__(self):
        art = r"""
                 /\_/\  
                ( ^o^ ) 
                 >   ⌒
                """
        super().__init__("Playful", art)


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
        print(self.curr_sprite.__str__())

    def besad(self):
        self.curr_sprite = SadCat()
        print(self.curr_sprite.__str__())

    def behungry(self):
        self.curr_sprite = HungryCat()
        print(self.curr_sprite.__str__())

    def besleepy(self):
        self.curr_sprite = SleepyCat()
        print(self.curr_sprite.__str__())

    def beangry(self):
        self.curr_sprite = AngryCat()
        print(self.curr_sprite.__str__())

    def beplayful(self):
        self.curr_sprite = PlayfulCat()
        print(self.curr_sprite.__str__())


    def checkState(self):
        is_hungry, is_tired, is_bored, is_fine, is_sad, is_angry = "hunger", "fatigue", "boredom", "happiness", "default", "anger"
        status = {is_hungry: True, is_tired: True, is_bored: True, is_fine: True, is_angry: True, is_sad: True}

        below_threshold = 0

        if self.hunger < 5:
            status[is_hungry] = True
            below_threshold = below_threshold + 1
        else:
            status[is_hungry] = False

        if self.tiredness < 5:
            status[is_tired] = True
            below_threshold = below_threshold + 1
        else:
            status[is_tired] = False

        if self.boredom < 5:
            status[is_bored] = True
            below_threshold = below_threshold + 1
        else:
            status[is_bored] = False


        if below_threshold >= 3:
            self.beangry()
            status[is_angry] = True
            return
        else:
            status[is_angry] = False

        if below_threshold > 2:
            self.besad()
            status[is_sad] = True
            return
        else:
            status[is_sad] = False

        if below_threshold == 0:
            self.behappy()
            status[is_fine] = True
            return
        else:
            status[is_fine] = False

        if not status[is_sad] or status[is_angry]:
            if status[is_hungry]:
                self.behungry()
            if status[is_tired]:
                self.besleepy()
            if status[is_bored]:
                self.besad()

    def draw(self):
        """draw the current sprite to the screen
        """
        
        screen.fill(WHITE)
        self.curr_sprite.draw(screen, 300, 200)
        pygame.display.flip()


  
font = pygame.font.SysFont('Courier', 24)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sayo's Pet Game")

    #events
hungertick = pygame.USEREVENT + 1
pygame.time.set_timer(hungertick, 20000)

boredomtick = pygame.USEREVENT + 2
pygame.time.set_timer(boredomtick, 10000)

fatiguetick = pygame.USEREVENT + 3
pygame.time.set_timer(fatiguetick, 100000)

# Define font
font = pygame.font.SysFont('Courier', 24)

running = True
clock = pygame.time.Clock()
cat = Cat()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == hungertick:
            cat.hunger = cat.hunger - 1
        
        elif event.type == boredomtick:
            cat.boredom = cat.boredom - 1
            
        elif event.type == fatiguetick:
            cat.tiredness = cat.tiredness -1


    cat.checkState()
    cat.draw()
    clock.tick(60)
