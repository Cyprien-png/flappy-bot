import pygame
import random

class Obstacle:
    
    def __init__(self):
        self.position_x = pygame.display.get_surface().get_size()[0]
        self.width = 50
        self.hole_size = 200
        self.hole_height = random.randint(0, pygame.display.get_surface().get_size()[1] - self.hole_size)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.position_x, 0, self.width, self.hole_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.position_x, self.hole_height + self.hole_size, self.width, pygame.display.get_surface().get_size()[1]))
        
    def update(self, velocity):
        self.position_x -= velocity
        return False if self.position_x + self.width < 0 else True
        
     