#! /usr/bin/env python3
# coding: utf-8


# RECURSIVE BACTRACKING

import random
import time

from Variables_Map_Building import *


class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.up = True
        self.down = True
        self.left = True
        self.right = True
        self.visited = False
        self.dead_end = False

    def wall_test_RB(self, grid):
        """Pick a random direction and break the wall if possible"""
        self.visited = True
        if not self.dead_end:
            tries = []
            if self.i-1 >= 0 and not grid[self.i-1][self.j].visited:
                tries.append((grid[self.i-1][self.j], "Up"))
            if self.i+1 < len(grid) and not grid[self.i+1][self.j].visited:
                tries.append((grid[self.i+1][self.j], "Down"))
            if self.j-1 >= 0 and not grid[self.i][self.j-1].visited:
                tries.append((grid[self.i][self.j-1], "Left"))
            if self.j+1 < len(grid[0]) and not grid[self.i][self.j+1].visited:
                tries.append((grid[self.i][self.j+1], "Right"))
            if len(tries) != 0:
                main_cell, direction = random.choice(tries)
                if direction == "Up":
                    self.up = False
                if direction == "Down":
                    self.down = False
                if direction == "Left":
                    self.left = False
                if direction == "Right":
                    self.right = False
            else:
                main_cell = self
                self.dead_end = True
            if len(tries) == 1:
                self.dead_end = True
        else:
            main_cell = self

        return main_cell


w = 50
h = 25
number_of_players = 1


SYMBOL_WALL = "\U00002338"
SYMBOL_WALL_N = "\U0000257d"
SYMBOL_WALL_S = "\U0000257f"
SYMBOL_WALL_E = "\U0000257e"
SYMBOL_WALL_W = "\U0000257c"
SYMBOL_WALL_EW = "\U00002550"
SYMBOL_WALL_NS = "\U00002551"
SYMBOL_WALL_SE = "\U00002554"
SYMBOL_WALL_SW = "\U00002557"
SYMBOL_WALL_NE = "\U0000255A"
SYMBOL_WALL_NW = "\U0000255D"
SYMBOL_WALL_NSE = "\U00002560"
SYMBOL_WALL_NSW = "\U00002563"
SYMBOL_WALL_SEW = "\U00002566"
SYMBOL_WALL_NEW = "\U00002569"
SYMBOL_WALL_NSEW = "\U0000256C"
SYMBOL_DOOR = "\U0000254D"
SYMBOL_DOOR_VERTICAL = "\U0000254F"
SYMBOL_PLAYER = "\U0000229a"
SYMBOL_CORRIDOR = " "
SYMBOL_CORRIDOR_VISITED = "\U000022C5"
SYMBOL_FOG = "\U00002425"
SYMBOL_KEY = "\U000026b7"
BLACK_ON_WHITE = "\033[0;1;30;47m"
RED_TEXT = "\033[31m"
GREEN_TEXT = "\033[32m"
YELLOW_TEXT = "\033[33m"
BLUE_TEXT = "\033[34m"
MAGENTA_TEXT = "\033[35m"
CYAN_TEXT = "\033[36m"
WHITE_TEXT = "\033[37m"
B_RED_TEXT = "\033[1;31m"
B_GREEN_TEXT = "\033[1;32m"
B_YELLOW_TEXT = "\033[1;33m"
B_BLUE_TEXT = "\033[1;34m"
B_MAGENTA_TEXT = "\033[1;35m"
B_CYAN_TEXT = "\033[1;36m"
B_WHITE_TEXT = "\033[1;37m"
CLEAR_SCREEN = '\033[2J'
CURSOR_RESET = '\033[H'
CLR_ATTR = "\033[0m"

COLOR_PLAYER_1 = B_BLUE_TEXT
COLOR_PLAYER_2 = B_RED_TEXT


