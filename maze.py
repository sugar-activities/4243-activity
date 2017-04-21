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

from pygame import Rect

class Maze:
    SOLID = 0 #wall
    EMPTY = 1 #where pacman can move
    SEEN = 2 #already eaten

    def __init__(self, seed, width, height):
        # use the seed given to us to make a pseudo-random number generator
        # we will use that to generate the maze, so that other players can
        # generate the exact same maze given the same seed.
        print "Generating maze:%d,%d,%d" % (seed, width, height)
        self.width, self.height = width, height
        self.bounds = Rect(0,0,width,height)

        self.generate ()


    def generate (self):
        self.map = []
        for x in range(0, self.width-1):
           if (x == 0):
              self.map.append([self.SOLID] * self.height) # draw left border
           else:
              self.map.append([self.EMPTY] * self.height)
        self.map.append([self.SOLID] * self.height) # draw right border

        for x in range(1, self.width-1):
            self.map[x][0] = self.SOLID # draw top border
            self.map[x][self.height - 1] = self.SOLID # draw bottom border

        self.map[8][1] = self.SOLID
        self.map[24][1] = self.SOLID
        self.map[2][2] = self.SOLID
        self.map[3][2] = self.SOLID
        self.map[4][2] = self.SOLID
        self.map[5][2] = self.SOLID
        self.map[6][2] = self.SOLID
        self.map[8][2] = self.SOLID
        self.map[10][2] = self.SOLID
        self.map[11][2] = self.SOLID
        self.map[12][2] = self.SOLID
        self.map[13][2] = self.SOLID
        self.map[14][2] = self.SOLID
        self.map[15][2] = self.SOLID
        self.map[16][2] = self.SOLID
        self.map[17][2] = self.SOLID
        self.map[18][2] = self.SOLID
        self.map[19][2] = self.SOLID
        self.map[20][2] = self.SOLID
        self.map[21][2] = self.SOLID
        self.map[22][2] = self.SOLID
        self.map[24][2] = self.SOLID
        self.map[26][2] = self.SOLID
        self.map[27][2] = self.SOLID
        self.map[28][2] = self.SOLID
        self.map[29][2] = self.SOLID
        self.map[30][2] = self.SOLID
        self.map[2][3] = self.SOLID
        self.map[30][3] = self.SOLID
        self.map[2][4] = self.SOLID
        self.map[4][4] = self.SOLID
        self.map[6][4] = self.SOLID
        self.map[8][4] = self.SOLID
        self.map[9][4] = self.SOLID
        self.map[10][4] = self.SOLID
        self.map[12][4] = self.SOLID
        self.map[13][4] = self.SOLID
        self.map[14][4] = self.SOLID
        self.map[15][4] = self.SOLID
        self.map[16][4] = self.SOLID
        self.map[17][4] = self.SOLID
        self.map[18][4] = self.SOLID
        self.map[19][4] = self.SOLID
        self.map[20][4] = self.SOLID
        self.map[22][4] = self.SOLID
        self.map[23][4] = self.SOLID
        self.map[24][4] = self.SOLID
        self.map[26][4] = self.SOLID
        self.map[28][4] = self.SOLID
        self.map[30][4] = self.SOLID
        self.map[4][5] = self.SOLID
        self.map[6][5] = self.SOLID
        self.map[26][5] = self.SOLID
        self.map[28][5] = self.SOLID
        self.map[1][6] = self.SOLID
        self.map[2][6] = self.SOLID
        self.map[4][6] = self.SOLID
        self.map[6][6] = self.SOLID
        self.map[8][6] = self.SOLID
        self.map[9][6] = self.SOLID
        self.map[10][6] = self.SOLID
        self.map[11][6] = self.SOLID
        self.map[12][6] = self.SOLID
        self.map[14][6] = self.SOLID
        self.map[15][6] = self.SOLID
        self.map[16][6] = self.SOLID
        self.map[17][6] = self.SOLID
        self.map[18][6] = self.SOLID
        self.map[20][6] = self.SOLID
        self.map[21][6] = self.SOLID
        self.map[22][6] = self.SOLID
        self.map[23][6] = self.SOLID
        self.map[24][6] = self.SOLID
        self.map[26][6] = self.SOLID
        self.map[28][6] = self.SOLID
        self.map[30][6] = self.SOLID
        self.map[31][6] = self.SOLID
        self.map[4][7] = self.SOLID
        self.map[12][7] = self.SOLID
        self.map[20][7] = self.SOLID
        self.map[28][7] = self.SOLID
        self.map[2][8] = self.SOLID
        self.map[4][8] = self.SOLID
        self.map[6][8] = self.SOLID
        self.map[7][8] = self.SOLID
        self.map[8][8] = self.SOLID
        self.map[9][8] = self.SOLID
        self.map[10][8] = self.SOLID
        self.map[12][8] = self.SOLID
        self.map[14][8] = self.SOLID
        self.map[15][8] = self.SOLID
        self.map[16][8] = self.SOLID
        self.map[17][8] = self.SOLID
        self.map[18][8] = self.SOLID
        self.map[20][8] = self.SOLID
        self.map[22][8] = self.SOLID
        self.map[23][8] = self.SOLID
        self.map[24][8] = self.SOLID
        self.map[25][8] = self.SOLID
        self.map[26][8] = self.SOLID
        self.map[28][8] = self.SOLID
        self.map[30][8] = self.SOLID
        self.map[2][9] = self.SOLID
        self.map[10][9] = self.SOLID
        self.map[12][9] = self.SOLID
        self.map[20][9] = self.SOLID
        self.map[22][9] = self.SOLID
        self.map[30][9] = self.SOLID
        self.map[2][10] = self.SOLID
        self.map[4][10] = self.SOLID
        self.map[5][10] = self.SOLID
        self.map[6][10] = self.SOLID
        self.map[7][10] = self.SOLID
        self.map[8][10] = self.SOLID
        self.map[10][10] = self.SOLID
        self.map[12][10] = self.SOLID
        self.map[13][10] = self.SOLID
        self.map[14][10] = self.SOLID
        self.map[15][10] = self.SOLID
        self.map[16][10] = self.SOLID
        self.map[17][10] = self.SOLID
        self.map[18][10] = self.SOLID
        self.map[19][10] = self.SOLID
        self.map[20][10] = self.SOLID
        self.map[22][10] = self.SOLID
        self.map[24][10] = self.SOLID
        self.map[25][10] = self.SOLID
        self.map[26][10] = self.SOLID
        self.map[27][10] = self.SOLID
        self.map[28][10] = self.SOLID
        self.map[30][10] = self.SOLID
        self.map[2][11] = self.SOLID
        self.map[10][11] = self.SOLID
        self.map[12][11] = self.SOLID
        self.map[20][11] = self.SOLID
        self.map[22][11] = self.SOLID
        self.map[30][11] = self.SOLID
        self.map[2][12] = self.SOLID
        self.map[3][12] = self.SOLID
        self.map[4][12] = self.SOLID
        self.map[6][12] = self.SOLID
        self.map[8][12] = self.SOLID
        self.map[10][12] = self.SOLID
        self.map[12][12] = self.SOLID
        self.map[14][12] = self.SOLID
        self.map[15][12] = self.SOLID
        self.map[16][12] = self.SOLID
        self.map[17][12] = self.SOLID
        self.map[18][12] = self.SOLID
        self.map[20][12] = self.SOLID
        self.map[22][12] = self.SOLID
        self.map[24][12] = self.SOLID
        self.map[26][12] = self.SOLID
        self.map[28][12] = self.SOLID
        self.map[29][12] = self.SOLID
        self.map[30][12] = self.SOLID
        self.map[6][13] = self.SOLID
        self.map[8][13] = self.SOLID
        self.map[24][13] = self.SOLID
        self.map[26][13] = self.SOLID
        self.map[2][14] = self.SOLID
        self.map[3][14] = self.SOLID
        self.map[4][14] = self.SOLID
        self.map[5][14] = self.SOLID
        self.map[6][14] = self.SOLID
        self.map[8][14] = self.SOLID
        self.map[8][14] = self.SOLID
        self.map[10][14] = self.SOLID
        self.map[12][14] = self.SOLID
        self.map[13][14] = self.SOLID
        self.map[14][14] = self.SOLID
        self.map[15][14] = self.SOLID
        self.map[16][14] = self.SOLID
        self.map[17][14] = self.SOLID
        self.map[18][14] = self.SOLID
        self.map[19][14] = self.SOLID
        self.map[20][14] = self.SOLID
        self.map[22][14] = self.SOLID
        self.map[24][14] = self.SOLID
        self.map[26][14] = self.SOLID
        self.map[27][14] = self.SOLID
        self.map[28][14] = self.SOLID
        self.map[29][14] = self.SOLID
        self.map[30][14] = self.SOLID
        self.map[10][15] = self.SOLID
        self.map[22][15] = self.SOLID
        self.map[2][16] = self.SOLID
        self.map[3][16] = self.SOLID
        self.map[4][16] = self.SOLID
        self.map[5][16] = self.SOLID
        self.map[6][16] = self.SOLID
        self.map[7][16] = self.SOLID
        self.map[8][16] = self.SOLID
        self.map[10][16] = self.SOLID
        self.map[12][16] = self.SOLID
        self.map[13][16] = self.SOLID
        self.map[14][16] = self.SOLID
        self.map[15][16] = self.SOLID
        self.map[16][16] = self.SOLID
        self.map[17][16] = self.SOLID
        self.map[18][16] = self.SOLID
        self.map[19][16] = self.SOLID
        self.map[20][16] = self.SOLID
        self.map[22][16] = self.SOLID
        self.map[24][16] = self.SOLID
        self.map[25][16] = self.SOLID
        self.map[26][16] = self.SOLID
        self.map[27][16] = self.SOLID
        self.map[28][16] = self.SOLID
        self.map[29][16] = self.SOLID
        self.map[30][16] = self.SOLID
        self.map[4][17] = self.SOLID
        self.map[28][17] = self.SOLID
        self.map[1][18] = self.SOLID
        self.map[2][18] = self.SOLID
        self.map[4][18] = self.SOLID
        self.map[6][18] = self.SOLID
        self.map[7][18] = self.SOLID
        self.map[8][18] = self.SOLID
        self.map[10][18] = self.SOLID
        self.map[12][18] = self.SOLID
        self.map[13][18] = self.SOLID
        self.map[14][18] = self.SOLID
        self.map[15][18] = self.SOLID
        self.map[16][18] = self.SOLID
        self.map[17][18] = self.SOLID
        self.map[18][18] = self.SOLID
        self.map[19][18] = self.SOLID
        self.map[20][18] = self.SOLID
        self.map[22][18] = self.SOLID
        self.map[24][18] = self.SOLID
        self.map[25][18] = self.SOLID
        self.map[26][18] = self.SOLID
        self.map[28][18] = self.SOLID
        self.map[30][18] = self.SOLID
        self.map[31][18] = self.SOLID
        self.map[4][19] = self.SOLID
        self.map[10][19] = self.SOLID
        self.map[22][19] = self.SOLID
        self.map[28][19] = self.SOLID
        self.map[2][20] = self.SOLID
        self.map[3][20] = self.SOLID
        self.map[4][20] = self.SOLID
        self.map[5][20] = self.SOLID
        self.map[6][20] = self.SOLID
        self.map[7][20] = self.SOLID
        self.map[8][20] = self.SOLID
        self.map[10][20] = self.SOLID
        self.map[12][20] = self.SOLID
        self.map[13][20] = self.SOLID
        self.map[14][20] = self.SOLID
        self.map[15][20] = self.SOLID
        self.map[16][20] = self.SOLID
        self.map[17][20] = self.SOLID
        self.map[18][20] = self.SOLID
        self.map[19][20] = self.SOLID
        self.map[20][20] = self.SOLID
        self.map[22][20] = self.SOLID
        self.map[24][20] = self.SOLID
        self.map[25][20] = self.SOLID
        self.map[26][20] = self.SOLID
        self.map[27][20] = self.SOLID
        self.map[28][20] = self.SOLID
        self.map[29][20] = self.SOLID
        self.map[30][20] = self.SOLID
        self.map[10][21] = self.SOLID
        self.map[22][21] = self.SOLID

    def validMove(self, x, y):
        return self.bounds.collidepoint(x,y) and self.map[x][y]!=self.SOLID
