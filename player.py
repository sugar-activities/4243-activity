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
from pygame import sprite as sprite
from utils import get_dir

class Player:
    def __init__(self, buddy, startx, starty, color = 'green', size=36):
        self.buddy = buddy
        self.nick = buddy.props.nick
        self.score = 0
        self.color = color
        self.size = size
        self.startposition = (startx, starty)
        self.hidden = False
        self.bonusplayers = None
        self.opensprites = sprite.RenderUpdates()
        self.closedsprites = sprite.RenderUpdates()
        self.dirName = get_dir()
        self.open = sprite.Sprite()
        self.closed = sprite.Sprite()
        self._path = self.dirName + "pacman-" + self.color
        img = pygame.image.load(self._path + "-open-right.png")
        self.open.image = pygame.transform.scale(img, (self.size, self.size))
        img = pygame.image.load(self._path + "-closed.png")
        self.closed.image = pygame.transform.scale(img, (self.size, self.size))
        self.opensprites.add(self.open)
        self.closedsprites.add(self.closed)
        self.mouthClosed = 1
        self.supertime = 0
        self.reset()

    def draw(self, screen, bounds, size):
        rect = pygame.Rect(bounds.x+self.position[0]*size, bounds.y+self.position[1]*size, size, size)
        #border = size / 10.
        #center = rect.inflate(-border*2, -border*2)
        if (self.mouthClosed == 1):
          self.closed.rect = rect
          self.closedsprites.draw(screen)
          self.mouthClosed = 0
        else:
          self.open.rect = rect
          self.opensprites.draw(screen)
          self.mouthClosed = 1

    def reset(self):
        self.direction = (0,0)
        self.position = self.startposition
        self.previous = (1,1)
        self.elapsed = None
    
    def animate(self, maze):
        # if the player finished the maze, then don't move
        if self.direction == (0,0):
            return self.position
        if self.canGo(self.direction, maze):
            self.move(self.direction, maze)
        else:
            self.direction = (0,0)
            self.mouthClosed = 1
        return self.position
    
    def move(self, direction, maze):
        """Move the player in a given direction (deltax,deltay)"""
        newposition = (self.position[0]+direction[0], self.position[1]+direction[1])
        self.previous = self.position
        self.position = newposition
        if (maze.map [newposition[0]][newposition[1]] == maze.EMPTY):
          self.score += 1

    def canGo(self, direction, maze):
        """Can the player go in this direction without bumping into something?"""
        newposition = (self.position[0]+direction[0], self.position[1]+direction[1])
        return maze.validMove(newposition[0], newposition[1])

    def cameFrom(self, direction):
        """Note the position/direction that we just came from."""
        return self.previous == (self.position[0]+direction[0], self.position[1]+direction[1])

    def bonusPlayers(self):
        if self.bonusplayers is None:
            self.bonusplayers = []
            self.bonusplayers.append(Player(self.buddy, 1, 21, 'green', self.size))
            self.bonusplayers.append(Player(self.buddy, 31, 21, 'blue', self.size))
            #self.bonusplayers.append(Player(self.buddy, 31, 1, '', self.size))
            count = 2
            for player in self.bonusplayers:
                player.nick = self.nick + "-%d" % count
                player.hidden = True
                count += 1

        return self.bonusplayers

    def bonusPlayer(self, nick):
        if nick == self.nick:
            return self
        for bonusplayer in self.bonusPlayers():
            if bonusplayer.nick == nick:
                return bonusplayer

