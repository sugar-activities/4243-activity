# Pacman.activity
# A pac-man clone for the XO laptop.
#
# Thanks to Raphael Reinig for testing
#
# Copyright (C) 2008  Tristan Hoffmann, tristanhoffmann@boxbe.com
# Thanks to Joshua Minor, I used a lot of code from his Maze.activity
#
# This file is part of Pacman.activity
#
#     Pacman.activity is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Pacman.activity is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Pacman.activity.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import random
from pygame import sprite as sprite
from utils import get_dir

class Ghost:
    def __init__(self, color, seed, x, y, size=36):
        self.seed = seed
        self.generator = random.Random(seed)
        self.color = color
        self.size = size
        self.sprites = sprite.RenderUpdates()
        self.sprite = sprite.Sprite()
        self.dirName = get_dir()
        self._path = self.dirName + "ghost_" + self.color + ".png"
        img = pygame.image.load(self._path)
        self.sprite.image = pygame.transform.scale(img, (self.size, self.size))
        self.sprites.add(self.sprite)
        self.position = (x, y)
        self.startposition = self.position
        self.reset()

    def draw(self, screen, bounds, size):
        rect = pygame.Rect(bounds.x+self.position[0]*size, bounds.y+self.position[1]*size, size, size)
        self.sprite.rect = rect
        self.sprites.draw(screen)

    def reset(self):
        self.direction = (0,0)
        self.previous = self.startposition
        self.elapsed = None
    
    def animate(self, maze):
          directions = []
          if (self.canGo ((0,1), maze)):
            directions.append ((0,1))
            if (self.direction != (0,-1)):
              directions.append ((0,1)) # raise the probability that the ghost doesn't go back

          if (self.canGo ((0,-1), maze)):
            directions.append ((0,-1))
            if (self.direction != (0,1)):
              directions.append ((0,-1)) # raise the probability that the ghost doesn't go back

          if (self.canGo ((1,0), maze)):
            directions.append ((1,0))
            if (self.direction != (-1,0)):
              directions.append ((1,0)) # raise the probability that the ghost doesn't go back

          if (self.canGo ((-1,0), maze)):
            directions.append ((-1,0))
            if (self.direction != (1,0)):
              directions.append ((-1,0)) # raise the probability that the ghost doesn't go back

          if (self.canGo (self.direction, maze)): # don't go back if we can go forward
              backDirection = (-self.direction[0], -self.direction[1])
              directions.append (self.direction) # raise the probability that the ghost keeps it's direction
              directions.remove (backDirection) # remove possibility to go back

          self.direction = self.generator.choice (directions)
          self.move (self.direction, maze)


    def move(self, direction, maze):
        """Move the ghost in a given direction (deltax,deltay)"""
        if (direction[0] > 1):
          print "Direction[0] is greater than 1!"
        if (direction[1] > 1):
          print "Direction[1] is greater than 1!"
        if (direction == (1, 1)):
          print "Direction is (1, 1)"
        newposition = (self.position[0]+direction[0], self.position[1]+direction[1])
        self.position = newposition

    def canGo(self, direction, maze):
        """Can the ghost go in this direction without bumping into something?"""
        if (direction == (0,0)):
          return 0 # make sure the ghost isn't sleeping :)
        newposition = (self.position[0]+direction[0], self.position[1]+direction[1])
        return maze.validMove(newposition[0], newposition[1])

