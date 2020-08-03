from room import Room
from player import Player
from world import World
from util import Stack, Queue
import random
from ast import literal_eval
from graph import Graph

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# dictionary to look up opposite direction
opposite_direction = {"n":"s", "s":"n", "e":"w", "w":"e"}

# load dictionary into graph
graph = Graph()
for k, v in room_graph.items():
    graph.add_vertex(k)
    for k1, v1 in v[1].items():
        graph.add_edge(k, '?', k1)

#Iteration continues if there is at least one vertex id (room number) with '?' value.
while(graph.not_done()):
    current_room = player.current_room
    current_exits = player.current_room.get_exits()
    found_unexplored_exit = False
    adj_dict = graph.get_neighbors(current_room.id)

    for direction in current_exits:
        # if the room in this direction is unvisited, it will have '?' instead of room number
        if adj_dict[direction] == '?':
            print(f"[DFT] Current room is {current_room.id} and direction is {direction}")
            # get the room we would reach if we followed this direction
            next_room = player.current_room.get_room_in_direction(direction)

            # link current room to next room in this direction
            adj_dict[direction] = next_room.id

            # link next room to current room in opposite direction
            graph.get_neighbors(next_room.id)[opposite_direction[direction]]=current_room.id

            # having updated references, travel to next room in this direction, this will update player.current_room
            player.travel(direction)

            # record our move
            traversal_path.append(direction)

            found_unexplored_exit = True

            # depth first traversal - break from the direction iteration of previous room, as player.current_room is set to next room
            break
    if found_unexplored_exit:
        continue
    #all adjacent rooms were visited, need to perform BFS to find shortest path
    
    print(f"[BFS] input room is {player.current_room.id}")
    path = graph.do_bfs(player.current_room.id, world)
    print(f"[BFS] discovered path is {path}")

    # iterate over the list of (direction, room) pairs 
    for i in range(1, len(path)):
        direction = path[i][0]
        player.travel(direction)
        traversal_path.append(direction)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
