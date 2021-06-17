#######################################################################
#######################################################################

### This is the 3rd version of Map Game. This is the one that I got
### Player Mode to work as intended.

### Map Mode is where the player moves around the screen inside of
### a fixed map. Player Mode leaves the player fixed on the screen
### and moves the map around the player.

### In the 2nd version I got the rotations of the map to work correctly.
### However, it changed the coordinates of the original map. Here I got
### the program to draw a rotated map based on only the original
### coordinates without actually altering them. This allows the map
### information to remain fixed so that we can always go back to Map
### Mode.


#######################################################################
# import packages
#######################################################################

import pygame, math
from pygame.locals import *


#######################################################################
# initialize variables and stuff
#######################################################################

# set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (215, 215, 215)
PINK = (255, 125, 125)
PURPLE = (200, 100, 255)
SKY_BLUE = (100, 200, 255)
YELLOW = (255, 255, 100)

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up display window
background_color = WHITE
(WINDOW_LENGTH, WINDOW_HEIGHT) = (1100, 700)
X = round(WINDOW_LENGTH / 2)       # this is the x-value for the center of the screen
Y = round(WINDOW_HEIGHT / 2)    # this is the y-value for the center of the screen
center = (X, Y)                 # this is the center coordinate of the window
HORIZON = int(WINDOW_HEIGHT * 0.5)

# define surface
screen = pygame.display.set_mode((WINDOW_LENGTH, WINDOW_HEIGHT))
pygame.display.set_caption('Map Game')

# These define the map the player is playing on.
# Every two points form a line, each line makes up the map.
# I tried to make each line into it's own list or tuple of 2 points
# but this proved to be severly difficult to render
# (plus, it would increase the number of operations... although
# the time difference may or may not be marginal).
box_color = BLACK
box_thickness = 3
#box = [(50, 110), (600, 110), (600, 110), (600, 210), (600, 210), (50, 110)]    # triangle
#box = [(50, 110), (550, 110), (550, 110), (550, 510), (550, 510), (30, 510), (30, 510), (50, 110)] # almost a rectangle

point01 = (50, 110)
point02 = (550, 110)
point03 = (700, 400)
point04 = (400, 800)
point05 = (200, 300)
#box = [point01, point02, point02, point03, point03, point04, point04, point05, point05, point01]
#colors = [BLUE, RED, GREEN, YELLOW, PINK]
    
box = [(50, 110), (550, 110), (550, 110), (550, 510), (550, 510), (50, 510), (50, 510), (50, 110)] # almost a rectangle
colors = [BLUE, RED, GREEN, YELLOW]



# player variables
player_color = RED
init_x = 250 # the starting x-coordinate
init_y = 200 # the starting y-coordinate
speed = 2
init_angle = 0 # -0.5 * math.pi
player_length = 25
turning_speed = 0.025
radius = 10

# other variables
ROTATE = -0.5 * math.pi # this is the universal rotation about the axis (ie. the orientation)
zoom_level = 1
zoom_speed = 0.1

#######################################################################
# classes
#######################################################################

class Player:
    def __init__(self, x, y, speed, angle):
        self.x = x
        self.y = y
        self.speed = 0
        self.angle = angle
        self.color = player_color
        self.dx = 0
        self.dy = 0
        self.radius = radius

    # method to 'move' the player forward/backward
    def move(self):
        player.dx = player.speed * math.cos(player.angle)
        player.dy = player.speed * math.sin(player.angle)
        player.x += player.dx
        player.y += player.dy

    def display_map_mode(self):  # draw the player on the screen in Map Mode (so the map is fixed and the player is moving around)
        # define the center point of the player
        center_point = (round(self.x), round(self.y))

        # calculate the endpoint of the player (in the direction that the player is facing)
        end_point_x = round(self.x + (1.0 * player_length * math.cos(self.angle)))
        end_point_y = round(self.y + (1.0 * player_length * math.sin(self.angle)))
        upper_point = (end_point_x, end_point_y)

        # calculate the lefthand side of the player
        left_angle = self.angle - (0.65 * math.pi)
        left_x = round(self.x + (0.5 * player_length * math.cos(left_angle)))
        left_y = round(self.y + (0.5 * player_length * math.sin(left_angle)))
        left_point = (left_x, left_y)

        # calculate the righthand side of the player
        right_angle = self.angle + (0.65 * math.pi)
        right_x = round(self.x + (0.5 * player_length * math.cos(right_angle)))
        right_y = round(self.y + (0.5 * player_length * math.sin(right_angle)))
        right_point = (right_x, right_y)

        # draw the player
        pygame.draw.polygon(screen, self.color, [upper_point, right_point, center_point, left_point], 1)

    def display_player_mode(self):    # draw the player on the screen in Player Mode (so the player is fixed and the map is moving around)
        upper_point_x = X + player_length * math.cos(ROTATE)
        upper_point_y = Y + player_length * math.sin(ROTATE)
        upper_point = (round(upper_point_x), round(upper_point_y))

        left_angle = ROTATE - (0.65 * math.pi)
        left_x = round(X + (0.5 * player_length * math.cos(left_angle)))
        left_y = round(Y + (0.5 * player_length * math.sin(left_angle)))
        left_point = (round(left_x), round(left_y))

        right_angle = ROTATE + (0.65 * math.pi)
        right_x = round(X + (0.5 * player_length * math.cos(right_angle)))
        right_y = round(Y + (0.5 * player_length * math.sin(right_angle)))
        right_point = (round(right_x), round(right_y))

        # draw the player
        pygame.draw.polygon(screen, self.color, [upper_point, right_point, center, left_point], 1)


