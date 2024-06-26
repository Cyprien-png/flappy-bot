import pygame
from Player import Player
from Obstacle import Obstacle

class Game:
    
    screen = pygame.display.set_mode((1280, 500))
    clock = pygame.time.Clock()
    running = True
    player = Player()
    obstacles = []
    obstacles_gap = 400
    game_speed = 2
    passed_obstacles = 0

    
    distance = 0
    lose_count = 0
    
    def __init__(self):
        pygame.init()
        
    def score(self):
        return self.passed_obstacles
        
    def lose(self):
        self.lose_count += 1
        self.player.position_y = pygame.display.get_surface().get_size()[1] / 2
        self.player.velocity = 0
        self.distance = 0
        self.obstacles = []
        self.passed_obstacles = 0

        
    def check_collision(self):
        player = self.player
        obstacles = self.obstacles
        
        for obstacle in obstacles:
            if player.position_x + player.width/2 > obstacle.position_x and player.position_x - player.width/2 < obstacle.position_x + obstacle.width:
                if player.position_y - player.width/2 < obstacle.hole_height or player.position_y + player.width/2 > obstacle.hole_height + obstacle.hole_size:
                    self.lose()
                    break
        
    def draw(self):
        obstacles = self.obstacles
        
        # clear screen
        self.screen.fill((149, 203, 231 ))

        # draw game objects
        for obstacle in obstacles:
            obstacle.draw(self.screen)
        
        self.player.draw(self.screen)
        
        # draw game text score
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.score()), 1, (255, 255, 255))
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
            if obstacle.position_x == self.player.position_x:
                self.passed_obstacles += 1
        
        if self.player.update() == False:
            self.lose()
            
        # check collision
        self.check_collision()
                   
    
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