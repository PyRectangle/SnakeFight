from graphics.render import Render
import pygame


class Window:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Snake Fight")
        self.keys = [0] * 323
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.fps = 0
        self.render = Render(self.screen)
        self.quit = False

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.terminate()
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = 1
        if event.type == pygame.KEYUP:
            self.keys[event.key] = 0

    def terminate(self):
         pygame.quit()
         self.quit = True

    def update(self):
        self.dt = self.clock.tick() / 1000
        self.fps = self.clock.get_fps()
        for event in pygame.event.get():
            self.handleEvent(event)
