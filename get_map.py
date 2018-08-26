import cv2
import numpy as np
from pprint import pprint
import json
import random

import pyastar

from time import time
from os.path import basename, join, splitext

# input/output files
MAZE_FPATH = join('mazes', 'maze_small.png')
# MAZE_FPATH = join('mazes', 'maze_large.png')
OUTP_FPATH = ('map_with_path.png')

locs = {'deli meats': (12, 14)
        , 'beer': (7, 16)
        , 'wine': (18, 16)
        , 'soda': (12, 17)
        , 'chips': (12, 19)
        , 'cookies': (7, 20)
        , 'crackers': (18, 20)
        , 'bottled juice': (4, 22)
        , 'canned juice': (11, 22)
        , 'asceptics': (16, 22)
        , 'isotonics': (21, 22)
        , 'candy': (4, 23)
        , 'popcorn': (11, 23)
        , 'snack nuts': (16, 23)
        , 'snacks': (21, 23)
        , 'bread': (5, 25)
        , 'tortillas': (12, 25)
        , 'pastries': (20, 25)
        , 'condiments': (3, 26)
        , 'pickles': (7, 26)
        , 'vinegar': (10, 26)
        , 'salad dressing': (13, 26)
        , 'peanut butter': (18, 26)
        , 'jam': (22, 26)
        , 'jelly': (22, 26)
        , 'canned meat': (4, 28)
        , 'rice': (9, 28)
        , 'dried beans': (12, 28)
        , 'goya': (15, 28)
        , 'jalapenoes': (18, 28)
        , 'picante': (22, 28)
        , 'pasta': (3, 29)
        , 'pasta sauce': (7, 29)
        , 'canned tomatoes': (12, 29)
        , 'canned pasta': (18, 29)
        , 'gravy mix': (21, 29)
        , 'canned beans': (7, 31)
        , 'dried fruit': (15, 31)
        , 'canned fruit': (7, 31)
        , 'deli': (23, 6)
        , 'bakery': (28, 6)
        , 'flowers': (7, 3)
        , 'market': (29, 20)
        , 'seafood': (30, 34)
        }

shelves = [([1, 25], [15, 15])
           , ([1, 25], [18, 18])
           , ([1, 25], [21, 21])
           , ([1, 25], [24, 24])
           , ([1, 25], [27, 27])
           , ([1, 25], [30, 30])
           , ([10, 12], [9, 12])
           , ([14, 17], [9, 12])
           , ([19, 22], [10, 10])
           , ([24, 26], [10, 10])
           , ([28, 30], [10, 10])
           , ([27, 29], [15, 27])
           , ([10, 17], [5, 5])
           , ([19, 25], [5, 5])
           , ([27, 30], [5, 5])
           , ([8, 8], [0, 6])
           , ([28, 30], [32, 34])
           ]


def main(food):
    #  maze = cv2.imread(MAZE_FPATH)
    #  if maze is None:
    #      print('no file found: %s' % (MAZE_FPATH))
    #      return
    #  else:
    #      print('loaded maze of shape %r' % (maze.shape[0:2],))

    #  grid = cv2.cvtColor(maze, cv2.COLOR_BGR2GRAY).astype(np.float32)
    grid_size = (32, 35)
    grid = np.ones(grid_size, dtype=np.float32)
    maze = np.ones((grid_size[0], grid_size[1], 3), dtype=np.float32)
    for row_rng, col_rng in shelves:
        row_lower = row_rng[0]
        row_upper = row_rng[1]
        col_lower = col_rng[0]
        col_upper = col_rng[1]
        if row_upper == row_lower:
            for j in range(col_lower, col_upper):
                grid[row_upper, j] = np.inf
                maze[row_upper, j] = (0, 0, 0)
        elif col_upper == col_lower:
            for i in range(row_lower, row_upper):
                grid[i, col_upper] = np.inf
                maze[i, col_upper] = (0, 0, 0)
        else:
            for i in range(row_lower, row_upper):
                for j in range(col_lower, col_upper):
                    grid[i, j] = np.inf
                    maze[i, j] = (0, 0, 0)
    assert grid.min() == 1, 'cost of moving must be at least 1'
    output = {'shelves': maze.tolist()
              , 'size': grid_size}

    # start is the first white block in the top row
    start_j, = np.where(grid[-1, :] == 1)
    start = tuple(np.array([0, start_j[0]]))

    # end is the first white block in the final column
    #  end_i, = np.where(grid[:, -1] == 1)
    #  end = np.array([end_i[0], grid.shape[0] - 1])
    ends = []
    if isinstance(food, str):
        ends.append(locs[food])
    elif isinstance(food, list):
        for item in food:
            item_name = item.lower()
            if item_name not in list(locs.keys()):
                raise ValueError('Unsupported food item, supported foods are %s'
                                 % ', '.join(locs.keys()))
            else:
                ends.append(locs[item])

    def find_closest(point, ends):
        shortest_dist = float('inf')
        for end in ends:
            dist = np.linalg.norm(np.array(end) - np.array(point))
            if dist == 0:
                continue
            else:
                if dist < shortest_dist:
                    shortest_dist = dist
                    closest_point = end
        return closest_point

    order = {}
    ends_scrap = [start, *ends.copy()]
    end = start
    print(end)
    for i in range(len(ends_scrap)-1):
        closest = find_closest(end, ends_scrap)
        print(closest)
        print(ends_scrap)
        ends_scrap.remove(end)
        order[end] = closest
        end = closest

    # set allow_diagonal=True to enable 8-connectivity
    path_color = (1, 1, 0)
    for end in ends:
        path = pyastar.astar_path(grid, start, end, allow_diagonal=False)
        start = end
        output['path'] = path.tolist()

        if path.shape[0] > 0:
            maze[path[:, 0], path[:, 1]] = maze[path[:, 0], path[:, 1]] - path_color
            print('plotting path to %s'
                  % ([key for key, value in locs.items() if value == end][0]))
        else:
            print('no path found')
        path_color = (random.uniform(0.1, 0.5),
                      random.uniform(0.1, 0.3),
                      random.uniform(0.1, 0.5)
                      )
        maze_out = np.repeat(maze, 20, axis=0)
        maze_out = np.repeat(maze_out, 20, axis=1)
        maze_out = np.flipud(maze_out)
        cv2.imshow("image", maze_out)
        cv2.waitKey()

    print('done')
    with open('map.json', 'w') as outfile:
        json.dump(output, outfile)
    cv2.imwrite(OUTP_FPATH, maze_out)


if __name__ == '__main__':
    food = list(locs.keys())[:10]
    main(food)
