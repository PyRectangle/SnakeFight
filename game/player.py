from random import randint
import random
import json


class Player:
    def __init__(self, startX = None, startY = None, startDirection = None, color = (50, 255, 50), window = None, apples = None, players = None, ki = True, client = None):
        if startX == None:
            startX = randint(0, 640 / 20 - 1)
        if startY == None:
            startY = randint(0, 480 / 20 - 1)
        if startDirection == None:
            startDirection = randint(0, 3)
        self.players = players
        self.apples = apples
        self.window = window
        self.direction = startDirection
        self.color = color
        self.parts = [[startX, startY]]
        self.count = 0
        self.ki = ki
        self.dead = False
        self.moved = False
        self.first = True
        self.multiplayer = client != None
        self.client = client

    def checkOnApple(self, x, y, destroy = True):
        count = 0
        for apple in self.apples.apples:
            if apple[0] == x and apple[1] == y:
                if destroy:
                    del self.apples.apples[count]
                return True
            count += 1
        return False
        
    def checkAppleDirect(self, direct, only = True, tcoords = None):
        if tcoords == None:
            coords = self.parts[0].copy()
        else:
            coords = tcoords
        dist = 0
        for i in range(32):
            dist += 1
            if self.checkOnApple(*coords, False):
                return dist
            if not only:
                if self.checkAppleDirect(self.calcDirect(direct + 1), tcoords = coords.copy()) != None or self.checkAppleDirect(self.calcDirect(direct - 1), tcoords = coords.copy()) != None:
                    return dist - 1
            coords = self.calculateDirectCoords(coords, direct)
    
    def checkDeathDirect(self, direct):
        coords = self.parts[0].copy()
        dist = 0
        for i in range(32):
            dist += 1
            if self.checkOnDeath(coords):
                return dist
            coords = self.calculateDirectCoords(coords, direct)

    def getBestDirect(self):
        direct = self.direction
        adistances = []
        ddistances = []
        directions = [direct, direct + 1, direct - 1]
        adistances.append(self.checkAppleDirect(self.direction, False))
        ddistances.append(self.checkDeathDirect(self.direction))
        self.changeDirection(direct + 1)
        adistances.append(self.checkAppleDirect(self.direction))
        ddistances.append(self.checkDeathDirect(self.direction))
        self.changeDirection(direct - 1)
        adistances.append(self.checkAppleDirect(self.direction))
        ddistances.append(self.checkDeathDirect(self.direction))
        self.changeDirection(directions[0])
        highest = 0
        for i in ddistances:
            if i != None:
                if i > highest:
                    highest = i
        lowest = 640
        for i in adistances:
            if i != None and i < lowest:
                lowest = i
        apossible = []
        adpossible = []
        count = 0
        for i in adistances:
            if i != None:
                if i == lowest or i < 10:
                    apossible.append(directions[count])
                    adpossible.append(i)
            count += 1
        dpossible = []
        ddpossible = []
        count = 0
        for i in ddistances:
            if i != None:
                if i == highest or i > 2:
                    dpossible.append(directions[count])
                    ddpossible.append(i)
            count += 1
        possible = []
        count = 0
        for d in dpossible:
            acount = 0
            for a in apossible:
                if d == a:
                    if ddpossible[count] > adpossible[acount]:
                        possible.append(d)
                acount += 1
            count += 1
        if possible == []:
            count = 0
            for i in dpossible:
                if ddpossible[count] == highest:
                    possible.append(i)
                count += 1
        directs = []
        for i in possible:
            if self.checkDirectFreeBlockSide(i):
                directs.append(i)
        if directs == []:
            directs = possible
        return random.choice(directs)
    
    def checkDirectFreeBlockSide(self, direct, coords = None, no = False):
        if coords == None:
            coords = self.parts[0].copy()
        for i in range(32):
            coords = self.calculateDirectCoords(coords, direct)
            if no:
                deaths = [self.checkOnDeath(self.calculateDirectCoords(self.parts[0].copy(), direct)),
                          self.checkOnDeath(self.calculateDirectCoords(self.parts[0].copy(), self.calcDirect(direct + 1))),
                          self.checkOnDeath(self.calculateDirectCoords(self.parts[0].copy(), self.calcDirect(direct - 1)))]
            else:
                deaths = [self.checkOnDeath(self.calculateDirectCoords(self.parts[0].copy(), direct)),
                          self.checkDirectFreeBlockSide(self.calcDirect(direct + 1), self.calculateDirectCoords(self.parts[0].copy(), self.calcDirect(direct + 1)), True),
                          self.checkDirectFreeBlockSide(self.calcDirect(direct - 1), self.calculateDirectCoords(self.parts[0].copy(), self.calcDirect(direct - 1)), True)]
            if not deaths[1] or not deaths[2]:
                return True
            elif deaths[0]:
                break
        return False
    
    def go(self):
        self.moved = False
        if self.ki or self.first:
            self.first = False
            self.changeDirection(self.getBestDirect())
            if self.checkOnDeath(self.calculateDirectCoords(self.parts[0].copy(), self.direction)):
                if not self.checkOnDeath(self.calculateDirectCoords(self.parts[0].copy(), 0)):
                    self.changeDirection(0)
                if not self.checkOnDeath(self.calculateDirectCoords(self.parts[0].copy(), 1)):
                    self.changeDirection(1)
                if not self.checkOnDeath(self.calculateDirectCoords(self.parts[0].copy(), 2)):
                    self.changeDirection(2)
                if not self.checkOnDeath(self.calculateDirectCoords(self.parts[0].copy(), 3)):
                    self.changeDirection(3)
        self.addPart(True)
        if not self.checkOnApple(*self.parts[0]):
            del self.parts[-1]
    
    def calculateDirectCoords(self, coords, direction):
        if direction == 0:
            coords[1] += 1
        if direction == 1:
            coords[0] += 1
        if direction == 2:
            coords[1] -= 1
        if direction == 3:
            coords[0] -= 1
        return coords
    
    def addPart(self, start = False):
        if start:
            self.parts.insert(0, self.calculateDirectCoords(self.parts[0].copy(), self.direction))
        else:
            self.parts.append(self.calculateDirectCoords(self.parts[0].copy(), self.direction))

    def calcDirect(self, direct):
        while direct < 0:
            direct += 4
        while direct > 3:
            direct -= 4
        return direct

    def changeDirection(self, number):
        if not self.moved or self.ki:
            self.moved = True
            if self.calcDirect(self.direction + 1) == self.calcDirect(number) or self.calcDirect(self.direction - 1) == self.calcDirect(number) or self.ki:
                self.direction = self.calcDirect(number)
    
    def update(self, time):
        self.count += self.window.dt
        if self.count >= time:
            self.count -= time
            self.go()
            if self.checkOnDeath(self.parts[0]):
                self.die()

    def checkOnDeath(self, coords):
        touch = False
        if self.multiplayer:
            try:
                for client in self.client.clients:
                    if client["id"] == self.client.id:
                        parts = self.parts[1:]
                    else:
                        parts = client["Parts"]
                    for part in parts:
                        if part == coords:
                            touch = True
                            break
                    if touch:
                        break
            except KeyError:
                pass
        else:
            for player in self.players:
                if player == self:
                    parts = self.parts[1:]
                else:
                    parts = player.parts
                for part in parts:
                    if part == coords:
                        touch = True
                        break
                if touch:
                    break
        if coords[0] < 0 or coords[1] < 0 or coords[0] > 31 or coords[1] > 23:
            touch = True
        return touch
    
    def die(self):
        if self.ki and not self.multiplayer:
            for i in range(len(self.players)):
                if self.players[i] == self:
                    del self.players[i]
                    break
        else:
            if self.multiplayer:
                self.client.send(json.dumps({"Dead": True}))
            self.dead = True
    
    def render(self):
        for part in self.parts:
            self.window.render.cube(*part, self.color)
