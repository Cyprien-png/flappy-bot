import pygame
from Player import Player

class Game:
    
    screen = pygame.display.set_mode((1280, 500))
    clock = pygame.time.Clock()
    running = True
    player = Player()
    
    def __init__(self):
        pygame.init()
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        pygame.display.flip()
        
    def update(self):
        self.player.update()
    
    def run(self):
        while self.running:
            self.clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player.jump()

            self.draw()
            self.update()

game = Game()
game.run()