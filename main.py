from graphics.window import Window
from game.player import Player
from game.apples import Apples
from threading import Thread
from random import randint
from tkinter import *
import pygame
import time
import json
import sys
import os


class Main:
    def __init__(self, snakes, apples, speed, autoplay, client = None):
        if getattr(sys, 'frozen', False):
            CurrentPath = sys._MEIPASS
        else:
            CurrentPath = os.path.dirname(__file__)
        self.multiplayer = client != None
        self.client = client
        self.speed = speed
        self.window = Window()
        self.apples = Apples(apples)
        self.go = False
        self.goCount = 0
        fontFile = os.path.join(CurrentPath, "freesansbold.ttf")
        self.font = pygame.font.Font(fontFile, 240)
        self.font.set_bold(True)
        self.fontSmall = pygame.font.Font(fontFile, 120)
        self.fontSmall.set_bold(True)
        self.textSurf = None
        self.end = False
        self.biggestClients = 1
        self.startPlayers = snakes
        self.players = []
        if self.multiplayer:
            self.players.append(Player(color = self.client.clients[self.client.id]["Color"], window = self.window, apples = self.apples, players = self.players, ki = bool(autoplay), client = self.client))
        else:
            self.players.append(Player(window = self.window, apples = self.apples, players = self.players, ki = bool(autoplay), client = self.client))
        for i in range(snakes - 1):
            self.players.append(Player(color = (randint(0, 255), randint(0, 255), randint(0, 255)), window = self.window, apples = self.apples, players = self.players, ki = True))
        self.loop()

    def waitWindow(self):
        self.tkwindow = Tk()
        self.tkwindow.resizable(False, False)
        self.tkwindow.title("Waiting...")
        Label(self.tkwindow, text = "Waiting for connections to close...").pack()
        self.tkwindow.update_idletasks()
        self.tkwindow.geometry("{}x{}+{}+{}".format(self.tkwindow.winfo_width(), self.tkwindow.winfo_height(), int(self.tkwindow.winfo_screenwidth() / 2 + self.tkwindow.winfo_width() / 2), int(self.tkwindow.winfo_screenheight() / 2 + self.tkwindow.winfo_height() / 2)))

    def loop(self):
        while True:
            try:
                self.textSurf1 = None
                if not self.go and not self.end:
                    self.goCount += self.window.dt
                    if self.goCount >= 3:
                        self.textSurf = None
                        self.go = True
                self.window.screen.fill((0, 0, 0))
                if not self.multiplayer:
                    self.apples.update()
                if self.window.keys[pygame.K_DOWN]:
                    self.players[0].changeDirection(0)
                if self.window.keys[pygame.K_UP]:
                    self.players[0].changeDirection(2)
                if self.window.keys[pygame.K_RIGHT]:
                    self.players[0].changeDirection(1)
                if self.window.keys[pygame.K_LEFT]:
                    self.players[0].changeDirection(3)
                if not self.multiplayer:
                    self.apples.render(self.window)
                over = not self.multiplayer
                if self.multiplayer and self.players == []:
                    self.client.send(json.dumps({"Parts": []}))
                for player in self.players:
                    if self.go:
                        player.update(0.1 / self.speed)
                        if self.multiplayer:
                            self.client.send(json.dumps({"Parts": player.parts}))
                    if player.dead and self.multiplayer:
                        self.client.send(json.dumps({"Parts": []}))
                    if self.window.quit and over:
                        break
                    if not self.multiplayer:
                        player.render()
                if self.multiplayer:
                    if self.client.id == 0:
                        self.client.send(json.dumps({"Apples": self.apples.apples}))
                    if self.client.id == 0:
                        for client in self.client.clients:
                            try:
                                if self.apples.check(*client["Parts"][0]):
                                    self.apples.apples.remove([*client["Parts"][0]])
                            except (KeyError, IndexError):
                                pass
                            self.apples.update()
                    else:
                        try:
                            self.apples.apples = self.client.clients[0]["Apples"]
                        except KeyError:
                            pass
                    self.apples.render(self.window)
                    allDead = True
                    count = 0
                    notDead = []
                    for client in self.client.clients:
                        try:
                            for x, y in client["Parts"]:
                                self.window.render.cube(x, y, client["Color"])
                            if not client["Dead"]:
                                count += 1
                                if count > 1:
                                    allDead = False
                        except KeyError as e:
                            allDead = False
                            notDead.append(client)
                        try:
                            if client["Won"]:
                                over = True
                        except KeyError:
                            pass
                    try:
                        if notDead[0]["id"] == self.client.id and len(notDead) == 1:
                            self.client.clients[self.client.id]["Won"] = True
                    except IndexError:
                        pass
                if self.window.quit and over:
                    break
                self.window.render.grid((40, 40, 40))
                self.window.update()
                won = False
                try:
                    if (len(self.players) == 1 and self.startPlayers > 1) or (self.multiplayer and self.client.clients[self.client.id]["Won"]):
                        self.textSurf = self.fontSmall.render("Winner", True, self.players[0].color)
                        self.go = False
                        self.end = True
                        won = True
                except (KeyError, IndexError):
                    pass
                showGameOver = False
                try:
                    showGameOver = self.players[0].dead and not won
                except IndexError:
                    showGameOver = True
                if showGameOver:
                    self.end = True
                    self.go = False
                    self.fontSmall.set_bold(False)
                    self.textSurf = self.fontSmall.render("Game", True, (255, 255, 255))
                    self.textSurf1 = self.fontSmall.render("Over", True, (255, 255, 255))
                if not self.go and not self.end:
                    self.textSurf = self.font.render(str(int(3 - self.goCount + 1)), True, (255, 255, 255))
                if self.textSurf != None:
                    if self.textSurf1 != None:
                        self.window.screen.blit(self.textSurf, (320 - self.textSurf.get_width() / 2, 190 - self.textSurf.get_height() / 2))
                        self.window.screen.blit(self.textSurf1, (320 - self.textSurf1.get_width() / 2, 290 - self.textSurf1.get_height() / 2))
                    else:
                        self.window.screen.blit(self.textSurf, (320 - self.textSurf.get_width() / 2, 240 - self.textSurf.get_height() / 2))
                pygame.display.update()
            except pygame.error:
                break
        if self.multiplayer and self.client.id != 0:
            self.client.close()
        elif self.multiplayer:
            self.waitWindow()
            while len(self.client.clients) > 1:
                self.tkwindow.update()
                time.sleep(0.1)
                self.client.send("{}")
            self.tkwindow.destroy()
            self.client.close()
