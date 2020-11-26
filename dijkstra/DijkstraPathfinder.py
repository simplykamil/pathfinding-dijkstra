import pygame

import mazecreator.picasso as picasso
import mazecreator.settings as settings
from mazecreator.Creator import Creator
from mazecreator.SquareState import SquareState


class DijkstraPathfinder:
    @staticmethod
    def find_path():
        def _get_start_and_end_pos():
            start_pos, end_pos = None, None
            for row in grid:
                for square in row:
                    if square.state == SquareState.START:
                        start_pos = square.row, square.col
                    elif square.state == SquareState.END:
                        end_pos = square.row, square.col

            return start_pos, end_pos

        def _get_valid_neighbours(r: int, c: int):
            """
            Find valid neighbours for a square:
            valid means it's not a wall, has not been visited
            :param r: row
            :param c: column
            :return: valid neighbours
            :rtype: list()
            """

            up_neighbour = (r, c + 1)
            down_neighbour = (r, c - 1)
            left_neighbour = (r - 1, c)
            right_neighbour = (r + 1, c)

            neighbours = [up_neighbour, down_neighbour, left_neighbour, right_neighbour]
            v_neighbours = list()

            for neighbour in neighbours:
                r, c = neighbour
                if r in range(settings.ROWS) and c in range(settings.ROWS):
                    if grid[r][c].state not in [SquareState.VISITED, SquareState.WALL, SquareState.START]:
                        v_neighbours.append(neighbour)

            return v_neighbours

        def _reconstruct_path():
            path = [end_pos]
            current = end_pos

            while prev[current]:
                path.append(prev[current])
                current = prev[current]
                # print(u)

            path.reverse()
            return path

        WINDOW = pygame.display.set_mode((800, 800))
        grid = Creator.get_grid()

        start_pos, end_pos = _get_start_and_end_pos()

        print()
        print(f'Starting position: {start_pos}')
        print(f'Ending position: {end_pos}')
        print()

        dist = {}
        prev = {}
        q = list()

        finished = False

        while not finished:

            for row in grid:
                for square in row:
                    pos = square.get_pos()

                    dist[square.get_pos()] = float("inf")
                    prev[square.get_pos()] = None
                    if square.state in [SquareState.EMPTY, SquareState.START, SquareState.END]:
                        q.append(pos)

            dist[start_pos] = 0

            while q:
                u = min(q, key=dist.__getitem__)
                q.remove(u)

                for v in _get_valid_neighbours(*u):
                    alt = dist[u] + 1

                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u

                        vr, vc = v
                        grid[vr][vc].change_state(SquareState.VISITED)

                    if v == end_pos:
                        q = list()
                        break

                picasso.draw(WINDOW, grid)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finished = True
                        q = list()
                        break

            path = _reconstruct_path()

            for square in path:
                row, col = square
                grid[row][col].change_state(SquareState.PATH)
                picasso.draw(WINDOW, grid)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finished = True
                        break

        print(f'Path found, took {len(path)} moves')
        print(f'Moves: {path}')
        print()

        pygame.quit()


if __name__ == '__main__':
    DijkstraPathfinder.find_path()
