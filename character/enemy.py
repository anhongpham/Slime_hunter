import pygame as pg
from pygame.locals import *
from setup import SCREEN, COLOR
import random
pg.init()

# create Enemy abstract class as a sprite
class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color, resource=None):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

        self.resource = resource

        self.setup_status()

        self.tag = 'enemy'
        self.name = 'enemy'

        self.direction = 'right'

        self.color = color

        self.attack_timer = pg.time.get_ticks()
        self.move_timer = pg.time.get_ticks()
        self.live_timer = pg.time.get_ticks()

    def setup_status(self):
        self.max_hp = 10
        self.hp = self.max_hp
        self.mp = 0
        self.attack_power = 1
        self.defense = 5
        self.default_speed = 3
        self.speed = self.default_speed

    def attack(self, player):
        current_time = pg.time.get_ticks()
        if current_time - self.attack_timer < 1000:
            return
    
        player.get_damage(self.attack_power)
        self.attack_timer = current_time
        
    
    def get_damage(self, damage, inventory):
        if damage > self.defense:
            self.hp -= (damage - self.defense)
            if self.hp <= 0:
                self.die(inventory)

    def show_hp(self, screen):
        # show hp on top of the slime, color: red
        # the bar only have width = self.width when hp = self.max_hp
        # => hp/max_hp = width/max_width
        # => width = hp/max_hp * max_width
        pg.draw.rect(screen, COLOR['red'], (self.rect.x, self.rect.y - 10, self.hp/self.max_hp * self.width, 5))

    def drop(self, inventory):
        inventory.add_item(self.resource)

    def die(self, inventory):
        self.drop(inventory)
        self.kill()

    def random_movement(self, move, camera):
        current_time = pg.time.get_ticks()
        if current_time - self.move_timer < 3000:
            return

        '''
        Random movement algorithm:
        1. generate a random direction (8 directions)
        2. generate a random number of steps
        3. move the enemy in that direction for a number of steps
        
        '''
        # generate a random direction
        direction_list = [('up', 1), ('down', -1), ('left', 1), ('right', -1)]
        
        direction1 = random.choice(direction_list)
        direction2 = random.choice(direction_list)

        # prevent the case left-right or up-down
        # prevent the repeat case 
        while direction1[0] == direction2[0] or direction1[1] == direction2[1]:
            direction2 = random.choice(direction_list)

        # move the enemy in that direction for a number of steps
        step1 = random.randint(30, 60)
        step2 = random.randint(30, 60)

        for i in range(step1):
            move(self, direction1[0], self.speed, camera)

        for i in range(step2):
            move(self, direction2[0], self.speed, camera)

        # reset the timer 
        self.move_timer = current_time

    # make slime move towards the player
    # use move inplace from pygame
    def move_towards_player(self, player):
        current = pg.time.get_ticks()
        if current - self.move_timer > 11000:
            self.kill()
            return
        
        # generate a random x and y component for the movement vector
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)

        # add a component that moves the slime towards the player's position
        player_x, player_y = player.get_pos()
        slime_x, slime_y = self.get_pos()
        dx += (player_x - slime_x + random.uniform(-50, 50)) / 100
        dy += (player_y - slime_y + random.uniform(-50, 50)) / 100

        # normalize the movement vector to have a magnitude of 1
        magnitude = (dx ** 2 + dy ** 2) ** 0.5
        dx /= magnitude
        dy /= magnitude

        # update the slime's position using the movement vector
        self.rect.x += int(dx * self.speed)
        self.rect.y += int(dy * self.speed)

    def get_save_data(self):
        # get position first
        save_dict = {'name': self.name, 'x': self.rect.x, 'y': self.rect.y,
                     'width': self.width, 'height': self.height, 'color': self.color}

        return save_dict

    def load_data(self, save_data):
        self.rect.x = save_data['x']
        self.rect.y = save_data['y']
        self.width = save_data['width']
        self.height = save_data['height']
        self.color = save_data['color']

    def __str__(self):
        return f'I am {self.name}'

    def get_pos(self):
        return self.rect.x, self.rect.y
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


slime_image = pg.image.load('asset/image/slime.png')
# create Slime class as a sprite
class Slime(Enemy):
    def __init__(self, x, y, width, height, color, resource):
        super().__init__(x, y, width, height, color, resource)

        self.image = slime_image
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.setup_status()
        self.tag = 'enemy'
        self.name = 'slime'
        self.color = color

    def setup_status(self):
        super().setup_status()
        self.max_hp = 10
        self.hp = self.max_hp
        self.mp = 0
        self.attack_power = 50
        self.defense = 5
        self.default_speed = 3