class Wall:
    def __init__(self, y, x, neighbors=False):
        self.x = x
        self.y = y
        self.end = False
        self.neighbors = neighbors
        self.has_key = False

        if self.neighbors == "N":
            self.symbol = SYMBOL_WALL_N
        elif self.neighbors == "S":
            self.symbol = SYMBOL_WALL_S
        elif self.neighbors == "E":
            self.symbol = SYMBOL_WALL_E
        elif self.neighbors == "W":
            self.symbol = SYMBOL_WALL_W
        elif self.neighbors == "EW":
            self.symbol = SYMBOL_WALL_EW
        elif self.neighbors == "NS":
            self.symbol = SYMBOL_WALL_NS
        elif self.neighbors == "SE":
            self.symbol = SYMBOL_WALL_SE
        elif self.neighbors == "SW":
            self.symbol = SYMBOL_WALL_SW
        elif self.neighbors == "NE":
            self.symbol = SYMBOL_WALL_NE
        elif self.neighbors == "NW":
            self.symbol = SYMBOL_WALL_NW
        elif self.neighbors == "NSE":
            self.symbol = SYMBOL_WALL_NSE
        elif self.neighbors == "NSW":
            self.symbol = SYMBOL_WALL_NSW
        elif self.neighbors == "SEW":
            self.symbol = SYMBOL_WALL_SEW
        elif self.neighbors == "NEW":
            self.symbol = SYMBOL_WALL_NEW
        elif self.neighbors == "NSEW":
            self.symbol = SYMBOL_WALL_NSEW
        else:
            self.symbol = SYMBOL_WALL

    def __str__(self):
        return YELLOW_TEXT+self.symbol+CLR_ATTR


class Corridor:
    def __init__(self, y, x, has_key=False):
        self.x = x
        self.y = y
        self.end = False
        self.has_key = has_key

    def __str__(self):
        symbol = SYMBOL_CORRIDOR
        if self.has_key:
            symbol = SYMBOL_KEY

        return WHITE_TEXT+symbol+CLR_ATTR


class Door:
    def __init__(self, y, x, vertical, end=False):
        self.x = x
        self.y = y
        self.end = end
        self.vertical = vertical
        self.has_key = False

    def __str__(self):
        if self.end:
            color = RED_TEXT
        else:
            color = YELLOW_TEXT
        if self.vertical:
            symbol = SYMBOL_DOOR_VERTICAL
        else:
            symbol = SYMBOL_DOOR

        return color+symbol+CLR_ATTR


class Player:
    def __init__(self, y, x, player_number=1):
        self.x = x
        self.y = y
        self.player_number = player_number


def round_to_sup_odd(x):
    """Round a number to its superior odd"""
    if x % 2 == 1:
        return x
    else:
        return x + 1


def groundwork(w, h):
    """Prepare a canvas to carve the map"""
    w = round_to_sup_odd(w)
    h = round_to_sup_odd(h)
    groundwork = []
    for i in range(h):
        groundwork.append([])
        for j in range(w):
            groundwork[i].append(LETTER_WALL)
    return groundwork


def make_str_from_2d_array(maze_map):
    """Convert a list into a string"""
    groundwork_str = ""
    for line in maze_map:
        for letter in line:
            groundwork_str += letter
        groundwork_str += "\n"
    return groundwork_str


def make_grid(w, h):
    """Make a grid of cells"""
    w = w//2
    h = h//2
    new_grid = []
    for i in range(h):
        new_grid.append([])
        for j in range(w):
            new_grid[i].append(Cell(i, j))
    return new_grid


def delete_isolated_wall(maze_map):
    """Delete isolated walls"""
    for x in range(1, len(maze_map)-2):
        for y in range(1, len(maze_map[0])-2):
            if maze_map[x][y] == LETTER_WALL:
                if (
                        maze_map[x][y-1] == LETTER_CORRIDOR and
                        maze_map[x][y+1] == LETTER_CORRIDOR and
                        maze_map[x-1][y] == LETTER_CORRIDOR and
                        maze_map[x+1][y] == LETTER_CORRIDOR):
                    maze_map[x][y] = LETTER_CORRIDOR


