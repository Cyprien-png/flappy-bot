import pygame
from Player import Player
from Obstacle import Obstacle
import neat
import os
import pickle


class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 500))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.obstacles = []
        self.obstacles_gap = 400
        self.game_speed = 2
        self.distance = 0
        self.lose_count = 0
        self.passed_obstacles = 0
        
    def score(self):
        return self.passed_obstacles
        
    def lose(self):
        self.lose_count += 1
        # self.reset()
        self.screen.fill((255, 0, 0))
        pygame.display.flip()
        
    def reset(self):
        self.lose_count = 0
        self.player.position_y = pygame.display.get_surface().get_size()[1] / 2
        self.player.velocity = 0
        self.distance = 0
        self.passed_obstacles = 0
        # empty the obstacles list
        self.obstacles = []
        
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
                   
    
    def train_ai(self, genome, config, train=False):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        while self.running:
            
            # if train == False:
                # self.clock.tick(120)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     quit()
                   
                   
            next_obstacles = []
     
            for obstacle in self.obstacles:
                if obstacle.position_x > self.player.position_x - obstacle.width - self.player.width: 
                    next_obstacles.append(obstacle)
            
            
            if  len(next_obstacles) > 0:
                next_obstacle_height = next_obstacles[0].hole_height
                next_obstacle_distance = next_obstacles[0].position_x - self.player.position_x
                next_obstacle_height_min = next_obstacle_height - next_obstacles[0].hole_size / 2
                next_obstacle_height_max = next_obstacle_height + next_obstacles[0].hole_size / 2
                if len(next_obstacles) > 1:
                    next_obstacle_height_2 = next_obstacles[1].hole_height
                    next_obstacle_distance_2 = next_obstacles[1].position_x - self.player.position_x
                    next_obstacle_height_min_2 = next_obstacle_height_2 - next_obstacles[1].hole_size / 2
                    next_obstacle_height_max_2 = next_obstacle_height_2 + next_obstacles[1].hole_size / 2
                else:
                    next_obstacle_height_2 = pygame.display.get_surface().get_size()[1] / 2
                    next_obstacle_height_min_2 = pygame.display.get_surface().get_size()[1] / 2 - 100
                    next_obstacle_height_max_2 = pygame.display.get_surface().get_size()[1] / 2 + 100
                    next_obstacle_distance_2 = pygame.display.get_surface().get_size()[0]
            else :
                next_obstacle_height = pygame.display.get_surface().get_size()[1] / 2
                next_obstacle_height_min = pygame.display.get_surface().get_size()[1] / 2 - 100
                next_obstacle_height_max = pygame.display.get_surface().get_size()[1] / 2 + 100
                next_obstacle_distance = pygame.display.get_surface().get_size()[0]
                next_obstacle_height_2 = pygame.display.get_surface().get_size()[1] / 2
                next_obstacle_height_min_2 = pygame.display.get_surface().get_size()[1] / 2 - 100
                next_obstacle_height_max_2 = pygame.display.get_surface().get_size()[1] / 2 + 100
                next_obstacle_distance_2 = pygame.display.get_surface().get_size()[0]
                
            # print(self.player.position_y, next_obstacle_height_min, next_obstacle_height_max, next_obstacle_distance)
            output = net.activate((self.player.position_y,  next_obstacle_height_min, next_obstacle_height_max, next_obstacle_distance, next_obstacle_height_min_2, next_obstacle_height_max_2, next_obstacle_distance_2))
            decision = output.index(max(output))
            
            if decision == 0:
                pass
            else :
                self.player.jump()
 
            self.update()
            if train == False:
                self.draw()
            
            if self.distance%self.obstacles_gap == 0:
                self.obstacles.append(Obstacle())
                
            self.distance += self.game_speed
            
            if self.lose_count > 0 or self.score() > 10000000:
                self.calculate_fitness(genome, self.distance, self.passed_obstacles)
                break

    def calculate_fitness(self, genome, distance, passed_obstacles):
        genome.fitness = distance + passed_obstacles * 100


def eval_genomes(genomes, config):    


    for genome_id, genome in genomes:
        genome.fitness = 0
        game = Game()
        
        # Create a new game for each genome
        
        force_quit = game.train_ai(genome, config, True)
        if force_quit:
            quit()


def test_ai(config):
    with open("best.genome", "rb") as f:
        genome = pickle.load(f)
    game = Game()
    game.train_ai(genome, config)
    quit()

def run_neat(config):

    if not os.path.exists("checkpoints"):
        os.makedirs("checkpoints")
        
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1, None, "checkpoints/"))


    winner = p.run(eval_genomes, 300)
    with open("best.genome", "wb") as f:
        pickle.dump(winner, f)

    

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
# run_neat(config)
test_ai(config)
