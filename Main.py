from FibonacciHeap import FibonacciHeap as fh
from GUI import GUI



def main():
    # Create a new Fibonacci Heap
    heap = fh()
    gui = GUI()
    # heap.insert(5)
    # heap.insert(3)
    # heap.insert(8)
    # heap.insert(4)
    # heap.insert(1)
    # heap.insert(2)
    # # Remove the minimum element from the heap
    # heap.extract_min()
    print("********Welcome to the Fibonacci Heap Simulator!********")
    while True:
        # Display the menu
        gui.displayMenu()
        option = gui.getMenuOption("Enter your option: ")
        if option == 1: # Insert a node
            key = gui.getIntegerNumber("Enter the key: ")
            heap.insert(key)
        elif option == 2: # Delete min node
            if heap.min_node is None:
                print("The heap is empty!")
                continue
            min_node_extracted = heap.extract_min()
            print("The minimum node with key " + str(min_node_extracted.key) + " is deleted!")
        elif option == 3: # Find and decrease key
            if heap.min_node is None:
                print("The heap is empty!")
                continue
            key = gui.getIntegerNumber("Enter the key: ")
            if gui.notifyIfKeyLessThanMin(key, heap.min_node.key) is False:
                node = heap.find_node_with_key(key)
                if gui.notifyIfKeyNotFound(node) is False:
                    new_key = gui.getIntegerNumber("Enter the new key: ")
                    heap.decrease_key(node, new_key)
        elif option == 4: # Search a key
            if heap.min_node is None:
                print("The heap is empty!")
                continue
            key = gui.getIntegerNumber("Enter the key: ")
            if gui.notifyIfKeyLessThanMin(key, heap.min_node.key) is False:
                node = heap.find_node_with_key(key)
                if gui.notifyIfKeyNotFound(node) is False:
                    heap.closePlot()
                    heap.draw_fibonacci_heap(node)
        elif option == 5: # Delete a node with a key
            if heap.min_node is None:
                print("The heap is empty!")
                continue
            key = gui.getIntegerNumber("Enter the key: ")
            if gui.notifyIfKeyLessThanMin(key, heap.min_node.key) is False:
                node = heap.find_node_with_key(key)
                if gui.notifyIfKeyNotFound(node) is False:
                    heap.delete_node(node)
        elif option == 6: # Draw the Fibonacci Heap
            heap.closePlot()
            heap.draw_fibonacci_heap()
        elif option == 7: # Exit
            heap.closePlot()
            break



    # # Insert some elements into the heap
    # heap.insert(5)
    # heap.insert(3)
    # heap.insert(8)
    # heap.insert(4)
    # heap.insert(1)
    # heap.insert(2)
    # # Remove the minimum element from the heap
    # heap.extract_min()
    # heap.decrease_key(heap.find_node_with_key(8), 2)

    # print(heap.min_node.key)
    # # print all node in root list
    # for node in heap.iterate(heap.root_list):
        
    #     print("Root list:")
    #     print(node.key)
    #     if node.child is not None:

    #         for child in heap.iterate(node.child):
    #             print("Child list:")
    #             if child is not None:
    #                 print(child.key)
    #             else:
    #                 print("None")
    #     else:
    #         print("None")
    # # roots = []
    # # for x in heap.iterate(heap.root_list):
    # #     roots.append(x)

    # # for i, root in enumerate(roots):
    # #     print(i, root.key)
    # heap.draw_fibonacci_heap()


if __name__ == '__main__':
    main()