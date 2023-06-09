import pygame as pg
from pygame.locals import *

pg.init()


class Camera:
    def __init__(self, player, screen_width, screen_height, map_width, map_height):
        self.player = player
        self.x = 0
        self.y = 0
        self.width = screen_width
        self.height = screen_height
        self.map_width = map_width
        self.map_height = map_height

        # create a rect for the camera and center it in the screen
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.width / 2, self.height / 2)

        self.padding = 60
        self.padding_top = self.padding
        self.padding_left = self.padding
        self.padding_right = self.width - self.padding
        self.padding_bottom = self.height - self.padding

        self.speed = self.player.default_speed
        self.create_collision_points()
    '''
    CHECK COLLISION BETWEEN PLAYER AND PADDING
    '''
    def player_movement(self, _map, obj_list):
        self.move_top(_map, obj_list)
        self.move_bottom(_map, obj_list)
        self.move_left(_map, obj_list)
        self.move_right(_map, obj_list)
        pass 

    def move_top(self, _map, obj_list):
        if self.player.rect.y <= self.padding_top:
            self.player.top_transition = True
            
            self.collide(_map, self.top_point, -self.speed, obj_list)
            return

        self.player.top_transition = False

    def move_bottom(self, _map, obj_list):
        if self.player.rect.y + self.player.height >= self.padding_bottom:
            self.player.bottom_transition = True
            
            self.collide(_map, self.bottom_point, self.speed, obj_list)
            return

        self.player.bottom_transition = False

    def move_left(self, _map, obj_list):
        if self.player.rect.x <= self.padding_left:
            self.player.left_transition = True
            
            self.collide(_map, self.left_point, -self.speed, obj_list) 
            return

        self.player.left_transition = False

    def move_right(self, _map, obj_list):
        if self.player.rect.x + self.player.width >= self.padding_right:
            self.player.right_transition = True
        
            self.collide(_map, self.right_point, self.speed, obj_list)
            return

        self.player.right_transition = False

    '''
    CHECK THE COLLISION BETWEEN CAMERA AND MAP
    '''

    # create 4 points and place on 4 sides of the camera
    # check if the points are inside the map
    # if not, move the camera to the opposite direction
    # then use collidepoint() to check if the points are inside the map
    # if inside, then the camera can move
    # if not, then the camera can't move
    def create_collision_points(self):
        self.left_point = (self.x, self.y + self.height / 2)
        self.right_point = (self.x + self.width, self.y + self.height / 2)
        self.top_point = (self.x + self.width / 2, self.y)
        self.bottom_point = (self.x + self.width / 2, self.y + self.height)
    
    def collide(self, _map, point, speed, obj_list):
        if _map.rect.collidepoint(point):
            if point in [self.left_point, self.right_point]:
                self.x += speed
                self.move_objects(-speed, 0, _map, obj_list)

            elif point in [self.top_point, self.bottom_point]:
                self.y += speed
                self.move_objects(0, -speed, _map, obj_list)

    def move_objects(self, dx, dy, _map, obj_list):
        _map.update(dx, dy)

        for obj in obj_list:
            obj.rect.x += dx
            obj.rect.y += dy

    def update(self, _map, obj_list):
        self.create_collision_points()
        self.player_movement(_map, obj_list)

    def get_pos(self):
        return self.x, self.y

    '''
    SAVE METHODS
    '''
    def get_save_data(self):
        # get position first
        save_dict = {'dx': self.x, 'dy': self.y}

        return save_dict

    def load_data(self, save_data, _map, obj_list):
        dx = save_data['dx']
        dy = save_data['dy']

        self.x += dx
        self.y += dy

        self.move_objects(-dx, -dy, _map, obj_list)


