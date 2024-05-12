import pygame

class Player:

    position_y = 40
    position_x = 100
    height = 50
    width = 50
    velocity = 0

    def draw(self, screen):
        surface = pygame.surface.Surface((self.width, self.height))
        pygame.draw.circle(surface, (255, 0, 0), (25, 25), 25)
        screen.blit(surface, (self.position_x, self.position_y))

    def jump(self):
        self.velocity = -25

    def update(self):
        self.velocity += 0.5
        self.position_y += (self.velocity) / 5

        if self.position_y > 450:
            self.position_y = 450
            self.velocity = 0

        elif self.position_y < 0:
            self.position_y = 0
            self.velocity = 0
