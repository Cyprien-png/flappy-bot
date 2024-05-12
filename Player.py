import pygame

class Player:

    position_y = 0
    position_x = 100
    width = 50
    velocity = 0
    
    def __init__(self) -> None:
        self.position_y = pygame.display.get_surface().get_size()[1] / 2

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.position_x, self.position_y), self.width/2)

    def jump(self):
        self.velocity = -25

    def update(self):
        self.velocity += 0.5
        self.position_y += (self.velocity) / 5

        if self.position_y > pygame.display.get_surface().get_size()[1] - self.width/2:
            return False

        elif self.position_y < self.width/2:
            return False
        
        else:
            return True
