from random import randint


class Apples:
    def __init__(self, quantity):
        self.count = quantity
        self.apples = []
    
    def update(self):
        while len(self.apples) < self.count:
            self.apples.append([randint(0, 640 / 20 - 1), randint(0, 480 / 20 - 1)])
    
    def render(self, window):
        for apple in self.apples:
            window.render.cube(*apple, (255, 0, 0))