#######################################################################
# functions
#######################################################################

# this function writes the text that displays the current mode
def write_mode(current_mode):
    text_X = 10      # this is the top left corner x-value placement of the text
    text_Y = 10      # this is the top left corner y-value placement of the text
    text_color = BLACK
    font_size = 24
    font = pygame.font.SysFont(None, font_size)
    text = "MODE: " + current_mode  # this is what will be written to the screen (it says the mode of play)
    line = font.render(text, True, text_color)
    screen.blit(line, (text_X, text_Y))

def write_angle(angle):
    text_X = 10      # this is the top left corner x-value placement of the text
    text_Y = 30      # this is the top left corner y-value placement of the text
    text_color = BLACK
    font_size = 24
    font = pygame.font.SysFont(None, font_size)
    text = "ANGLE: " + str(round(angle, 2))  # this is what will be written to the screen (it says the mode of play)
    line = font.render(text, True, text_color)
    screen.blit(line, (text_X, text_Y))

def check_collision(player, map):
    for line in map.lines:
        if line[0][0] <= line[1][0]:
            x1 = line[0][0]
            x2 = line[1][0]
        else:
            x1 = line[1][0]
            x2 = line[0][0]
        if line[0][1] <= line[1][1]:
            y1 = line[0][1]
            y2 = line[1][1]
        else:
            y1 = line[1][1]
            y2 = line[0][1]
        if (player.x + player.radius) >=  x1 and (player.x - player.radius) <= x2 and (player.y - player.radius) <= y2 and (player.y + player.radius) >= y1:
            print(True)
            return True
    return False

def map_display_map_mode(room, color, thickness):
    for i in range(0, len(room), 2):
        pygame.draw.line(screen, color, room[i], room[i + 1], thickness)
        if i % 2 == 0:
            pygame.draw.circle(screen, colors[int(i / 2)], room[i], 15, 0)


