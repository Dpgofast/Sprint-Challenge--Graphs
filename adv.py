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
                    # otherwise path is already explored
                else:
                    lost = list(path)
                    lost.append(graph[last_room][exit])
                    cue.enqueue(lost)
    return []


def cue_moves(player, moves_cue):
    # current exits for the room currently in
    current_exits = graph[player.current_room.id]
    # track exits we havent tried
    untried_exits = []
    # for every valid direction from where we are
    for direction in current_exits:
        # If we find one unexplored path
        if current_exits[direction] == "?":
            # put it on the list to check out
            untried_exits.append(direction)
    # if we run out of unknowns
    if len(untried_exits) == 0:
        # list unknown paths to explore
        unexplored = spelunk(player, moves_cue)
        # track where we are
        room_num = player.current_room.id
        # go through list of unexplored paths
        for next in unexplored:
            # go through all possible moves in each room
            for direction in graph[room_num]:
                # if the room has an unexplored path available
                if graph[room_num][direction] == next:
                    # explore and add to the queue of moves
                    moves_cue.enqueue(direction)
                    # Exhaust all options
                    room_num = next
                    break
    # otherwise start down a random path
    else:
        moves_cue.enqueue(untried_exits[random.randint(0, len(untried_exits) - 1)])


# set iteration limit
tries = 100
# Track our best score 997 was my best in previous iteration
optimum_len = 997
# Track the optimum path to take
optimum_path = []
# run until max max tries
for x in range(tries):
    # initialize player in the world
    player = Player(world.starting_room)
    # initialize graph
    graph = {}
    # start in a new room
    fresh_room = {}
    # check the possible directions/exits in the room
    for direction in player.current_room.get_exits():
        # mark all exits as unexplored
        fresh_room[direction] = "?"
    # add the new room and exits to the graph at the starting room id index
    graph[world.starting_room.id] = fresh_room
    # Initialize a queue for the moves
    moves_cue = Queue()
    # keep track of moves in a list
    total_moves = []
    # start exploring
    cue_moves(player, moves_cue)
    #change directions to go backward through
    reverse_compass = {"n": "s", "s": "n", "e": "w", "w": "e"}
    # while possible moves/unexplored areas
    while moves_cue.size() > 0:
        # track starting room
        starting = player.current_room.id
        # get next path from queue
        next = moves_cue.dequeue()
        # explore path
        player.travel(next)
        # add to list of moves
        total_moves.append(next)
        # track where you end up
        end = player.current_room.id
        # add to graph connections
        graph[starting][next] = end
        # if connection not there
        if end not in graph:
            # set it
            graph[end] = {}
            # for each exit in possible exits from location
            for exit in player.current_room.get_exits():
                # mark as unexplored
                graph[end][exit] = "?"
        # go back from whence you came
        graph[end][reverse_compass[next]] = starting
        # if you run out of moves in queue
        if moves_cue.size() == 0:
            # check again and explore
            cue_moves(player, moves_cue)
    # if we beat our previous score
    if len(total_moves) < optimum_len:
        # our best path is the one we just explored
        optimum_path = total_moves
        # best move count is our last iteration
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
