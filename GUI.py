class GUI:
    def displayMenu(self):
        print("----------------Option Menu----------------")
        print("1. Insert a node")
        print("2. Delete min node")
        print("3. Find and decrease key")
        print("4. Search a key")
        print("5. Delete a node with a key")
        print("6. Draw the Fibonacci Heap")
        print("7. Exit")

    def getIntegerNumber(self, prompt):
        while True:
            try:
                userInput = input(prompt).strip()
                if userInput == "": 
                    # display error message
                    print("Input cannot be empty.")
                    continue
                userInput = int(userInput)
                return userInput

            except ValueError:
                print("Please enter a integer number.")
                continue
    
    def getMenuOption(self, prompt):
        while True:
            try:
                userInput = input(prompt).strip()
                if userInput == "": 
                    # display error message
                    print("Input cannot be empty.")
                    continue
                userInput = int(userInput)
                if userInput < 1 or userInput > 7:
                    print("Please enter a number between 1 and 7.")
                    continue
                return userInput

            except ValueError:
                print("Please enter a integer number.")
                continue

    def notifyIfKeyNotFound(self, node):
        if node is None:
            print("The key is not found!")
            return True
        else:
            return False

    def notifyIfKeyLessThanMin(self, key, min_key):
        if key < min_key:
            print("The key is less than the minimum key! The key is not found!")
            return True
        else:
            return False
    