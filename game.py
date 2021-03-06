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


import sys
import time

import pygame

import olpcgames.mesh as mesh
from sugar.presence import presenceservice


presenceService = presenceservice.get_instance()

from maze import Maze
from player import Player
from ghost import Ghost

MAZE_WIDTH = 33
MAZE_HEIGHT = 23

class PacmanGame:
    """Maze game controller.
    This class handles all of the game logic, event loop, mulitplayer, etc."""
    
    # Munsell color values http://wiki.laptop.org/go/Munsell
    N10	 = (255, 255, 255)
    N9p5 = (243, 243, 243)
    N9	 = (232, 232, 232)
    N8	 = (203, 203, 203)
    N7	 = (179, 179, 179)
    N6	 = (150, 150, 150)
    N5	 = (124, 124, 124)
    N4	 = ( 97,  97,  97)
    N3	 = ( 70,  70,  70)
    N2	 = ( 48,  48,  48)
    N1	 = ( 28,  28,  28)
    N0	 = (  0,   0,   0)
    EMPTY_COLOR = N1
    SOLID_COLOR = (40, 80, 65)
    TRAIL_COLOR = N10
    GOAL_COLOR  = (0x00, 0xff, 0x00)
    WIN_COLOR   = (0xff, 0xff, 0x00)

    def __init__(self, screen):

        # note what time it was when we first launched
        self.game_start_time = time.time()
        self.screen = screen
        self.pause = 0

        # compute the size of the tiles given the screen size, etc.
        size = self.screen.get_size()
        self.aspectRatio = size[0] / float(size[1])
        self.tileSize = min(size[0] / MAZE_WIDTH, size[1] / MAZE_HEIGHT)
        self.bounds = pygame.Rect((size[0] - self.tileSize * MAZE_WIDTH)/2,
                                  (size[1] - self.tileSize * MAZE_HEIGHT)/2,
                                  self.tileSize * MAZE_WIDTH,
                                  self.tileSize * MAZE_HEIGHT)
        self.outline = int(self.tileSize)
        self.player_size = self.tileSize - 4

        xoOwner = presenceService.get_owner()
        seed = int(time.time())
        # keep a list of all local players
        self.localplayers = []
        #print (xoOwner)
        # start with just one player
        player = Player(xoOwner, 1, 1, "yellow", self.player_size)
        self.localplayers.append(player)
        # plus some bonus players (all hidden to start with)
        self.localplayers.extend(player.bonusPlayers())

        # keep a dictionary of all remote players, indexed by handle
        self.remoteplayers = {}
        # keep a list of all players, local and remote, 
        self.allplayers = [] + self.localplayers
        # keep list of player images
        self.player_images = []

        self.ghosts = []
        redghost = Ghost ("red", seed, 19, 8, self.player_size)
        whiteghost = Ghost ("white", 2*seed, 13, 8, self.player_size)
        greenghost = Ghost ("green", 3*seed, 13, 11, self.player_size)
        orangeghost = Ghost ("orange", 4*seed, 19, 11, self.player_size)
        self.ghosts.append (whiteghost)
        self.ghosts.append (redghost)
        self.ghosts.append (greenghost)
        self.ghosts.append (orangeghost)
        
        # start with a small maze using a seed that will be different each time you play
        self.maze = Maze(seed, MAZE_WIDTH, MAZE_HEIGHT)
        self.reset()

        pygame.font.init()
        self.font = pygame.font.Font(None, 30)

        imgs = ["up", "down", "left", "right"]
        path = player.dirName + "pacman-" + player.color + "-open-%s.png"
        for t in imgs:
            img = pygame.image.load(path % t)
            img_t = pygame.transform.scale(img, (self.player_size, self.player_size))
            self.player_images.append(img_t)

        # support arrow keys, game pad arrows and game pad buttons
        # each set maps to a local player index and a direction
        self.arrowkeys = {
        # real key:     (localplayer index, ideal key)
        pygame.K_UP:    (0, pygame.K_UP),
        pygame.K_DOWN:  (0, pygame.K_DOWN),
        pygame.K_LEFT:  (0, pygame.K_LEFT),
        pygame.K_RIGHT: (0, pygame.K_RIGHT),
        pygame.K_KP8:   (1, pygame.K_UP),
        pygame.K_KP2:   (1, pygame.K_DOWN),
        pygame.K_KP4:   (1, pygame.K_LEFT),
        pygame.K_KP6:   (1, pygame.K_RIGHT),
        pygame.K_w:   (1, pygame.K_UP),
        pygame.K_s:   (1, pygame.K_DOWN),
        pygame.K_a:   (1, pygame.K_LEFT),
        pygame.K_d:   (1, pygame.K_RIGHT),
        pygame.K_KP9:   (2, pygame.K_UP),
        pygame.K_KP3:   (2, pygame.K_DOWN),
        pygame.K_KP7:   (2, pygame.K_LEFT),
        pygame.K_KP1:   (2, pygame.K_RIGHT), 
        }


    def game_running_time(self, newelapsed=None):
        return int(time.time() - self.game_start_time)

    def reset(self):
        """Reset the game state.  Everyone starts in the top-left.
        The goal starts in the bottom-right corner."""
        self.running = True
        self.level_start_time = time.time()
        self.finish_time = None
        for player in self.allplayers:
            player.reset()
        self.dirtyRect = None
        self.dirtyPoints = []
        #self.maze.map[self.maze.width-2][self.maze.height-2] = self.maze.GOAL -> no goal needed

        # clear and mark the whole screen as dirty
        self.screen.fill((0,0,0))
        self.markRectDirty(pygame.Rect(0,0,1200,900))

    def markRectDirty(self, rect):
        """Mark an area that needs to be redrawn.  This lets us
        play really big mazes without needing to re-draw the whole
        thing each frame."""
        if self.dirtyRect is None:
            self.dirtyRect = rect
        else:
            self.dirtyRect.union_ip(rect)

    def markPointDirty(self, pt):
        """Mark a single point that needs to be redrawn."""
        self.dirtyPoints.append(pt)

    def processEvent(self, event):
        """Process a single pygame event.  This includes keystrokes
        as well as multiplayer events from the mesh."""
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            if event.key == pygame.K_p:
                self.togglePause()
            elif self.arrowkeys.has_key(event.key):
                playernum, direction = self.arrowkeys[event.key]
                player = self.localplayers[playernum]
                player.hidden = False

                if direction == pygame.K_UP:
                    player.direction=(0,-1)
                    player.open.image = self.player_images[0]
                elif direction == pygame.K_DOWN:
                    player.direction=(0,1)
                    player.open.image = self.player_images[1]
                elif direction == pygame.K_LEFT:
                    player.direction=(-1,0)
                    player.open.image = self.player_images[2]
                elif direction == pygame.K_RIGHT:
                    player.direction=(1,0)
                    player.open.image = self.player_images[3]

                if len(self.remoteplayers)>0:
                    mesh.broadcast("move:%s,%d,%d,%d,%d" % (player.nick, player.position[0], player.position[1], player.direction[0], player.direction[1]))
        elif event.type == pygame.KEYUP:
            pass
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            pass
        elif event.type == mesh.CONNECT:
            print "Connected to the mesh."
        elif event.type == mesh.PARTICIPANT_ADD:
            buddy = mesh.get_buddy(event.handle)
            if event.handle == mesh.my_handle():
                print "Me:", buddy.props.nick, buddy.props.color
            else:
                print "Join:", buddy.props.nick, buddy.props.color
                player = Player(buddy)
                self.remoteplayers[event.handle] = player
                self.allplayers.append(player)
                self.allplayers.extend(player.bonusPlayers())
                self.markPointDirty(player.position)
                # send a test message to the new player
                mesh.broadcast("Welcome %s" % player.nick)
                # tell them which maze we are playing, so they can sync up
                mesh.send_to(event.handle, "maze:%d,%d,%d,%d" % (self.game_running_time(), self.maze.seed, self.maze.width, self.maze.height))
                for player in self.localplayers:
                    if not player.hidden:
                        mesh.send_to(event.handle, "move:%s,%d,%d,%d,%d" % (player.nick, player.position[0], player.position[1], player.direction[0], player.direction[1]))
        elif event.type == mesh.PARTICIPANT_REMOVE:
            if self.remoteplayers.has_key(event.handle):
                player = self.remoteplayers[event.handle]
                print "Leave:", player.nick
                self.markPointDirty(player.position)
                self.allplayers.remove(player)
                for bonusplayer in player.bonusPlayers():
                    self.markPointDirty(bonusplayer.position)
                    self.allplayers.remove(bonusplayer)
                del self.remoteplayers[event.handle]
        elif event.type == mesh.MESSAGE_UNI or event.type == mesh.MESSAGE_MULTI:
            buddy = mesh.get_buddy(event.handle)
            #print "Message from %s / %s: %s" % (buddy.props.nick, event.handle, event.content)
            if event.handle == mesh.my_handle():
                # ignore messages from ourself
                pass
            elif self.remoteplayers.has_key(event.handle):
                player = self.remoteplayers[event.handle]
                try:
                    self.handleMessage(player, event.content)
                except:
                    print "Error handling message: %s\n%s" % (event, sys.exc_info())
            else:
                print "Message from unknown buddy?"
        """else:
            print "Unknown event:", event"""

    def handleMessage(self, player, message):
        """Handle a message from a player on the mesh.
            We try to be forward compatible with new versions of Maze by allowing messages to
            have extra stuff at the end and ignoring unrecognized messages.
            We allow some messages to contain a different nick than the message's source player
            to support bonus players on that player's XO.
            The valid messages are:
            maze:running_time,seed,width,height
                A player has a differen maze.
                The one that has been running the longest will force all other players to use that maze.
                This way new players will join the existing game properly.
            move:nick,x,y,dx,dy
                A player's at x,y is now moving in direction dx,dy
            finish:nick,elapsed
                A player has finished the maze
        """
        # ignore messages from myself
        if player in self.localplayers:
            return
        if message.startswith("move:"):
            # a player has moved
            nick,x,y,dx,dy = message[5:].split(",")[:5]
            player = player.bonusPlayer(nick)
            player.hidden = False
            self.markPointDirty(player.position)
            player.position = (int(x),int(y))
            player.direction = (int(dx),int(dy))
            self.markPointDirty(player.position)
        elif message.startswith("maze:"):
            # someone has a different maze than us
            running_time,seed,width,height = map(lambda x: int(x), message[5:].split(",")[:4])
            # is that maze older than the one we're already playing?
            # note that we use elapsed time instead of absolute time because
            # people's clocks are often set to something totally wrong
            if self.game_running_time() < running_time:
                # make note of the earlier time that the game really started (before we joined)
                self.game_start_time = time.time() - running_time
                # use the new seed
                self.maze = Maze(seed, width, height)
                self.reset()
        elif message.startswith("finish:"):
            # someone finished the maze
            nick, elapsed = message[7:].split(",")[:2]
            player = player.bonusPlayer(nick)
            player.elapsed = float(elapsed)
            self.markPointDirty(player.position)
        else:
            # it was something I don't recognize...
            print "Message from %s: %s" % (player.nick, message)
            pass

    def arrowKeysPressed(self):
        keys = pygame.key.get_pressed()
        for key in self.allkeys:
            if keys[key]:
                return True
        return False

    def togglePause(self):
      if (self.pause == 1):
          self.pause = 0
          self.markRectDirty(pygame.Rect(0,0,1200,900)) # repaint
      else:
          self.pause = 1

    def run(self):
        """Run the main loop of the game."""
        # lets draw once before we enter the event loop
        self.draw()
        pygame.display.flip()
        clock = pygame.time.Clock()

        while self.running:

            # process all queued events
            for event in pygame.event.get():
                self.processEvent(event)

            if (self.pause == 0):
                self.animate(self.maze)
                self.draw()
            else: # repaint pause information frequently to prevent empty window after minimizing
                font = pygame.font.Font(None, 100)
                fg = (248,234,32)
                text = "Press p to resume the game"
                textimg = font.render(text, 1, fg)
                textwidth, textheight = font.size(text)
                rect = pygame.Rect(100, 200, textwidth, textheight)
                pygame.draw.rect (self.screen, self.SOLID_COLOR, rect)
                self.screen.blit(textimg, rect)

            pygame.display.flip()


            # this keeps the speed reasonable and limits cpu usage
            clock.tick(3);

    def animate(self, maze):
        """Animate one frame of action."""
        for player in self.allplayers:
            if (player.supertime > 0):
              player.supertime -= 1
            oldposition = player.position
            newposition = player.animate(self.maze)
            if oldposition != newposition:
                self.markPointDirty(oldposition)
                self.markPointDirty(newposition)
                if player in self.localplayers:
                    self.maze.map[player.previous[0]][player.previous[1]] = self.maze.SEEN

        finished = 1
        for x in range(0, self.maze.width):
            for y in range(0, self.maze.height):
                if (self.maze.map[x][y] == self.maze.EMPTY):
                    finished = 0
                    break;
        if (finished == 1):
            # reset maze
            maze.generate()
            # reset players
            for player in self.allplayers:
              player.position = player.startposition
            # reset ghosts
            for ghost in self.ghosts:
              ghost.reset ();
              ghost.position = ghost.startposition
            # stop game
            self.togglePause ()
            # repaint
            self.markRectDirty(pygame.Rect(0,0,1200,900))

        self.checkGhostPositions () # checks if player runs into ghost

        for ghost in self.ghosts:
          self.animateGhost (ghost, maze)

        self.checkGhostPositions()  # checks if ghost runs into player



    def animateGhost (self, ghost, maze):
          # ghosts follow any pacman they see
          x = ghost.position[0]

          # is there a ghost to the left?
          while x > 0:
            x = x - 1
            if (maze.map[x][ghost.position[1]] == maze.SOLID): # ghosts cannot see through walls, this would be unfair :)
              break
            for player in self.allplayers:
              if (player.hidden):
                continue
              if (player.position == (x, ghost.position[1])):
                ghost.direction = (-1, 0)
                self.markPointDirty (ghost.position)
                ghost.move (ghost.direction, maze)
                self.markPointDirty (ghost.position)
                return

          # is there a ghost to the right?
          x = ghost.position[0]
          while x < maze.width:
            x = x + 1
            if (maze.map[x][ghost.position[1]] == maze.SOLID): # ghosts cannot see through walls, this would be unfair :)
              break
            for player in self.allplayers:
              if (player.hidden):
                continue
              if (player.position == (x, ghost.position[1])):
                ghost.direction = (1, 0)
                self.markPointDirty (ghost.position)
                ghost.move (ghost.direction, maze)
                self.markPointDirty (ghost.position)
                return

          # is there a ghost to the top?
          y = ghost.position[1]
          while y > 0:
            y = y - 1
            if (maze.map[ghost.position[0]][y] == maze.SOLID): # ghosts cannot see through walls, this would be unfair :)
              break
            for player in self.allplayers:
              if (player.hidden):
                continue
              if (player.position == (ghost.position[0], y)):
                ghost.direction = (0, -1)
                self.markPointDirty (ghost.position)
                ghost.move (ghost.direction, maze)
                self.markPointDirty (ghost.position)
                return

          # is there a ghost to the right?
          y = ghost.position[1]
          while y < maze.height:
            y = y + 1
            if (maze.map[ghost.position[0]][y] == maze.SOLID): # ghosts cannot see through walls, this would be unfair :)
              break
            for player in self.allplayers:
              if (player.hidden):
                continue
              if (player.position == (ghost.position[0], y)):
                ghost.direction = (0, 1)
                self.markPointDirty (ghost.position)
                ghost.move (ghost.direction, maze)
                self.markPointDirty (ghost.position)
                return

          oldposition = ghost.position
          ghost.animate(self.maze)
          newposition = ghost.position
          if oldposition != newposition:
                self.markPointDirty(oldposition)
                self.markPointDirty(newposition)



    def checkGhostPositions (self):
      # is there a ghost hitting a player?
          for player in self.allplayers:
            if (player.hidden):
              continue
            for ghost in self.ghosts:
              if (ghost.position == player.position):
                if (player.supertime > 0):
                  ghost.reset ();
                  ghost.position = ghost.startposition
                else:
                  player.position = player.startposition
                  self.markPointDirty (player.position)
                  player.score = int(player.score/2)
                  player.supertime = 10 # make sure the player will not be eaten again in the next 10 moves
                break;

    def draw(self):
        """Draw the current state of the game.
        This makes use of the dirty rectangle to reduce CPU load."""
        if self.dirtyRect is None and len(self.dirtyPoints)==0:
            return

        def drawPoint(x,y):
            rect = pygame.Rect(self.bounds.x + x*self.tileSize, self.bounds.y + y*self.tileSize, self.tileSize, self.tileSize)
            tile = self.maze.map[x][y]
            if tile == self.maze.EMPTY:
                pygame.draw.rect(self.screen, self.EMPTY_COLOR, rect, 0)
                dot = rect.inflate(-self.outline/2, -self.outline/2)
                pygame.draw.ellipse(self.screen, self.TRAIL_COLOR, dot, 0)
            elif tile == self.maze.SOLID:
                pygame.draw.rect(self.screen, self.SOLID_COLOR, rect, 0)
            elif tile == self.maze.SEEN:
                pygame.draw.rect(self.screen, self.EMPTY_COLOR, rect, 0)
            else:
                pygame.draw.rect(self.screen, (0xff, 0x00, 0xff), rect, 0)

        # re-draw the dirty rectangle
        if self.dirtyRect is not None:
            # compute the area that needs to be redrawn
            left = max(0, self.dirtyRect.left)
            right = min(self.maze.width, self.dirtyRect.right)
            top = max(0, self.dirtyRect.top)
            bottom = min(self.maze.height, self.dirtyRect.bottom)

            # loop over the dirty rect and draw
            for x in range(left, right):
                for y in range(top, bottom):
                    drawPoint(x,y)

        # re-draw the dirty points
        for x,y in self.dirtyPoints:
            drawPoint(x,y)

        # draw all players
        for player in self.allplayers:
            if not player.hidden:
                player.draw(self.screen, self.bounds, self.tileSize)

        #draw all ghosts
        for ghost in self.ghosts:
          ghost.draw (self.screen, self.bounds, self.tileSize)

        # clear the dirty rect so nothing will be drawn until there is a change
        self.dirtyRect = None
        self.dirtyPoints = []

        # draw score
        fg = (21, 203, 35)
        text = ""
        for player in self.allplayers:
            if not player.hidden:
                text += player.nick + ": " + str(player.score) + "  "
        textimg = self.font.render(text, 1, fg)
        textwidth, textheight = self.font.size(text)
        rect = pygame.Rect(25, 15, textwidth, textheight)
        pygame.draw.rect (self.screen, self.SOLID_COLOR, rect)
        self.screen.blit(textimg, rect)

def main():
    """Run a game of Maze."""
    # ask pygame how big the screen is, leaving a little room for the toolbar
    toolbarheight = 55
    pygame.display.init()
    videoinfo = pygame.display.Info()
    width = videoinfo.current_w
    height = videoinfo.current_h - toolbarheight
    screen = pygame.display.set_mode((width, height))

    game = PacmanGame(screen)
    game.run()

if __name__ == '__main__':
    main()
