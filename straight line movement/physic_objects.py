import pymunk
import pygame

class physics_obj:
    def __init__(self, init_position, init_velocity, acceralation, color):
        self.init_position = init_position
        self.init_velocity = init_velocity
        self.acceralation = acceralation
        self.color = color

        self.body = pymunk.Body()
        self.body.position = init_position
        self.body.velocity = init_velocity

class create_square(physics_obj):
    def __init__(self, init_position=(0, 0), width=50, height=50, density=1, init_velocity=(0, 0), 
                 color=(0, 0, 255), collision_type=1, acceralation=(5, 0), space=None):
        
        super().__init__(init_position, init_velocity, acceralation, color)
        self.width = width
        self.height = height
        self.density = density

        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.density = density
        self.shape.elasticity = 1
        self.shape.collision_type = collision_type

        space.add(self.body, self.shape)

    def update(self, time):
        vel_x = self.body.velocity[0] + self.acceralation[0]*time
        vel_y = self.body.velocity[1] + self.acceralation[1]*time
        self.body.velocity = (vel_x, vel_y)

    def draw(self, display, h):
        x, y = convert_coordinates(self.body.position, h)
        w = self.width
        h = self.height
        pygame.draw.rect(display, self.color, [int(x + w/2), int(y - h/2), w, h])

class graph_info:
    def __init__(self):
        self.pos_x = []
        self.pos_y = []
        self.vel_x = []
        self.vel_y = []

    def add_info(self, obj: physics_obj):
        self.pos_x.append(obj.body.position[0])
        self.pos_y.append(obj.body.position[1])
        self.vel_x.append(obj.body.velocity[0])
        self.vel_y.append(obj.body.velocity[1])

def convert_coordinates(point, h):
    # we need to convert because pygame and pymunk coordinates system don't work the same way.
    return point[0], h-point[1]