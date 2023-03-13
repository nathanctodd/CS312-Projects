#!/usr/bin/python3


from CS312Graph import *
import time
import math


class Node:
    left_child = None
    right_child = None
    value = float('inf')

class Heap_Priority_Queue:

    q_heap_array = []
    q_pointer_array = dict()

    def insert(self, node_id, dist):                    
        self.q_pointer_array[node_id] = len(self.q_heap_array)  # O(1)
        self.q_heap_array.append(node_id)                       # O(1)
        self.bubble_up(len(self.q_heap_array) - 1 , dist)       # O( log(V))
                                                                # Total: O( log(V) )


    def make_queue(self, nodes, dist):      
        for i in range(len(nodes)):         # O( |V| )
            self.insert(i, dist)            # Total: O( |V| )


    def bubble_up(self, node_id, dist):
        parent_node = math.floor((node_id - 1) / 2)
        if node_id > 0:
            is_above_zero = True
        else:
            is_above_zero = False
        while is_above_zero and (dist[self.q_heap_array[node_id]] < dist[self.q_heap_array[parent_node]]):  # O( log(V) )
            temp = self.q_heap_array[node_id]                                                               # O(1)
            self.q_heap_array[node_id] = self.q_heap_array[math.floor((node_id - 1)/2)]                     # O(1)
            self.q_heap_array[math.floor((node_id - 1)/2)] = temp                                           # O(1)
            self.q_pointer_array[node_id] = math.floor((node_id - 1)/2)                                     # O(1)
            self.q_pointer_array[math.floor((node_id - 1)/2)] = node_id
            node_id = parent_node
            parent_node = math.floor((node_id - 1) / 2)
            if node_id <= 0:
                is_above_zero = False
                                                                                                            # Total: O( log(V) )

    def delete_min(self, dist):
        deleted_element = self.q_heap_array[0]               # O(1)
        last_element = self.q_heap_array[-1]                 # O(1)
        self.q_pointer_array[last_element] = None            # O(1)
        self.q_heap_array[0] = last_element                  # O(1)
        self.q_heap_array.pop()                              # O(1)
        self.bubble_down(dist)                               # O( log(V) )
        return deleted_element                               # Total: O( log(V) )

    def switch_left_child(self, dist, current_node):
        temp = self.q_heap_array[current_node]
        self.q_heap_array[current_node] = self.q_heap_array[(current_node * 2) + 1]
        self.q_heap_array[(current_node * 2) + 1] = temp
        self.q_pointer_array[current_node] = current_node * 2 + 1
        self.q_pointer_array[current_node*2+1] = current_node

    def switch_right_child(self, dist, current_node):
        temp = self.q_heap_array[current_node]
        self.q_heap_array[current_node] = self.q_heap_array[(current_node*2)+2]
        self.q_heap_array[(current_node*2)+2] = temp
        self.q_pointer_array[current_node] = current_node * 2 + 2
        self.q_pointer_array[current_node*2+2] = current_node


    def has_more_children(self, current_node):
        if ((current_node * 2) + 2) < (len(self.q_heap_array)):
            return 2
        elif (current_node * 2) + 1 < (len(self.q_heap_array)):
            return 1
        else:
            return 0


    def bubble_down(self, dist):
        current_node = 0
        if self.has_more_children(current_node) > 0:                                                               # O(1)
            has_no_more_lower_children = False
        else:
            has_no_more_lower_children = True  
                                                                             
        while has_no_more_lower_children != True:                                                                              # O( log(V) )
            if self.has_more_children(current_node) == 2:
                if dist[self.q_heap_array[current_node*2 + 1]] < dist[self.q_heap_array[(current_node*2)+ 2]]:     # O(1)
                    if dist[self.q_heap_array[current_node*2 + 1]] < dist[self.q_heap_array[current_node]]:        # O(1)
                        self.switch_left_child(dist, current_node)                                                 # O(1)
                        current_node = current_node * 2 + 1
                    else:
                        has_no_more_lower_children = True
                else:
                    if dist[self.q_heap_array[current_node*2 + 2]] < dist[self.q_heap_array[current_node]]:        # O(1)
                        self.switch_right_child(dist, current_node)                                                # O(1)
                        current_node = current_node * 2 + 2
                    else:
                        has_no_more_lower_children = True
            elif self.has_more_children(current_node) == 1:                                                        # O(1)
                if dist[self.q_heap_array[current_node*2 + 1]] < dist[self.q_heap_array[current_node]]:            # O(1)
                    self.switch_left_child(dist, current_node)                                                     # O(1)
                    current_node = current_node * 2 + 1
                else:
                    has_no_more_lower_children = True
            if self.has_more_children(current_node) == 0:
                has_no_more_lower_children = True                                                                  # Total: O( log(V) )




