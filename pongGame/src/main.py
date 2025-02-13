import pygame
import sys
from game import PongGame
from menu import PongMenu
from enum import Enum

# Definición de estados del juego
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

# Inicialización de Pygame
pygame.init()

# Constantes
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración de la ventana
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong Game")

game_state = GameState.MENU
menu = PongMenu(WINDOW_WIDTH, WINDOW_HEIGHT)
game = None

def main():
    global game_state
    global game
    clock = pygame.time.Clock()
    
    while True:
        if game_state == GameState.MENU:
            start_game, difficulty, max_score = menu.handle_input()
            menu.draw(screen)
            
            if start_game:
                game = PongGame(WINDOW_WIDTH, WINDOW_HEIGHT, difficulty, max_score)
                game_state = GameState.PLAYING
                
        elif game_state == GameState.PLAYING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_state = GameState.MENU
                        continue
                        
            game.handle_input()
            game.update()
            screen.fill(BLACK)
            game.draw(screen)
            
            if game.check_winner():
                game_state = GameState.MENU
                
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()