import pygame
import asyncio
import platform
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.SysFont('Arial', 36)
SMALL_FONT = pygame.font.SysFont('Arial', 24)

# Word list
WORDS = ['PYTHON', 'PROGRAMMING', 'COMPUTER', 'ALGORITHM', 'DATABASE', 'NETWORK', 'SOFTWARE']

# Game variables
word = ""
guessed_letters = set()
wrong_guesses = 0
max_guesses = 6
buttons = []
game_state = "playing"  # playing, won, lost

def setup():
    global screen, word, guessed_letters, wrong_guesses, buttons, game_state
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hangman Game")
    word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = 0
    game_state = "playing"
    
    # Create letter buttons
    buttons.clear()
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i, letter in enumerate(letters):
        x = 50 + (i % 13) * 50
        y = 400 + (i // 13) * 60
        buttons.append({'letter': letter, 'rect': pygame.Rect(x, y, 40, 40), 'enabled': True})

def draw_hangman():
    # Gallows
    pygame.draw.line(screen, BLACK, (150, 350), (150, 100), 5)  # Vertical pole
    pygame.draw.line(screen, BLACK, (150, 100), (250, 100), 5)  # Horizontal beam
    pygame.draw.line(screen, BLACK, (250, 100), (250, 150), 5)  # Rope
    
    # Hangman parts
    if wrong_guesses > 0:  # Head
        pygame.draw.circle(screen, BLACK, (250, 175), 25, 3)
    if wrong_guesses > 1:  # Body
        pygame.draw.line(screen, BLACK, (250, 200), (250, 250), 3)
    if wrong_guesses > 2:  # Left arm
        pygame.draw.line(screen, BLACK, (250, 210), (220, 230), 3)
    if wrong_guesses > 3:  # Right arm
        pygame.draw.line(screen, BLACK, (250, 210), (280, 230), 3)
    if wrong_guesses > 4:  # Left leg
        pygame.draw.line(screen, BLACK, (250, 250), (220, 290), 3)
    if wrong_guesses > 5:  # Right leg
        pygame.draw.line(screen, BLACK, (250, 250), (280, 290), 3)

def draw_word():
    display_word = ""
    for letter in word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = FONT.render(display_word, True, BLACK)
    screen.blit(text, (300, 200))

def draw_buttons():
    for button in buttons:
        color = BLUE if button['enabled'] else GRAY
        pygame.draw.rect(screen, color, button['rect'])
        text = SMALL_FONT.render(button['letter'], True, WHITE)
        text_rect = text.get_rect(center=button['rect'].center)
        screen.blit(text, text_rect)

def draw_game_state():
    if game_state == "won":
        text = FONT.render("You Won!", True, BLUE)
        screen.blit(text, (300, 300))
    elif game_state == "lost":
        text = FONT.render("Game Over! Word was: " + word, True, RED)
        screen.blit(text, (300, 300))
        restart_text = SMALL_FONT.render("Click to Restart", True, BLACK)
        screen.blit(restart_text, (300, 350))

def check_win():
    global game_state
    if all(letter in guessed_letters for letter in word):
        game_state = "won"
    elif wrong_guesses >= max_guesses:
        game_state = "lost"

def handle_click(pos):
    global wrong_guesses, game_state
    for button in buttons:
        if button['rect'].collidepoint(pos) and button['enabled']:
            button['enabled'] = False
            letter = button['letter']
            guessed_letters.add(letter)
            if letter not in word:
                wrong_guesses += 1
            check_win()
            break
    if game_state != "playing":
        # Restart on click
        setup()

def update_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.MOUSEBUTTONDOWN and game_state != "playing":
            handle_click(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "playing":
            handle_click(event.pos)
    
    screen.fill(WHITE)
    draw_hangman()
    draw_word()
    draw_buttons()
    draw_game_state()
    pygame.display.flip()

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
