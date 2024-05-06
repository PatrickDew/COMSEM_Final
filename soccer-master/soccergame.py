import pgzero
import pgzrun
import pygame
import math
import sys
import random
from enum import Enum
from pygame.math import Vector2

# Check Pygame Zero version
pgzero_ver = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split('.')]
if pgzero_ver < [1,2]:
    print("This game requires at least version 1.2 of Pygame Zero. You have version {0}. Please upgrade using the command 'pip3 install --upgrade pgzero'".format(pgzero.__version__))
    sys.exit()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480
GAME_TITLE = "Soccer"

HALF_WINDOW_WIDTH = WINDOW_WIDTH / 2

LEVEL_WIDTH = 1000
LEVEL_HEIGHT = 1400
HALF_LEVEL_WIDTH = LEVEL_WIDTH // 2
HALF_LEVEL_HEIGHT = LEVEL_HEIGHT // 2

HALF_PITCH_WIDTH = 442
HALF_PITCH_HEIGHT = 622

GOAL_WIDTH = 186
GOAL_DEPTH = 20
HALF_GOAL_WIDTH = GOAL_WIDTH // 2

PITCH_BOUNDS_X = (HALF_LEVEL_WIDTH - HALF_PITCH_WIDTH, HALF_LEVEL_WIDTH + HALF_PITCH_WIDTH)
PITCH_BOUNDS_Y = (HALF_LEVEL_HEIGHT - HALF_PITCH_HEIGHT, HALF_LEVEL_HEIGHT + HALF_PITCH_HEIGHT)

GOAL_BOUNDS_X = (HALF_LEVEL_WIDTH - HALF_GOAL_WIDTH, HALF_LEVEL_WIDTH + HALF_GOAL_WIDTH)
GOAL_BOUNDS_Y = (HALF_LEVEL_HEIGHT - HALF_PITCH_HEIGHT - GOAL_DEPTH,
                 HALF_LEVEL_HEIGHT + HALF_PITCH_HEIGHT + GOAL_DEPTH)

PITCH_RECT = pygame.rect.Rect(PITCH_BOUNDS_X[0], PITCH_BOUNDS_Y[0], HALF_PITCH_WIDTH * 2, HALF_PITCH_HEIGHT * 2)
GOAL_0_RECT = pygame.rect.Rect(GOAL_BOUNDS_X[0], GOAL_BOUNDS_Y[0], GOAL_WIDTH, GOAL_DEPTH)
GOAL_1_RECT = pygame.rect.Rect(GOAL_BOUNDS_X[0], GOAL_BOUNDS_Y[1] - GOAL_DEPTH, GOAL_WIDTH, GOAL_DEPTH)

AI_MIN_X = 78
AI_MAX_X = LEVEL_WIDTH - 78
AI_MIN_Y = 98
AI_MAX_Y = LEVEL_HEIGHT - 98

PLAYER_START_POSITIONS = [(350, 550), (650, 450), (200, 850), (500, 750), (800, 950), (350, 1250), (650, 1150)]

LEAD_DISTANCE_1 = 10
LEAD_DISTANCE_2 = 50

DRIBBLE_DIST_X, DRIBBLE_DIST_Y = 18, 16

PLAYER_DEFAULT_SPEED = 2
CPU_PLAYER_WITH_BALL_BASE_SPEED = 2.6
PLAYER_INTERCEPT_BALL_SPEED = 2.75
LEAD_PLAYER_BASE_SPEED = 2.9
HUMAN_PLAYER_WITH_BALL_SPEED = 3
HUMAN_PLAYER_WITHOUT_BALL_SPEED = 3.3

DEBUG_SHOW_LEADS = False
DEBUG_SHOW_TARGETS = False
DEBUG_SHOW_PEERS = False
DEBUG_SHOW_SHOOT_TARGET = False
DEBUG_SHOW_COSTS = False

# Difficulty settings
class Difficulty:
    def __init__(self, goalie_enabled, second_lead_enabled, speed_boost, holdoff_timer):
        self.goalie_enabled = goalie_enabled
        self.second_lead_enabled = second_lead_enabled
        self.speed_boost = speed_boost
        self.holdoff_timer = holdoff_timer

DIFFICULTY_LEVELS = [Difficulty(False, False, 0, 120), Difficulty(False, True, 0.1, 90), Difficulty(True, True, 0.2, 60)]

# Custom math functions
def sin(x):
    return math.sin(x*math.pi/4)

def cos(x):
    return sin(x+2)

# Convert vector to angle
def vector_to_angle(vec):
    return int(4 * math.atan2(vec.x, -vec.y) / math.pi + 8.5) % 8

# Convert angle to vector
def angle_to_vector(angle):
    return Vector2(sin(angle), -cos(angle))

# Function to calculate distance key for sorting
def distance_key(pos):
    return lambda p: (p.vpos - pos).length()

# Safe normalization of vector
def safe_normalize(vec):
    length = vec.length()
    if length == 0:
        return Vector2(0,0), 0
    else:
        return vec.normalize(), length

# Custom Actor class
class CustomActor(Actor):
    def __init__(self, img, x=0, y=0, anchor=None):
        super().__init__(img, (0, 0), anchor=anchor)
        self.vpos = Vector2(x, y)

    def draw(self, offset_x, offset_y):
        self.pos = (self.vpos.x - offset_x, self.vpos.y - offset_y)
        super().draw()

# Ball physics function
KICK_STRENGTH = 11.5
DRAG = 0.98

def ball_physics(position, velocity, bounds):
    position += velocity

    if position < bounds[0] or position > bounds[1]:
        position, velocity = position - velocity, -velocity

    return position, velocity * DRAG

# Function to calculate steps required to cover a distance
def calculate_steps(distance):
    steps, velocity = 0, KICK_STRENGTH

    while distance > 0 and velocity > 0.25:
        distance, steps, velocity = distance - velocity, steps + 1, velocity * DRAG

    return steps
