import pygame
import pymunk
import matplotlib.pyplot as plt

# pygame
pygame.init()
WIDTH, HEIGHT = 750, 750
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

# pymunk
space = pymunk.Space()
space.gravity = 0, -981

class create_square:
    def __init__(self, position, width, height, density, velocity, color):
        self.init_pos = position
        self.width = width
        self.height = height
        self.color = color
        self.density = density
        self.init_velocity = velocity

        self.body = pymunk.Body()
        self.body.position = position
        self.body.velocity = velocity
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.density = density
        space.add(self.body, self.shape)

class segment_obj:
    def __init__(self, start_pos, end_pos, thickness, color):
        # init variable
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        self.init_pos = [start_pos, end_pos]
        self.thickness = thickness
        self.color = color

        self.shape = pymunk.Segment(self.body, start_pos, end_pos, thickness)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

stupid_square1 = create_square((20, HEIGHT/2), 50, 50, 1, (100, 0), (0, 0, 255))
stupid_segment = segment_obj((0, 50), (WIDTH, 50), 5, (0, 0, 0))

def convert_coordinates(point):
    # we need to convert because pygame and pymunk coordinates system don't work the same way.
    return point[0], HEIGHT-point[1]

def not_exit(events):
    # go through every event
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def draw_square(display, square: create_square):
    x, y = convert_coordinates(square.body.position)
    w = square.width
    h = square.height
    pygame.draw.rect(display, square.color, [int(x + w/2), int(y - h/2), square.width, square.height])

def draw_segment(display, segment: segment_obj):
    start = convert_coordinates(segment.init_pos[0])
    end = convert_coordinates(segment.init_pos[1])
    pygame.draw.line(display, segment.color, start, end, segment.thickness)

def show_graph(t, pos):
    # decoration
    plt.xlabel("time")
    plt.ylabel("position")

    # graph
    plt.plot(t, pos, label="position with respect to time")

    # show
    plt.legend()
    plt.show()

def game():
    # data to show to the grpah
    time_list = []
    square_x = []
    square_y = []
    time_now = 0
    while not_exit(pygame.event.get()):
        display.fill((255, 255, 255))

        # drawing
        draw_square(display, stupid_square1)
        draw_segment(display, stupid_segment)

        # update data to show to the grpah
        square_x.append(stupid_square1.body.position[0])
        square_y.append(stupid_square1.body.position[1])
        time_list.append(time_now)

        # update screen
        pygame.display.update()

        # run this FPS loops per second
        clock.tick(FPS)

        # 1/FPS seconds for each loop
        space.step(1/FPS)
        time_now += 1/FPS

    pygame.quit()
    show_graph(time_list, square_y)

game()