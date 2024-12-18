import pygame
import random
import sys

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Font setup
pygame.font.init()
font = pygame.font.SysFont('Courier', 36)
small_font = pygame.font.SysFont('Courier', 24)

# Game State
LIVES = 8
FPS = 60

def choose_word():
    """Function to choose a random word from a text file"""
   
    #choose random number
    i = 1
    lineNo = random.randint(1,1000)
    # print(lineNo)
        
    #open word bank for reading
    wordBank = open("hangman-wordlist.txt", "r")
        
    lines = wordBank.readlines()
        
    #get the word that corrolates with the random number
    for line in lines:
        if i == lineNo:
            chosenWord = line[:-1]
            # print(chosenWord)
                
        i= i+1
        
    wordBank.close()
    
    return chosenWord


def draw_game_state(screen, word, player_word, incorrect_guesses, lives_left):
    """Draw the current state of the game on the screen"""
    screen.fill(WHITE)
    
    # Title
    title_text = font.render("Hangman Game", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))
    
    # Display player's current progress
    current_progress = " ".join(player_word)
    progress_text = font.render(current_progress, True, BLACK)
    screen.blit(progress_text, (SCREEN_WIDTH // 2 - progress_text.get_width() // 2, 100))
    
    # Display incorrect guesses
    incorrect_text = small_font.render(f"Incorrect Guesses: {', '.join(incorrect_guesses)}", True, RED)
    screen.blit(incorrect_text, (20, 200))
    
    # Display remaining lives
    lives_text = small_font.render(f"Lives Left: {lives_left}", True, BLACK)
    screen.blit(lives_text, (20, 250))
    
    # Display instructions
    instructions_text = small_font.render("Type a letter to guess", True, BLUE)
    screen.blit(instructions_text, (20, 500))
    
    pygame.display.flip()


def check_match(word, currentguess):
    """Function to check if the player has guessed the word"""
    
    #create a string with their correctly guessed letters
    joinedGuessWord = ""
    for char in currentguess:
        joinedGuessWord = joinedGuessWord + char
    
    #determine if they have guessed the word or not
    if joinedGuessWord == word:
        return True
    else:
        return False


def display_message(screen, message, colour):
    """Display continue message in the center of the screen"""
    screen.fill(WHITE)
    message_text = font.render(message, True, colour)
    instructions_text = small_font.render("Press C to continue or Q to quit", True, BLACK)
    screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    waiting = False
                    return True
                elif event.key == pygame.K_q:
                    return False
                    