def map_display_player_mode(room, color, thickness, angle, zoom_level):
    colors = [BLUE, RED, GREEN, YELLOW]
    for i in range(0, len(room), 2):
        # Convert each tuple (vertex) into separate x and y values.
        # Note that room[i] represents one vertex and room[i + 1] represents the other vertex.
        x1 = room[i][0]
        y1 = room[i][1]
        x2 = room[i + 1][0]
        y2 = room[i + 1][1]

        # Shift each vertex horizontally/vertically to be oriented around the origin with respect to the player
        # (so it's acting as if the player is at the origin and everything is being drawn relative to that).
        x1 = x1 - player.x
        y1 = y1 - player.y
        x2 = x2 - player.x
        y2 = y2 - player.y

        # Rotate each vertex around the origin.
        # The negative angle argument of the trig function is because:
        #  -->  when you press LEFT, everything rotates to the RIGHT (clockwise)
        #  -->  when you press RIGHT, everything rotates to the LEFT (counter-clockwise).

        new_x1 = x1 * math.cos(-angle + ROTATE) - y1 * math.sin(-angle + ROTATE)
        new_y1 = x1 * math.sin(-angle + ROTATE) + y1 * math.cos(-angle + ROTATE)
        new_x2 = x2 * math.cos(-angle + ROTATE) - y2 * math.sin(-angle + ROTATE)
        new_y2 = x2 * math.sin(-angle + ROTATE) + y2 * math.cos(-angle + ROTATE)

        # Zoom in or zoom out.

        new_x1 = new_x1 * zoom_level
        new_y1 = new_y1 * zoom_level
        new_x2 = new_x2 * zoom_level
        new_y2 = new_y2 * zoom_level

        # Shift each vertex horizontally/vertically being oriented around the center of the screen.
        x1 = new_x1 + X
        y1 = new_y1 + Y
        x2 = new_x2 + X
        y2 = new_y2 + Y

        # Round each point to the nearest integer before drawing it.
        x1 = round(x1)
        y1 = round(y1)
        x2 = round(x2)
        y2 = round(y2)

        # draw the line connecting the two vertices
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), thickness)
        if i % 2 == 0:
            pygame.draw.circle(screen, colors[int(i / 2) - 1], (x1, y1), 15, 0)

    write_info = False

    if write_info == True:
        text_X = 10      # this is the top left corner x-value placement of the text
        text_Y = 50      # this is the top left corner y-value placement of the text
        text_color = BLACK
        font_size = 24
        font = pygame.font.SysFont(None, font_size)
        point1 = "(" + str(room[0][0]) + ", " + str(room[0][1]) + ")"
        point2 = "(" + str(x1) + ", " + str(y1) + ")"
        text = "Point #1: " + point1 + " |-> " + point2
        line = font.render(text, True, text_color)
        screen.blit(line, (text_X, text_Y))

        text_X = 10      # this is the top left corner x-value placement of the text
        text_Y = 70      # this is the top left corner y-value placement of the text
        text_color = BLACK
        font_size = 24
        font = pygame.font.SysFont(None, font_size)
        point1 = "(" + str(room[1][0]) + ", " + str(room[1][1]) + ")"
        point2 = "(" + str(x2) + ", " + str(y2) + ")"
        text = "Point #2: " + point1 + " |-> " + point2
        line = font.render(text, True, text_color)
        screen.blit(line, (text_X, text_Y))

        text_X = 10      # this is the top left corner x-value placement of the text
        text_Y = 90      # this is the top left corner y-value placement of the text
        text_color = BLACK
        font_size = 24
        font = pygame.font.SysFont(None, font_size)
        #distance1 = round(math.hypot( room[1][0] - room[0][0], room[1][1] - room[0][1]), 3)
        #distance2 = round(math.hypot( x2 - x1, y2 - y1), 3)
        distance1 = round(math.hypot(player.x - room[0][0], player.y - room[0][1]), 2)
        distance2 = round(math.hypot(new_x1, new_y1), 2)
        text = "Distance: " + str(distance1) + " --> " + str(distance2)
        line = font.render(text, True, text_color)
        screen.blit(line, (text_X, text_Y))

    return None


