import pygame as pg
from pygame.locals import *
from item.item import Item
pg.init()

class Apple(Item):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.name = 'apple'
        self.color = 'red'

        self.image = pg.image.load('asset/image/candy_02a.png')
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()





    
