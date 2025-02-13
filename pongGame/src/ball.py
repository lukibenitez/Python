import pygame
from random import choice
import math

class Ball:
    def __init__(self, x, y, size, speed, color):
        # En lugar de usar Rect, guardamos las coordenadas directamente
        self.x = x
        self.y = y
        self.radius = size // 2    # Ahora usamos radio en lugar de size
        self.speed = speed
        self.speed_x = 0
        self.speed_y = 0
        self.color = color
        self.original_pos = (x, y)
        self.original_speed = speed
        self.attached = True  # Nueva variable para saber si la bola está pegada a la paleta

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        # Dibujamos un círculo en lugar de un rectángulo
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def collides_with_paddle(self, paddle):
        # Encontrar el punto más cercano entre el círculo y el rectángulo
        closest_x = max(paddle.rect.left, min(self.x, paddle.rect.right))
        closest_y = max(paddle.rect.top, min(self.y, paddle.rect.bottom))
        
        # Calcular la distancia entre el centro del círculo y el punto más cercano
        distance_x = self.x - closest_x
        distance_y = self.y - closest_y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        # Si la distancia es menor que el radio, hay colisión
        return distance <= self.radius
    
    def attach_to_paddle(self, paddle):
        # Posicionar la bola en el centro derecho de la paleta
        self.x = paddle.rect.right + self.radius
        self.y = paddle.rect.centery
        self.speed_x = 0
        self.speed_y = 0
        self.attached = True
        
    def launch(self):
        if self.attached:
            self.speed_x = self.speed
            self.speed_y = choice([-self.speed, self.speed])
            self.attached = False

    def bounce_y(self):
        self.speed_y *= -1

    def bounce_x(self):
        self.speed_x *= -1
    
    def bounce_from_paddle(self, paddle):
        # Calcular el punto de impacto relativo en la paleta (-1 a 1)
        # -1 es la parte superior de la paleta, 0 es el centro, 1 es la parte inferior
        relative_intersect_y = (paddle.rect.centery - self.y) / (paddle.rect.height / 2)
        
        # Normalizar para mantener la velocidad constante
        normalized_y = -relative_intersect_y * 0.75  # Factor 0.75 para limitar el ángulo máximo
        
        # Calcular la dirección x basada en qué paleta golpeó
        direction = -1 if self.speed_x > 0 else 1
        
        # Velocidad base
        speed = math.sqrt(self.speed_x**2 + self.speed_y**2)
        
        # Calcular el nuevo ángulo
        angle = normalized_y * math.pi/3  # 60 grados como ángulo máximo
        
        # Actualizar velocidades
        self.speed_x = direction * speed * math.cos(angle)
        self.speed_y = speed * math.sin(angle)

    def reset(self):
        self.x = self.original_pos[0]
        self.y = self.original_pos[1]
        self.speed_x = self.original_speed * choice([-1, 1])
        self.speed_y = self.original_speed * choice([-1, 1])