def map_display_first_person_mode(room, color, thickness, angle, zoom_level):
    y1_behind = False
    y2_behind = False
    colors = [BLUE, RED, GREEN, YELLOW]
    for i in range(0, len(room), 2):
        # Convert each tuple (vertex) into separate x and y values.
        # Note that room[i] represents one vertex and room[i + 1] represents the other vertex.
        x1 = room[i][0]
        y1 = room[i][1]
        x2 = room[i + 1][0]
        y2 = room[i + 1][1]

        # Shift each vertex horizontally/vertically to be oriented around the origin with respect to the player
        # (so it's acting as if the player is at the origin and everything is being drawn relative to that).
        x1 = x1 - player.x
        y1 = y1 - player.y
        x2 = x2 - player.x
        y2 = y2 - player.y

        # Rotate each vertex around the origin.
        # The negative angle argument of the trig function is because:
        #  -->  when you press LEFT, everything rotates to the RIGHT (clockwise)
        #  -->  when you press RIGHT, everything rotates to the LEFT (counter-clockwise).
        ROTATE = 0.5 * math.pi
        new_x1 = x1 * math.cos(-angle + ROTATE) - y1 * math.sin(-angle + ROTATE)
        new_y1 = x1 * math.sin(-angle + ROTATE) + y1 * math.cos(-angle + ROTATE)
        new_x2 = x2 * math.cos(-angle + ROTATE) - y2 * math.sin(-angle + ROTATE)
        new_y2 = x2 * math.sin(-angle + ROTATE) + y2 * math.cos(-angle + ROTATE)
        ROTATE = -0.5 * math.pi
        
        # Zoom in or zoom out.
        new_x1 = new_x1 * zoom_level
        new_y1 = new_y1 * zoom_level
        new_x2 = new_x2 * zoom_level
        new_y2 = new_y2 * zoom_level

        if new_y1 > HORIZON:
            new_y1 = HORIZON
        if new_y2 > HORIZON:
            new_y2 = HORIZON

        x1 = new_x1 * (1 - (new_y1 / HORIZON))
        y1 = new_y1
        x2 = new_x2 * (1 - (new_y2 / HORIZON))
        y2 = new_y2

        if y1 < 0:
            y1_behind = True
        if y2 < 0:
            y2_behind = True
            
        # Shift each vertex horizontally/vertically being oriented around the center of the screen.
        x1 = x1 + X
        y1 = y1 + Y
        x2 = x2 + X
        y2 = y2 + Y

        # Round each point to the nearest integer before drawing it.
        x1 = round(x1)
        y1 = round(new_y1)
        x2 = round(x2)
        y2 = round(new_y2)

        # draw the line connecting the two vertices
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), thickness)
        pygame.draw.line(screen, color, (x1, WINDOW_HEIGHT - y1), (x2, WINDOW_HEIGHT - y2), thickness)
        if y1_behind == False:
            pygame.draw.line(screen, color, (x1, y1), (x1, WINDOW_HEIGHT - y1), thickness)
        if y2_behind == False:
            pygame.draw.line(screen, color, (x2, y2), (x2, WINDOW_HEIGHT - y2), thickness)
        
        if i % 2 == 0:
            pygame.draw.circle(screen, colors[int(i / 2)-1], (x1, y1), 15, 0)
            pygame.draw.circle(screen, colors[int(i / 2)-1], (x1, WINDOW_HEIGHT - y1), 15, 0)

    # draw cursor crosshairs
    length = 25
    pygame.draw.line(screen, GREY, (X - length, Y), (X + length, Y), 3)
    pygame.draw.line(screen, GREY, (X, Y - length), (X, Y + length), 3)



#### The rest of the functions are math functions.  ####
#### For future iterations, use numpy.              ####

# this function maps an angle to (-pi, pi]
def map_angle_to_domain(angle):
    if angle > math.pi:
        return angle - (2 * math.pi)
    elif angle <= -math.pi:
        return angle + (2 * math.pi)
    else:
        return angle

# this function finds the dot product (scalar product) between two vectors
# the input to the function is two vectors, which are tupels
def dot_product(vector_1, vector_2):
    x_product = vector_1[0]*vector_2[0]
    y_product = vector_1[1]*vector_2[1]
    dot_product = x_product + y_product
    return dot_product

# this function finds the angle between two vectors
# the input to the function is two vectors, which are tupels
def angle_between(vector_1, vector_2):
    # cos(O) = (v1 * v2) / ||v1|| ||v2||
    # cos(O) = (v1x*v2x + v1y*v2y) / (v1_length * v2_length)
    v1_length = math.hypot()
    v2_length = math.hypot()
    result = dot_product(vector_1, vector_2) / (v1_length, v2_length)
    angle = math.acos(result)
    return angle

# this function calculates the angle between the Player and a point
def calculate_angle_between(player, point):
    # make a Player vector
    x = math.cos(player.angle)
    y = math.sin(player.angle)
    player_vector = (x, y)

    point_x = point[0]
    point_y = point[1]

    x_distance = point_x - player.x
    y_distance = point_y - player.y
    point_vector = (x_distance, y_distance)

    # this is the distance of the Player to that Corner
    distance = math.hypot(y_distance, x_distance)

    # this is the angle from the Player to that Corner
    # according to the STANDARD grid...
    # so the Player's angle is not used in the calculations here
    corner_angle = math.atan2(y_distance, x_distance)

    # this is the angle between the "direction the Player is facing" to that Corner
    # the angle is a positive angle if the corner is to the Player's right-hand side
    # the angle is a negative angle if the corner is to the Player's left-hand side
    angle_between = math.acos(dot_product(player_vector, point_vector) / distance)

        ##################################################
        ###
        ### The following is a more thorough coding scheme so that the reader can see what is going on.
        ### It is all being commented out.
        ### Instead, more consice code is below that.
        ### The more consice code is used because it is faster (ie. less calculations)
        ### but the old code is there so that you can understand the math and what is happening.
        ###
        ################################################
        #if player.angle < 0 and corner_angle < 0:
        #    if corner_angle < player.angle:
        #        angle_between = -abs(angle_between)
        #    elif corner_angle >= player.angle:
        #        angle_between = abs(angle_between)
        #
        #if player.angle >= 0 and corner_angle >= 0:
        #    if corner_angle < player.angle:
        #        angle_between = -abs(angle_between)
        #    elif corner_angle >= player.angle:
        #        angle_between = abs(angle_between)
        #
        #if player.angle < 0 and corner_angle >= 0:
        #    if corner_angle < player.angle + math.pi:
        #        angle_between = abs(angle_between)
        #    elif corner_angle >= player.angle + math.pi:
        #        angle_between = -abs(angle_between)
        #
        #if player.angle >= 0 and corner_angle < 0:
        #    if corner_angle < player.angle - math.pi:
        #        angle_between = abs(angle_between)
        #    elif corner_angle >= player.angle - math.pi:
        #        angle_between = -abs(angle_between)
        #################################################

    if player.angle * corner_angle >= 0:
        if corner_angle < player.angle:
            angle_between = -angle_between
        else:
            None
    elif player.angle * corner_angle < 0:
        if player.angle >= 0:
            if corner_angle >= player.angle - math.pi:
                angle_between = -angle_between
            else:
                None
        elif player.angle < 0:
            if corner_angle >= player.angle + math.pi:
                angle_between = -angle_between
    else:
        None

    return angle_between


