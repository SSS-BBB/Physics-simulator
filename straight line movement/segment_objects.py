import pymunk
import pygame

class segment_obj:
    def __init__(self, start_pos=(0, 10), end_pos=(10, 10), thickness=5, color=(0, 0, 0), space=None):
        # init variable
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        self.init_pos = [start_pos, end_pos]
        self.thickness = thickness
        self.color = color

        self.shape = pymunk.Segment(self.body, start_pos, end_pos, thickness)
        # self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw(self, display, h):
        start = convert_coordinates(self.init_pos[0], h)
        end = convert_coordinates(self.init_pos[1], h)
        pygame.draw.line(display, self.color, start, end, self.thickness)

def convert_coordinates(point, h):
    # we need to convert because pygame and pymunk coordinates system don't work the same way.
    return point[0], h-point[1]