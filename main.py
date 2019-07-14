from graphics.window import Window
from game.player import Player
from game.apples import Apples
from random import randint
import pygame
import sys
import os


class Main:
    def __init__(self, snakes, apples, speed, autoplay):
        if getattr(sys, 'frozen', False):
            CurrentPath = sys._MEIPASS
        else:
            CurrentPath = os.path.dirname(__file__)
        self.speed = speed
        self.window = Window()
        self.apples = Apples(apples)
        self.go = False
        self.goCount = 0
        fontFile = os.path.join(CurrentPath, "freesansbold.ttf")
        if not os.path.exists(fontFile):
            fontFile = "freesansbold.ttf"
        self.font = pygame.font.Font(fontFile, 240)
        self.font.set_bold(True)
        self.fontSmall = pygame.font.Font(fontFile, 120)
        self.fontSmall.set_bold(True)
        self.textSurf = None
        self.end = False
        self.startPlayers = snakes
        self.players = []
        self.players.append(Player(window = self.window, apples = self.apples, players = self.players, ki = bool(autoplay)))
        for i in range(snakes - 1):
            self.players.append(Player(color = (randint(0, 255), randint(0, 255), randint(0, 255)) ,window = self.window, apples = self.apples, players = self.players, ki = True))
        self.loop()
    
    def loop(self):
        while True:
            try:
                if not self.go and not self.end:
                    self.goCount += self.window.dt
                    if self.goCount >= 3:
                        self.textSurf = None
                        self.go = True
                self.window.screen.fill((0, 0, 0))
                self.apples.update()
                if self.window.keys[pygame.K_DOWN]:
                    self.players[0].changeDirection(0)
                if self.window.keys[pygame.K_UP]:
                    self.players[0].changeDirection(2)
                if self.window.keys[pygame.K_RIGHT]:
                    self.players[0].changeDirection(1)
                if self.window.keys[pygame.K_LEFT]:
                    self.players[0].changeDirection(3)
                self.apples.render(self.window)
                for player in self.players:
                    if self.go:
                        player.update(0.1 / self.speed)
                    if self.window.quit:
                        break
                    player.render()
                if self.window.quit:
                    break
                self.window.render.grid((40, 40, 40))
                self.window.update()
                if len(self.players) == 1 and self.startPlayers > 1:
                    self.textSurf = self.fontSmall.render("Winner", True, self.players[0].color)
                    self.go = False
                    self.end = True
                if not self.go and not self.end:
                    self.textSurf = self.font.render(str(int(3 - self.goCount + 1)), True, (255, 255, 255))
                if self.textSurf != None:
                    self.window.screen.blit(self.textSurf, (320 - self.textSurf.get_width() / 2, 240 - self.textSurf.get_height() / 2))
                pygame.display.update()
            except pygame.error:
                break
