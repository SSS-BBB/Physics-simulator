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
    def __init__(self, init_position=(WIDTH/2, HEIGHT/2), width=50, height=50, density=1, init_velocity=(0, 0), 
                 color=(0, 0, 255), collision_type=1, acceralation=(5, 0)):
        
        super().__init__(init_position, init_velocity, acceralation, color)
        self.width = width
        self.height = height
        self.density = density

        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.density = density
        self.shape.elasticity = 1
        self.shape.collision_type = collision_type

        space.add(self.body, self.shape)

class segment_obj:
    def __init__(self, start_pos=(0, 10), end_pos=(WIDTH, 10), thickness=5, color=(0, 0, 0)):
        # init variable
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        self.init_pos = [start_pos, end_pos]
        self.thickness = thickness
        self.color = color

        self.shape = pymunk.Segment(self.body, start_pos, end_pos, thickness)
        # self.shape.elasticity = 1
        space.add(self.body, self.shape)

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

obj_list = {"square": [], "circle": []}

squares = []
stupid_square1 = create_square((20, 50+2), 50, 50, 1, (100, 0), (0, 0, 255), collision_type=1)
squares.append(stupid_square1)
# stupid_square2 = create_square((WIDTH-100, HEIGHT/2), 50, 50, 1, (-100, 0), (255, 0, 0), collision_type=2)
# squares.append(stupid_square2)
obj_list["square"] = squares

stupid_segment = segment_obj((0, 50), (WIDTH*100, 50), 5, (0, 0, 0))


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

def show_graph(t, graph_info: graph_info):
    # decoration
    plt.xlabel("time")
    plt.ylabel("postion")

    # graph
    plt.plot(t, graph_info.pos_x, label="pos_x")
    plt.plot(t, graph_info.pos_y, label="pos_y")

    # show
    plt.legend()
    plt.show()

def collide(arbiter, space, data):
    print("collided")

def update_obj(obj: physics_obj, t):
    vel_x = obj.body.velocity[0] + obj.acceralation[0]
    vel_y = obj.body.velocity[1] + obj.acceralation[1]
    obj.body.velocity = (vel_x, vel_y)

def game():
    # data to show to the grpah
    time_list = []
    time_now = 0

    handler = space.add_collision_handler(1, 2)
    handler.separate = collide

    square_graph = graph_info()
    while not_exit(pygame.event.get()):
        display.fill((255, 255, 255))

        # drawing
        for s in squares:
            draw_square(display, s)
        draw_segment(display, stupid_segment)

        # update data to show to the grpah
        square_graph.add_info(stupid_square1)
        time_list.append(time_now)

        # update screen
        pygame.display.update()

        # run this FPS loops per second
        clock.tick(FPS)

        # 1/FPS seconds for each loop
        space.step(1/FPS)
        for obj in obj_list.values():
            for o in obj:
                update_obj(o, 1/FPS)
        time_now += 1/FPS

    pygame.quit()
    show_graph(time_list, square_graph)

game()