#######################################################################
# main program
#######################################################################

player = Player(init_x, init_y, speed, init_angle)  # Make the player

MODES = ["Map Mode", "Player Mode", "First-Person Mode"]
k = 0
mode = MODES[k]

PAUSE = False

# the main program
running = True
while running:
    mainClock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            PAUSE = True
        elif event.type == pygame.MOUSEBUTTONUP:
            PAUSE = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                k = (k + 1) % len(MODES)
                mode = MODES[k]
        mouseX, mouseY = pygame.mouse.get_pos()

        #if event.type == pygame.KEYUP:
        #    if event.key == pygame.K_LEFT:
        #        player.angle = player.angle - turning_speed
        #        player.angle = map_angle_to_domain(player.angle)
        #    elif event.key == pygame.K_RIGHT:
        #        player.angle = player.angle + turning_speed
        #        player.angle = map_angle_to_domain(player.angle)

    # if the game is NOT paused, then proceed with all this stuff
    if PAUSE == False:
        screen.fill(background_color) # erase screen

        # if the Player's speed is sufficiently slow enough, reset the speed to zero.
        if abs(player.speed) < 0.1:
            player.speed = 0

        # check for keyboard input
        keys=pygame.key.get_pressed()

        if keys[K_UP]:              # user presses UP arrow (moves FORWARD)
            if player.speed < 0:
                player.speed = 0.75 * player.speed
            else:
                player.speed = speed    # set the player speed (if it had been zero, it is now not zero)
        elif keys[K_DOWN]:          # user presses DOWN arrow (moves BACKWARD)
            if player.speed > 0:
                player.speed = 0.75 * player.speed
            else:
                player.speed = -speed   # set the player speed (if it had been zero, it is now not zero)
        else:
            None

        if keys[K_LEFT]:            # user presses LEFT arrow (rotate counter-clockwise)
            player.angle = player.angle - turning_speed
            player.angle = map_angle_to_domain(player.angle)
        elif keys[K_RIGHT]:         # user presses RIGHT arrow (rotate clockwise)
            player.angle = player.angle + turning_speed
            player.angle = map_angle_to_domain(player.angle)
        else:
            None

        if keys[K_a]:
            zoom_level = zoom_level + zoom_speed
        elif keys[K_z]:
            zoom_level = zoom_level - zoom_speed
        else:
            None

        # Move the player's location.
        #if check_collision(player, map) == False:
        player.move()
        player.speed = 0.9 * player.speed

        # the next IF-THEN group draws the appropriate screen
        if mode == "Player Mode":
            player.display_player_mode()
            map_display_player_mode(box, box_color, box_thickness, player.angle, zoom_level)

        elif mode == "Map Mode":
            map_display_map_mode(box, box_color, box_thickness)
            player.display_map_mode()

        elif mode == "First-Person Mode":
            map_display_first_person_mode(box, box_color, box_thickness, player.angle, zoom_level)


        else:
            None

    else:
        None

    write_mode(mode)            # display the mode on the screen (map mode, player mode, etc.)
    write_angle(player.angle)   # display the player's angle on the screen
    pygame.display.flip()       # display the new screen
