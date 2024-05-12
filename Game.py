import pygame
from Player import Player
from Obstacle import Obstacle

class Game:
    
    screen = pygame.display.set_mode((1280, 500))
    clock = pygame.time.Clock()
    running = True
    player = Player()
    obstacles = []
    obstacles_gap = 250
    game_speed = 2
    
    distance = 0
    lose_count = 0
    
    def __init__(self):
        pygame.init()
        
    def lose(self):
        self.lose_count += 1
        self.player = Player()
        self.distance = 0
        self.obstacles = []
        
    def draw(self):
        obstacles = self.obstacles
        
        # clear screen
        self.screen.fill((0, 0, 0))

        # draw game objects
        for obstacle in obstacles:
            obstacle.draw(self.screen)
        
        self.player.draw(self.screen)
        
        # draw game text score
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.distance), 1, (255, 255, 255))
        textpos = text.get_rect(centerx=self.screen.get_width()/2)
        self.screen.blit(text, textpos)
        
        # update screen
        pygame.display.flip()
        
        
    def update(self):
        obstacles = self.obstacles

        # update game objects
        for obstacle in obstacles:
            if obstacle.update(self.game_speed) == False:
                self.obstacles.remove(obstacle)
        
        if self.player.update() == False:
            self.lose()
                   
    
    def run(self):
        while self.running:
            self.clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player.jump()

            self.update()
            self.draw()
            
            if self.distance%self.obstacles_gap == 0:
                self.obstacles.append(Obstacle())
                
            self.distance += self.game_speed

game = Game()
game.run()