def find_eligible_exit(maze_map, corner):
    """Find locations for the exit"""
    eligible_exits = []
    map_width = len(maze_map[0]) - 1
    map_height = len(maze_map) - 1
    if corner == "NW":
        for i in range(1, map_width // 2):
            if maze_map[1][i] != LETTER_WALL:
                eligible_exits.append((0, i))
        for j in range(1, map_height // 2):
            if maze_map[j][1] != LETTER_WALL:
                eligible_exits.append((j, 0))
        return eligible_exits
    if corner == "NE":
        for i in range(map_width // 2, map_width):
            if maze_map[1][i] != LETTER_WALL:
                eligible_exits.append((0, i))
        for j in range(1, map_height // 2):
            if maze_map[j][map_width - 1] != LETTER_WALL:
                eligible_exits.append((j, map_width))
        return eligible_exits
    if corner == "SW":
        for i in range(1, map_width // 2):
            if maze_map[map_height - 1][i] != LETTER_WALL:
                eligible_exits.append((map_height, i))
        for j in range(map_height // 2, map_height):
            if maze_map[j][1] != LETTER_WALL:
                eligible_exits.append((j, 0))
        return eligible_exits
    if corner == "SE":
        for i in range(map_width // 2, map_width):
            if maze_map[map_height - 1][i] != LETTER_WALL:
                eligible_exits.append((map_height, i))
        for j in range(map_height // 2, map_height):
            if maze_map[j][map_width - 1] != LETTER_WALL:
                eligible_exits.append((j, map_width))
        return eligible_exits


def make_entrance_and_exit(maze_map, number_of_players):
    """Place enter and exit on the map"""
    locations = ["NW", "NE", "SW", "SE"]
    for i in range(number_of_players):
        position_start = locations.pop(random.randint(0, len(locations)-1))
        if position_start == "NW":
            maze_map[1][1] = LETTER_PLAYER[i]
        elif position_start == "NE":
            maze_map[1][len(maze_map[1])-2] = LETTER_PLAYER[i]
        elif position_start == "SW":
            maze_map[len(maze_map)-2][1] = LETTER_PLAYER[i]
        elif position_start == "SE":
            maze_map[len(maze_map)-2][len(maze_map[1])-2] = LETTER_PLAYER[i]
    corner_end = locations.pop(random.randint(0, len(locations)-1))
    eligible_exits = find_eligible_exit(maze_map, corner_end)
    location_choice = random.randint(0, len(eligible_exits)-1)
    exit_location = eligible_exits.pop(location_choice)
    maze_map[exit_location[0]][exit_location[1]] = LETTER_END


def display(maze_map):
    lines = maze_map.split("\n")
    join_with = (LETTER_WALL, LETTER_DOOR, LETTER_END)
    props = []
    players = []
    for i, line in enumerate(lines):
        for j, letter in enumerate(line):
            if letter is LETTER_PLAYER[0]:
                players.append(Player(i, j))
                props.append(Corridor(i, j))
            elif letter is LETTER_PLAYER[1]:
                players.append(Player(i, j, player_number=2))
                props.append(Corridor(i, j))
            elif letter is LETTER_END:
                vertical = False
                if j < len(line) - 1:
                    if lines[i][j + 1] not in join_with:
                        vertical = True
                if j > 0:
                    if lines[i][j - 1] not in join_with:
                        vertical = True
                props.append(Door(i, j, vertical, end=True))
            elif letter is LETTER_DOOR:
                vertical = False
                if j < len(line) - 1:
                    if lines[i][j + 1] not in join_with:
                        vertical = True
                if j > 0:
                    if lines[i][j - 1] not in join_with:
                        vertical = True
                props.append(Door(i, j, vertical))
            elif letter is LETTER_WALL:
                neighbors = ""
                if i > 0:
                    if lines[i - 1][j] in join_with:
                        neighbors += "N"
                if i < (len(lines) - 2):
                    if lines[i + 1][j] in join_with:
                        neighbors += "S"
                if j < (len(lines[0]) - 1):
                    if lines[i][j + 1] in join_with:
                        neighbors += "E"
                if j > 0:
                    if lines[i][j - 1] in join_with:
                        neighbors += "W"
                props.append(Wall(i, j, neighbors))
            elif letter is LETTER_KEY:
                props.append(Corridor(i, j, has_key=True))
            else:
                props.append(Corridor(i, j))
    maze_display = ""
    for item in props:
        is_not_player = True
        item.revealed = True
        for player in players:
            if (item.x, item.y) == (player.x, player.y):
                is_not_player = False
                if player.player_number == 1:
                    color = B_BLUE_TEXT
                else:
                    color = B_RED_TEXT
                maze_display += color + SYMBOL_PLAYER + CLR_ATTR
        if is_not_player:
            maze_display += item.__str__()
        if item.x == w:
            maze_display += "\n"
    print(CLEAR_SCREEN + CURSOR_RESET + maze_display)


grid = make_grid(w, h)
maze_map = groundwork(w, h)
main_cell = random.choice(random.choice(grid))
backtracking = []
while True:
    map_test = make_str_from_2d_array(maze_map)
    if not main_cell.dead_end:
        backtracking.append(main_cell)
        main_cell = main_cell.wall_test_RB(grid)
        for line in grid:
            for item in line:
                maze_map[item.i*2+1][item.j*2+1] = LETTER_CORRIDOR
                if not item.up:
                    maze_map[item.i*2][item.j*2+1] = LETTER_CORRIDOR
                if not item.down:
                    maze_map[item.i*2+2][item.j*2+1] = LETTER_CORRIDOR
                if not item.left:
                    maze_map[item.i*2+1][item.j*2] = LETTER_CORRIDOR
                if not item.right:
                    maze_map[item.i*2+1][item.j*2+2] = LETTER_CORRIDOR
        map_finished = make_str_from_2d_array(maze_map)
        if map_finished != map_test:
            time.sleep(0.05)
            display(map_finished)
    else:
        del backtracking[len(backtracking) - 1]
        if len(backtracking) == 0:
            break
        main_cell = backtracking[len(backtracking) - 1]
number_of_rooms = (len(maze_map)*len(maze_map[1])) // 50
if number_of_rooms == 0:
    number_of_rooms = 1
key_placed = False
eligible_spots = []
if len(maze_map) > 3 and len(maze_map[0]) > 3:
    for i in range(2, len(maze_map) - 1, 2):
        for j in range(2, len(maze_map[0]) - 1, 2):
            eligible_spots.append((i, j))
    random.shuffle(eligible_spots)
    for i in range(number_of_rooms):
        spot = eligible_spots.pop(0)
        a = spot[0]
        b = spot[1]
        maze_map[a - 1][b] = LETTER_CORRIDOR
        maze_map[a + 1][b] = LETTER_CORRIDOR
        if i % 3 == 0:
            maze_map[a][b - 1] = LETTER_CORRIDOR
            maze_map[a][b + 1] = LETTER_CORRIDOR
            if not key_placed:
                maze_map[a][b] = LETTER_KEY
                key_placed = True
        delete_isolated_wall(maze_map)
        map_finished = make_str_from_2d_array(maze_map)
        display(map_finished)
        time.sleep(0.1)
make_entrance_and_exit(maze_map, number_of_players)
map_finished = make_str_from_2d_array(maze_map)
display(map_finished)
time.sleep(0.5)
maze_map_old = []
while maze_map != maze_map_old:
    maze_map_old = [x[:] for x in maze_map]
    for x in range(2, len(maze_map)-2):
        for y in range(2, len(maze_map[0])-2):
            if maze_map[x][y] == LETTER_WALL:
                empty_spaces = []
                if maze_map[x][y-1] in (LETTER_CORRIDOR):
                    empty_spaces.append("W")
                if maze_map[x][y+1] in (LETTER_CORRIDOR):
                    empty_spaces.append("E")
                if maze_map[x-1][y] in (LETTER_CORRIDOR):
                    empty_spaces.append("N")
                if maze_map[x+1][y] in (LETTER_CORRIDOR):
                    empty_spaces.append("S")
                if len(empty_spaces) == 3:
                    door_added = False
                    random.shuffle(empty_spaces)
                    for door_try in empty_spaces:
                        if (
                                door_try == "W" and
                                maze_map[x][y-2] == LETTER_WALL):
                            maze_map[x][y-1] = LETTER_DOOR
                            door_added = True
                            break
                        elif (
                                door_try == "E" and
                                maze_map[x][y+2] == LETTER_WALL):
                            maze_map[x][y+1] = LETTER_DOOR
                            door_added = True
                            break
                        elif (
                                door_try == "N" and
                                maze_map[x-2][y] == LETTER_WALL):
                            maze_map[x-1][y] = LETTER_DOOR
                            door_added = True
                            break
                        elif (
                                door_try == "S" and
                                maze_map[x+2][y] == LETTER_WALL):
                            maze_map[x+1][y] = LETTER_DOOR
                            door_added = True
                            break
                    if not door_added:
                        maze_map[x][y] = LETTER_CORRIDOR
                        maze_map[x-1][y] = LETTER_CORRIDOR
                        maze_map[x+1][y] = LETTER_CORRIDOR
                        maze_map[x][y-1] = LETTER_CORRIDOR
                        maze_map[x][y+1] = LETTER_CORRIDOR
                        delete_isolated_wall(maze_map)
                    map_finished = make_str_from_2d_array(maze_map)
                    display(map_finished)
                    time.sleep(0.1)
