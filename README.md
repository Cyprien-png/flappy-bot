# Flappy bot
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Description
This is a Flappy Bird like game made with pygame. The game is playable by a human or by a bot. The bot is an AI that uses a genetic algorithm to learn how to play the game.

The code is very messy and not optimized at all. I worked on this project few hours in the only purpose of learning about genetic algorithms without any prior knowledge about them and pygame.

## Run the game
If you still want to run the game, you can do it by running the following command:
```bash
pip install neat-python pygame
```

To play the game:
```bash
py Game.py
# Press the space bar to jump
```

To run the AI:
```bash
py AI.py
```

## The AI
The "best.genome" file contains the best genome which is the result of the genetic algorithm.

This genome has 1 neural network which is composed by 7 inputs, 4 hidden layer and 2 outputs. each frame, the game will feed the AI neural network with the inputs and get the outputs. 

### Inputs
- The bird's y position
- The bottom y position of the hole in the next pipe
- The top y position of the hole in the next pipe
- The distance between the bird and the next pipe
- The bottom y position of the hole in the second pipe
- The top y position of the hole in the second pipe
- The distance between the bird and the second pipe

### Outputs
As output the neural network will return two values. These values are interpreted as follows:
- If the first value is greater than the second value, the bird won't do anything
- If the second value is greater or equal to the first value, the bird will jump

### Fitness
The fitness is like a "reward" that the AI will get if it does something good. In this case, the fitness is equal to distance that the bird has traveled plus an additional bonus if the bird passes some pipes.
