import math
import networkx as nx
import matplotlib.pyplot as plt
import sys


class FibonacciHeap:

    # internal node class
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.parent = self.child = self.left = self.right = None
            self.degree = 0
            self.mark = False

    # function to iterate through a doubly linked list

    def iterate(self, head):
        if head is None:
            return
        node = stop = head
        flag = False
        while True:
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right

    # pointer to the head and minimum node in the root list
    root_list, min_node = None, None

    # maintain total node count in full fibonacci heap
    total_nodes = 0

    # insert new node into the unordered root list in O(1) time
    # returns the node so that it can be used for decrease_key later
    def insert(self, key, value=None):
        if key is None:
            return None
        n = self.Node(key, value)
        n.left = n.right = n
        self.merge_with_root_list(n)
        if self.min_node is None or n.key < self.min_node.key:
            self.min_node = n
        self.total_nodes += 1
        return n
    
    


    # merge two fibonacci heaps in O(1) time by concatenating the root lists
    # the root of the new root list becomes equal to the first list and the second
    # list is simply appended to the end (then the proper min node is determined)
    def merge(self, h2):
        H = FibonacciHeap()
        H.root_list, H.min_node = self.root_list, self.min_node
        # fix pointers when merging the two heaps
        last = h2.root_list.left
        h2.root_list.left = H.root_list.left
        H.root_list.left.right = h2.root_list
        H.root_list.left = last
        H.root_list.left.right = H.root_list
        # update min node if needed
        if h2.min_node.key < H.min_node.key:
            H.min_node = h2.min_node
        # update total nodes
        H.total_nodes = self.total_nodes + h2.total_nodes
        return H


    # return min node in O(1) time
    def find_min(self):
        return self.min_node

    # extract (delete) the min node from the heap in O(log n) time
    def extract_min(self):
        z = self.min_node
        if z is not None:
            if z.child is not None:
                # attach child nodes to root list
                children = [x for x in self.iterate(z.child)]
                for i in range(0, len(children)):
                    self.merge_with_root_list(children[i])
                    children[i].parent = None
            self.remove_from_root_list(z)
            # set new min node in heap
            if z == z.right:
                self.min_node = self.root_list = None
            else:
                self.min_node = z.right
                self.consolidate()
            self.total_nodes -= 1
        return z

    def consolidate(self):
        # Create an array A of size log_phi(n), where n is the total number of nodes in the heap,
        # to store nodes of different degrees during consolidation. Here, we use an upper bound
        # of log_2(n) * 2, which is a more efficient implementation.
        A = [None] * int(math.log(self.total_nodes, 2) * 2)
        nodes = [w for w in self.iterate(self.root_list)]
        for w in range(0, len(nodes)):
            x = nodes[w]
            d = x.degree
            while A[d] != None:
                y = A[d]
                if x.key > y.key:
                    temp = x
                    x, y = y, temp
                self.heap_link(y, x)
                A[d] = None
                d += 1
            A[d] = x
        # find new min node - no need to reconstruct new root list below
        # because root list was iteratively changing as we were moving
        # nodes around in the above loop
        for i in range(0, len(A)):
            if A[i] is not None:
                if A[i].key <= self.min_node.key:
                    self.min_node = A[i]
    
    # actual linking of one node to another in the root list
    # while also updating the child linked list
    def heap_link(self, y, x):
        self.remove_from_root_list(y)
        y.left = y.right = y
        self.merge_with_child_list(x, y)
        x.degree += 1
        y.parent = x
        y.mark = False
    

    def find_node_with_key(self, key):
        if key is None or key < self.min_node.key:
            return
        """
        Searches the heap for a node with the given key and returns the node if found.
        """
        # Define a recursive helper function to search for the node with the given key
        def find_node_with_key_helper(node):
            # Base case: if the current node is None, we didn't find the key
            if node is None:
                return None
            # If we found the node with the key, return it
            if node.key == key:
                return node
            # Recursively search the current node's children for the key
            if node.child is not None:
                for child in self.iterate(node.child):
                    result = find_node_with_key_helper(child)
                    # If we found the node with the key in the child's subtree, return it
                    if result is not None:
                        return result
            # If we reach this point, the node wasn't found in the current node's subtree, so return None
            return None

        for node in self.iterate(self.root_list):
            result = find_node_with_key_helper(node)
            # If we found the node with the key in the root list, return it
            if result is not None:
                return result
        # If we reach this point, the key wasn't found in the heap, so return None
        return None

    def delete_node(self, node):
        if node is None:
            return
        self.decrease_key(node, -sys.maxsize - 1)
        self.extract_min()

    # modify the key of some node in the heap in O(1) time
    def decrease_key(self, x, k):
        if x is None or k > x.key:
            return None
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self.cut(x, y)
            self.cascading_cut(y)
        if x.key < self.min_node.key:
            self.min_node = x

   
    # if a child node becomes smaller than its parent node we
    # cut this child node off and bring it up to the root list
    def cut(self, x, y):
        self.remove_from_child_list(y, x)
        y.degree -= 1
        self.merge_with_root_list(x)
        x.parent = None
        x.mark = False

    # cascading cut of parent node to obtain good time bounds
    def cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if y.mark is False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    # merge a node with the doubly linked root list
    def merge_with_root_list(self, node):
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node

    # merge a node with the doubly linked child list of a root node
    def merge_with_child_list(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    # remove a node from the doubly linked root list
    def remove_from_root_list(self, node):
        if node == self.root_list:
            self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left

    # remove a node from the doubly linked child list
    def remove_from_child_list(self, parent, node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left

    def draw_fibonacci_heap(self, nodeFound=None):
        if (self.total_nodes == 0):
            print("The heap is empty")
            return
        G = nx.Graph()
        pos = {}
        labels = {}
        color = []
        color_map = {}
        x = y = 0
        # Iterate through all roots and draw them in a line

        def draw_fibonacci_heap_helper(node, parent=None, nodeFound=None):
            if node is None:
                return
            nonlocal x
            nonlocal y
            pos[node] = (x, y)
            G.add_node(node)
            if node == nodeFound:
                labels[node] = (node.key, 'found')
                color_map[node] = 'purple'
            elif node == self.min_node:
                labels[node] = (node.key, 'min')
                color_map[node] = 'red'
            elif node.parent is None:
                labels[node] = node.key
                color_map[node] = 'green'
            elif node.mark is True:
                labels[node] = (node.key, 'marked')
                color_map[node] = 'blue'
            else:
                labels[node] = node.key
                color_map[node] = 'black'

            if node.child is not None:
                for child in self.iterate(node.child):
                    y -= 1
                    draw_fibonacci_heap_helper(child, node, nodeFound)
                    y += 1
            else:
                x += 1
            if parent is not None:
                G.add_edge(parent, node)
            else:
                if node.right is not None and node.right != node:
                    G.add_edge(node, node.right)
           
            return
        for node in self.iterate(self.root_list):
            draw_fibonacci_heap_helper(node, None, nodeFound)
        # print(color)
        # for key,value in pos.items():
        #     print(key.key)
        color = [color_map.get(node) for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, labels=labels, node_color=color, font_size=6,
                node_size=2000, font_color='white', font_weight='bold')
        plt.show(block=False)

    def closePlot(self):
        plt.close('all')
