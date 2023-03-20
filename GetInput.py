class GetInput:
    def getIntegerNumber(self, prompt):
        while True:
            try:
                userInput = input(prompt)
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
                userInput = input(prompt)
                if userInput == "": 
                    # display error message
                    print("Input cannot be empty.")
                    continue
                userInput = int(userInput)
                if userInput < 1 or userInput > 6:
                    print("Please enter a number between 1 and 6.")
                    continue
                return userInput

            except ValueError:
                print("Please enter a integer number.")
                continue