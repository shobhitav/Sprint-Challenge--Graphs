"""
Simple graph implementation - edge names are directions {'n','e','w','s'} and vertices are room numbers
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        # for key vertex_id 
        self.vertices[vertex_id]={}
 
    def add_edge(self, v1, v2, edge_name):
        """
        Add a directed edge to the graph.
        """
        self.vertices[v1][edge_name]=v2

    def get_neighbors(self, vertex_id):
        """
        Get the dictionary mapping connecting edge name to neighboring vertex id.
        """
        return self.vertices[vertex_id]

    def not_done(self):
        """
        Returns False if there is at least one vertex id (room number) with '?' value.
        """
        for v in self.vertices.values():
            for v1 in v.values():
                if v1 == '?':
                    return True
        return False

    #returns a shortest path from the current_room whose neighbors are explored/visited to a room that has not been explored yet
    def do_bfs(self, current_room_id, world):
        qq = Queue()
        
        # we don't care which direction took us to current room (we only want to create shortest path from current room to next unexplored room)
        qq.enqueue([('<direction>', current_room_id)])
        visited = set() #already seen 
        visited.add(current_room_id)
        
        while qq.size() > 0:
            curr_path = qq.dequeue()
            curr_room_pair = curr_path[-1]
            curr_room = world.rooms[curr_room_pair[1]]
            adj_dict = self.get_neighbors(curr_room.id)

            for direction in curr_room.get_exits():
                if adj_dict[direction] == '?':            
                    curr_path.append((direction, curr_room.get_room_in_direction(direction).id))
                    return curr_path
                elif curr_room.get_room_in_direction(direction).id not in visited:
                    new_room = curr_room.get_room_in_direction(direction)
                    new_path = curr_path.copy()
                    new_path.append((direction, new_room.id))
                    visited.add(new_room.id)
                    qq.enqueue(new_path)        

