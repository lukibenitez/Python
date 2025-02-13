import pygame
import sys
from enum import Enum

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

class PongMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 50)
        
        # Opciones del menú
        self.difficulty_options = ["FÁCIL", "INTERMEDIO", "IMPOSIBLE"]
        self.score_options = [5, 10, 15]
        self.current_difficulty = 0
        self.current_score = 1
        self.selected_option = 0  # 0 para dificultad, 1 para puntuación
        
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        # Título
        title = self.font_big.render("PONG GAME", True, (255, 255, 255))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 100))
        
        # Opciones de dificultad
        diff_text = self.font_small.render(f"Dificultad: < {self.difficulty_options[self.current_difficulty]} >", True, (255, 255, 0) if self.selected_option == 0 else (255, 255, 255))
        screen.blit(diff_text, (self.screen_width//2 - diff_text.get_width()//2, 300))
        
        # Opciones de puntuación
        score_text = self.font_small.render(f"Puntos para ganar: < {self.score_options[self.current_score]} >", True, (255, 255, 0) if self.selected_option == 1 else (255, 255, 255))
        screen.blit(score_text, (self.screen_width//2 - score_text.get_width()//2, 400))
        
        # Instrucciones
        start_text = self.font_small.render("Presiona ESPACIO para comenzar", True, (255, 255, 255))
        screen.blit(start_text, (self.screen_width//2 - start_text.get_width()//2, 500))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % 2
                
                elif event.key == pygame.K_LEFT:
                    if self.selected_option == 0:
                        self.current_difficulty = (self.current_difficulty - 1) % len(self.difficulty_options)
                    else:
                        self.current_score = (self.current_score - 1) % len(self.score_options)
                
                elif event.key == pygame.K_RIGHT:
                    if self.selected_option == 0:
                        self.current_difficulty = (self.current_difficulty + 1) % len(self.difficulty_options)
                    else:
                        self.current_score = (self.current_score + 1) % len(self.score_options)
                
                elif event.key == pygame.K_SPACE:
                    return True, self.difficulty_options[self.current_difficulty], self.score_options[self.current_score]
        
        return False, None, None