import pygame
import pymunk
import matplotlib.pyplot as plt
from physic_objects import *
from segment_objects import *

# pygame
pygame.init()
WIDTH, HEIGHT = 750, 750
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

# pymunk
space = pymunk.Space()
space.gravity = 0, -981

obj_list = {"square": [], "circle": []}

squares = []
stupid_square1 = create_square((20, 50+2), 50, 50, 1, (100, 0), (0, 0, 255), collision_type=1, space=space, acceralation=(200, 0))
squares.append(stupid_square1)
# stupid_square2 = create_square((WIDTH-100, HEIGHT/2), 50, 50, 1, (-100, 0), (255, 0, 0), collision_type=2)
# squares.append(stupid_square2)
obj_list["square"] = squares

stupid_segment = segment_obj((0, 50), (WIDTH*100, 50), 5, (0, 0, 0), space=space)


def convert_coordinates(point):
    # we need to convert because pygame and pymunk coordinates system don't work the same way.
    return point[0], HEIGHT-point[1]

def not_exit(events):
    # go through every event
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

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
            s.draw(display, HEIGHT)
        stupid_segment.draw(display, HEIGHT)

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
                o.update(1/FPS)
        time_now += 1/FPS

    pygame.quit()
    show_graph(time_list, square_graph)

game()