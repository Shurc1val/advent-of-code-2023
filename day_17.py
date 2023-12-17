from itertools import chain
import pytest

from read_data_function import read_data

# ----- PART ONE -----


def traverse_edge(heat_grid: list[list[int]], heat_loss_map: list[list[str]], traversals: list[list], current: list[int], change: list[int], heat_lost: int = 0, line_count: int = 0):
    
    directions = [
        [0,1],
        [0,-1],
        [1,0],
        [-1,0]
    ]
    if current != [0,0]:
        directions.remove([(-1)*num for num in change])
    if current[0] == 0:
        directions.remove([-1,0])
    if current[0] == len(heat_grid) - 1:
        directions.remove([1,0])
    if current[1] == 0:
        directions.remove([0,-1])
    if current[1] == len(heat_grid[0]) - 1:
        directions.remove([0,1])
    if (line_count == 3) and (change in directions):
        directions.remove(change)

    for direction in directions:
        next = list(map(lambda a,b: a + b, current, direction))
        next_heat_lost = heat_lost + heat_grid[next[0]][next[1]]
        count = line_count + 1
        if direction != change:
            count = 1
        recorded_heat_losses = heat_loss_map[next[0]][next[1]].get(str(direction), [])
        better_routes = []
        worse_routes = []
        for heat_loss in recorded_heat_losses:
            if (heat_loss['count'] <= count) and (heat_loss['loss'] <= next_heat_lost):
                better_routes.append(heat_loss)
            elif (heat_loss['count'] >= count) and (heat_loss['loss'] >= next_heat_lost):
                worse_routes.append(heat_loss)
        
        if better_routes == []:
            if heat_loss_map[next[0]][next[1]].get(str(direction)) is None:
                heat_loss_map[next[0]][next[1]][str(direction)] = []
            else:
                for route in worse_routes:
                    pass
                    heat_loss_map[next[0]][next[1]][str(direction)].remove(route)

            heat_loss_map[next[0]][next[1]][str(direction)].append({
                'loss': next_heat_lost,
                'count': count
            })

            traversals.append([next, direction, next_heat_lost, count])

    
def find_path(heat_grid: list[list[int]], heat_loss_map: list[list[str]]):
    traversals = [[[0,0], [0,1], 0, 0]]

    for edge in traversals:
        traverse_edge(heat_grid, heat_loss_map, traversals, *edge)


def part_one(str_input: str):
    heat_grid = [[int(num) for num in list(line)] for line in str_input.split('\n')]
    heat_loss_map = [[{} for i in range(len(row))] for row in heat_grid]
    for direction in [[0,1], [0,-1], [1,0], [-1,0]]:
        heat_loss_map[0][0][str(direction)] = [{
            'loss': 0,
            'count': 0
        }]
    find_path(heat_grid, heat_loss_map)
    print(list(chain.from_iterable(heat_loss_map[-1][-1].values())))
    return min([heat_loss['loss'] for heat_loss in list(chain.from_iterable(heat_loss_map[-1][-1].values()))])


def test_part_one():
    assert part_one("""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""") == 102


# ----- PART TWO -----


def cell_in_grid(heat_grid: list[list[int]], cell: list[int]) -> bool:
    if (cell[0] < 0) or (cell[0] >= len(heat_grid)):
        return False
    if (cell[1] < 0) or (cell[1] >= len(heat_grid[0])):
        return False
    return True


def traverse_edge_ultra(heat_grid: list[list[int]], heat_loss_map: list[list[str]], traversals: list[list], current: list[int], change: list[int], heat_lost: int = 0, line_count: int = 0):
    
    directions = [
        [0,1],
        [0,-1],
        [1,0],
        [-1,0]
    ]
    if current != [0,0]:
        directions.remove([(-1)*num for num in change])
    if current[0] == 0:
        directions.remove([-1,0])
    if current[0] == len(heat_grid) - 1:
        directions.remove([1,0])
    if current[1] == 0:
        directions.remove([0,-1])
    if current[1] == len(heat_grid[0]) - 1:
        directions.remove([0,1])
    if (line_count == 10) and (change in directions):
        directions.remove(change)

    for direction in directions:
        count = line_count + 1
        if direction != change:
            count = 4
        if count == 4:
            next = list(map(lambda a,b: a + 4*b, current, direction))
            if not cell_in_grid(heat_grid, next):
                continue
            next_heat_lost = heat_lost + sum([heat_grid[cell[0]][cell[1]] for cell in [list(map(lambda a,b: a + i*b, current, direction)) for i in range(1,5)]])
        else:
            next = list(map(lambda a,b: a + b, current, direction))
            next_heat_lost = heat_lost + heat_grid[next[0]][next[1]]
        recorded_heat_losses = heat_loss_map[next[0]][next[1]].get(str(direction), [])
        better_routes = []
        worse_routes = []
        for heat_loss in recorded_heat_losses:
            if (heat_loss['count'] <= count) and (heat_loss['loss'] <= next_heat_lost):
                better_routes.append(heat_loss)
            elif (heat_loss['count'] >= count) and (heat_loss['loss'] >= next_heat_lost):
                worse_routes.append(heat_loss)
        
        if better_routes == []:
            if heat_loss_map[next[0]][next[1]].get(str(direction)) is None:
                heat_loss_map[next[0]][next[1]][str(direction)] = []
            else:
                for route in worse_routes:
                    pass
                    heat_loss_map[next[0]][next[1]][str(direction)].remove(route)

            heat_loss_map[next[0]][next[1]][str(direction)].append({
                'loss': next_heat_lost,
                'count': count
            })

            traversals.append([next, direction, next_heat_lost, count])


def find_path_ultra(heat_grid: list[list[int]], heat_loss_map: list[list[str]]):
    traversals = [[[0,0], [0,1], 0, 0]]

    for edge in traversals:
        traverse_edge_ultra(heat_grid, heat_loss_map, traversals, *edge)


def part_two(str_input: str):
    heat_grid = [[int(num) for num in list(line)] for line in str_input.split('\n')]
    heat_loss_map = [[{} for i in range(len(row))] for row in heat_grid]
    for direction in [[0,1], [0,-1], [1,0], [-1,0]]:
        heat_loss_map[0][0][str(direction)] = [{
            'loss': 0,
            'count': 0
        }]
    find_path_ultra(heat_grid, heat_loss_map)
    print(list(chain.from_iterable(heat_loss_map[-1][-1].values())))
    return min([heat_loss['loss'] for heat_loss in list(chain.from_iterable(heat_loss_map[-1][-1].values()))])


def test_part_two():
    assert part_two("""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""") == 94


# --------------------


if __name__ == "__main__":
    #print(part_one(read_data("day_17.txt")))
    print(part_two(read_data("day_17.txt")))