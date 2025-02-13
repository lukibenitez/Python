import pygame
from paddle import Paddle
from ball import Ball
import time

class PongGame:
    def __init__(self, screen_width, screen_height, difficulty, max_score):
        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        
        # Dimensiones
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Crear paletas
        paddle_width = 15
        paddle_height = 90
        paddle_speed = 5
        
        self.paddle_left = Paddle(
            10, screen_height//2 - paddle_height//2,
            paddle_width, paddle_height, paddle_speed, self.WHITE
        )
        
        self.paddle_right = Paddle(
            screen_width - 25, screen_height//2 - paddle_height//2,
            paddle_width, paddle_height, paddle_speed, self.WHITE
        )
        
        # Crear pelota
        ball_size = 15
        ball_speed = 5
        self.ball = Ball(0, 0, ball_size, ball_speed, self.WHITE)
        self.ball.attach_to_paddle(self.paddle_left)
        
        # Puntuación
        self.score_left = 0
        self.score_right = 0
        self.font = pygame.font.Font(None, 74)

        self.max_score = max_score

        # Ajustar la velocidad de la IA según la dificultad
        self.difficulty = difficulty
        if difficulty == "FÁCIL":
            self.AI_SPEED = 4
            self.reaction_delay = 0.5  # Medio segundo de retraso
            self.prediction_error = 100  # Error en pixels para predecir posición
        elif difficulty == "INTERMEDIO":
            self.AI_SPEED = 6
            self.reaction_delay = 0.2  # 0.2 segundos de retraso
            self.prediction_error = 50  # Menor error de predicción
        else:  # IMPOSIBLE
            self.AI_SPEED = 8
            self.reaction_delay = 0  # Sin retraso
            self.prediction_error = 0  # Sin error

        self.last_move_time = time.time()
        self.target_y = self.paddle_left.rect.centery

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Lanzar la bola con espacio
        if keys[pygame.K_SPACE]:
            self.ball.launch()
            
        # Paleta derecha: Flecha arriba y abajo
        if keys[pygame.K_UP]:
            self.paddle_right.move(up=True)
        if keys[pygame.K_DOWN]:
            self.paddle_right.move(up=False)

    def update(self):

        # Actualizar la IA
        self.update_ai_paddle()

        # Actualizar posiciones
        self.ball.move()
        self.paddle_left.update(self.screen_height)
        self.paddle_right.update(self.screen_height)
        
        # Colisiones con bordes superior e inferior
        if self.ball.y - self.ball.radius <= 0 or \
            self.ball.y + self.ball.radius >= self.screen_height:
                self.ball.bounce_y()
        
        # Colisiones con paletas
        if self.ball.collides_with_paddle(self.paddle_left) or \
            self.ball.collides_with_paddle(self.paddle_right):
                paddle = self.paddle_left if self.ball.x < self.screen_width/2 else self.paddle_right
                self.ball.bounce_from_paddle(paddle)
            
        # Puntuación
        if self.ball.x - self.ball.radius <= 0:
            self.score_right += 1
            self.reset_round()
        elif self.ball.x + self.ball.radius >= self.screen_width:
            self.score_left += 1
            self.reset_round()

    def update_ai_paddle(self):
        current_time = time.time()
        
        # Solo actualiza el objetivo si ha pasado el tiempo de retraso
        if current_time - self.last_move_time >= self.reaction_delay:
            # Añadir error aleatorio a la predicción
            from random import randint
            error = randint(-self.prediction_error, self.prediction_error)
            
            # Actualizar posición objetivo
            if not self.ball.attached:
                self.target_y = self.ball.y + error
                self.last_move_time = current_time

        # Mover la paleta hacia el objetivo
        paddle_center = self.paddle_left.rect.centery
        
        if abs(paddle_center - self.target_y) > self.AI_SPEED:  # Si no está en la posición objetivo
            if self.target_y < paddle_center:
                self.paddle_left.move(up=True)
            elif self.target_y > paddle_center:
                self.paddle_left.move(up=False)

    def draw(self, screen):
        # Dibujar elementos
        self.paddle_left.draw(screen)
        self.paddle_right.draw(screen)
        self.ball.draw(screen)
        
        # Dibujar puntuación
        score_left_surf = self.font.render(str(self.score_left), True, self.WHITE)
        score_right_surf = self.font.render(str(self.score_right), True, self.WHITE)
        screen.blit(score_left_surf, (self.screen_width//4, 20))
        screen.blit(score_right_surf, (3*self.screen_width//4, 20))

    def reset_round(self):
        self.ball.attach_to_paddle(self.paddle_left)
        self.paddle_left.reset()
        self.paddle_right.reset()

    def check_winner(self):
        if self.score_left >= self.max_score or self.score_right >= self.max_score:
            return True
        return False