class Array_Priority_Queue:
    dictionary = dict()
    q_array = []
    def insert(self, node, distance):                               
        self.q_array.append(node)                                   # O(1)
        self.dictionary[node] = distance                            # O(1)
                                                                    # Total: O(1)


    def decrease_key(self, node, distance):                         
        self.dictionary[node] = distance                            # O(1)
                                                                    # Total: O(1)

    def delete_min(self):
        lowest_distance = float('inf')
        lowest_node_index = None
        for i in self.dictionary:                                   # O( |V| )
            if lowest_node_index == None:                           # O(1)
                lowest_node_index = i
            if self.dictionary.get(i) < lowest_distance:            # O(1)
                lowest_distance = self.dictionary.get(i)            # O(1)
                lowest_node_index = i
        if len(self.q_array) != 0:                                  # O(1)
            self.dictionary.pop(lowest_node_index)                  # O(1)
            self.q_array.remove(lowest_node_index)                  # O(1)
        return lowest_node_index                                    # Total: O( |V| )
        
        
    def make_queue(self, nodes, dist):
        for i in range(len(nodes)):                                 # O( |V| )
            self.dictionary[i] = dist[i]                            # O(1)
            self.q_array.append(i)                                  # O(1)



class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex):                  # O( |V| )
        self.dest = destIndex
        path_edges = []
        total_length = 0
        end_node = destIndex
        current_node = end_node
        previous_node = self.prev[current_node]
        while previous_node != None:
            distance = math.sqrt(   (math.pow((self.network.nodes[current_node].loc.x() - self.network.nodes[previous_node].loc.x()), 2) + math.pow((self.network.nodes[current_node].loc.y() - self.network.nodes[previous_node].loc.y()), 2))    )
            distance = distance * 100
            path_edges.append( (self.network.nodes[current_node].loc, self.network.nodes[previous_node].loc, '{:.0f}'.format(distance)))
            total_length += distance
            current_node = previous_node
            previous_node = self.prev[current_node]
        # if total_length == 0:
        #     total_length = float('inf')
        return {'cost':total_length, 'path':path_edges}

    

    def dijkstra_array(self, srcIndex):
        dist = [float('inf')] * len(self.network.nodes)                                             # O( |V| )
        prev = [None] * len(self.network.nodes)                                                     # O( |V| )
        dist[srcIndex] = 0
        array_priority_queue = Array_Priority_Queue()
        array_priority_queue.make_queue(self.network.nodes, dist)                                   # O( |V| )
        while len(array_priority_queue.q_array) > 0:                                                # O( |V| )
            u = self.network.nodes[int(array_priority_queue.delete_min())]                          # O(1)
            for edge in u.neighbors:                                                                # O(1)
                if dist[u.node_id] + edge.length < dist[edge.dest.node_id]:                         # O(1)
                    dist[edge.dest.node_id] = dist[u.node_id] + edge.length
                    prev[edge.dest.node_id] = u.node_id                                             # O(1)
                    array_priority_queue.decrease_key(edge.dest.node_id, dist[edge.dest.node_id])
        return dist, prev

    def dijkstra_heap(self, srcIndex):
        dist = [float('inf')] * len(self.network.nodes)
        prev = [None] * len(self.network.nodes)
        dist[srcIndex] = 0
        heap_priority_queue = Heap_Priority_Queue()
        heap_priority_queue.make_queue(self.network.nodes, dist) 
        while len(heap_priority_queue.q_heap_array) > 0:
            u = self.network.nodes[int(heap_priority_queue.delete_min(dist))]
            for edge in u.neighbors:
                if dist[u.node_id] + edge.length < dist[edge.dest.node_id]:
                    dist[edge.dest.node_id] = dist[u.node_id] + edge.length
                    prev[edge.dest.node_id] = u.node_id
                    if heap_priority_queue.q_pointer_array[edge.dest.node_id] != None and len(heap_priority_queue.q_heap_array) > heap_priority_queue.q_pointer_array[edge.dest.node_id]:
                        heap_priority_queue.bubble_up(heap_priority_queue.q_pointer_array[edge.dest.node_id], dist)
                        
        return dist, prev

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        if use_heap == True:
            dist, prev = self.dijkstra_heap(srcIndex)
            self.dist = dist
            self.prev = prev
            # print("PRE & DIST")
            # print(prev)
            # print(dist)
            # print()
            # print()
            # print(self.network.nodes)
        else:
            dist, prev = self.dijkstra_array(srcIndex)
            self.dist = dist
            self.prev = prev



        t2 = time.time()
        return (t2-t1)


print("HEllo")
nodes = [0, 1, 2, 3, 4, 5]
dist = [100, 99, 101, 98, 102, 103]
heap_queue = Heap_Priority_Queue()
heap_queue.make_queue(nodes, dist)
print(heap_queue.q_heap_array)
print(dist[heap_queue.q_heap_array[0]])
