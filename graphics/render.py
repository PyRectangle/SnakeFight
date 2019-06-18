import pygame


class Render:
    def __init__(self, surface):
        self.surface = surface
        self.GAP = 20
    
    def grid(self, color):
        for i in range(int(640 / self.GAP) + 1):
            x = i * self.GAP
            pygame.draw.line(self.surface, color, [x, 0], [x, 480])
        for i in range(int(480 / self.GAP) + 1):
            y = i * self.GAP
            pygame.draw.line(self.surface, color, [0, y], [640, y])
    
    def cube(self, x, y, color):
        x *= self.GAP
        x += 1
        y *= self.GAP
        y += 1
        pygame.draw.polygon(self.surface, color, [[x, y], [x + self.GAP - 2, y], [x + self.GAP - 2, y + self.GAP - 2], [x, y + self.GAP - 2]])
