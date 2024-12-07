#Program: Sayo's game?
#Author: Sayo Owolabi
#Date 02/12/24
from sys import displayhook

import pygame

import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sayo's Pet Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define font
font = pygame.font.SysFont('Courier', 24)

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

    def update_sprite(self):
        """Updates the sprite based on the cat's status"""
        if self.hunger < 3:
            self.curr_sprite = HungryCat()
        elif self.tiredness < 3:
            self.curr_sprite = SleepyCat()
        elif self.boredom < 3:
            self.curr_sprite = SadCat()
        elif self.hunger > 7 and self.tiredness > 7 and self.boredom > 7:
            self.curr_sprite = PlayfulCat()
        else:
            self.curr_sprite = HappyCat()

    def draw(self):
        """Draw the current sprite on the screen"""
        screen.fill(WHITE)
        self.curr_sprite.draw(screen, 300, 200)
        pygame.display.flip()


# Game loop
def main():
    running = True
    clock = pygame.time.Clock()
    cat = Cat()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Increase hunger
                    cat.hunger += 1
                elif event.key == pygame.K_DOWN:  # Decrease hunger
                    cat.hunger -= 1
                elif event.key == pygame.K_LEFT:  # Decrease tiredness
                    cat.tiredness -= 1
                elif event.key == pygame.K_RIGHT:  # Increase tiredness
                    cat.tiredness += 1
                elif event.key == pygame.K_SPACE:  # Decrease boredom
                    cat.boredom -= 1

        # Update sprite based on status
        cat.update_sprite()
        cat.draw()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
