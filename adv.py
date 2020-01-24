from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


# def traverse(graph):
#     # placeholder for all
#     maze = []
#     # placeholder for rooms
#     rooms = []
#     # set of visited rooms
#     visited = set()
#     # initialize maze with 0
#     maze.append(0)

#     while len(visited) < len(graph):
#         current = maze[-1]
#         visited.add(current)
#         conns = graph[current][-1]
#         open_conns = []
#         for looked, unlooked in conns.items():
#             if unlooked not in visited:
#                 open_conns.append(unlooked)
#         if len(open_conns) > 0:
#             room = open_conns[0]
#             maze.append(open_conns[0])
#         else:
#             room = maze[-2]
#             maze.pop()

#         for last_room, exits in conns.items():
#             if exits == room:
#                 rooms.append(last_room)
#     return rooms
# !!!! TESTS PASSED: 997 moves, 500 rooms visited !!!!
# This works but lets try with queue

# Explore the unknown or rather find it
def spelunk(player, moves_cue):
    # init queue
    cue = Queue()
    # init set for visited rooms
    visited = set()
    # add current room to queue
    cue.enqueue([player.current_room.id])
    # if queue is bigger than 0 there are things to explore
    while cue.size() > 0:
        # as path is explored removefrom queue
        path = cue.dequeue()
        # keep track of last room visited
        last_room = path[-1]
        # if the last room was not in previously visited
        if last_room not in visited:
            # add to list of visited
            visited.add(last_room)
            # Find all the exits for the room
            for exit in graph[last_room]:
                # if we find an exit in the room that is unexplored
                if graph[last_room][exit] == "?":
                    # add path to list to explore
                    return path
                    # otherwise remove path as already explored
                else:
                    lost = list(path)
                    lost.append(graph[last_room][exit])
                    cue.enqueue(lost)
    return []


def cue_moves(player, moves_cue):
    current_exits = graph[player.current_room.id]
    untried_exits = []
    for direction in current_exits:
        if current_exits[direction] == "?":
            untried_exits.append(direction)
    if len(untried_exits) == 0:
        unexplored = spelunk(player, moves_cue)
        room_num = player.current_room.id
        for next in unexplored:
            for direction in graph[room_num]:
                if graph[room_num][direction] == next:
                    moves_cue.enqueue(direction)
                    room_num = next
                    break
    else:
        moves_cue.enqueue(untried_exits[random.randint(0, len(untried_exits) - 1)])


tries = 100
optimum_len = 997
optimum_path = []
for x in range(tries):
    player = Player(world.starting_room)
    graph = {}

    fresh_room = {}
    for direction in player.current_room.get_exits():
        fresh_room[direction] = "?"
    graph[world.starting_room.id] = fresh_room

    moves_cue = Queue()
    total_moves = []
    cue_moves(player, moves_cue)

    reverse_compass = {"n": "s", "s": "n", "e": "w", "w": "e"}

    while moves_cue.size() > 0:
        starting = player.current_room.id
        next = moves_cue.dequeue()
        player.travel(next)
        total_moves.append(next)
        end = player.current_room.id
        graph[starting][next] = end
        if end not in graph:
            graph[end] = {}
            for exit in player.current_room.get_exits():
                graph[end][exit] = "?"
        graph[end][reverse_compass[next]] = starting
        if moves_cue.size() == 0:
            cue_moves(player, moves_cue)
    if len(total_moves) < optimum_len:
        optimum_path= total_moves
        optimum_len = len(total_moves)

# !!!! TESTS PASSED: 974 moves, 500 rooms visited !!!

traversal_path = optimum_path

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
