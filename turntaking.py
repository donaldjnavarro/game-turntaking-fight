import cmd
# Starting Turn
turn = 1
# User's First Turn
myTurn = 5
# Enemy's First Turn
enemyTurn = 10
# Default values
# cmd = False

class prompt(cmd.Cmd):
    """
    GLOBAL PROMPT:
    - This is the primary input prompt that contains the global commands that should be available no matter where in the game the user is.
    - All of the functions in this class with "do_" prefix will be run when the user inputs their name
    - If user inputs a blank value, then the prompt does nothing and loops.
    - If another class inherits this class, then all of these functions will be available in their prompt, in addition to any functions within the child class.
    """
 
    prompt  = '\n: '

    def do_quit(self, arg):
        """Close the program. Nothing is saved."""
        print('QUIT SCREEN')
        quit()
        # Removing this: beware this in prompt, it only ends the current prompt and enables the user to travel backwards into previous prompts
        # return True # End the current prompt loop
    
    def emptyline(self):
        # When the user presses enter without typing anything
        # return cmd.Cmd.emptyline(self) # this will repeat the last entered command
        return False # Take no action
        
    def postcmd(self, stop, line):
        global turn, enemyTurn
        untilMyTurn = myTurn - turn
        turn = turn+1
        # print("[debug] turn:",turn)

        # Enemy acts if ready
        if (enemyTurn <= turn):
            print("Enemy acts!")
            enemyTurn = turn+10

        # # 1. Inform the user if they are ready to act
        # # 2. Inform the user how long until they will be ready to act
        if (myTurn <= turn):
            print("You are ready to act.")
        else:
            print("Preparing to act:",untilMyTurn*"...")

        return cmd.Cmd.postcmd(self, stop, line)

    def do_act(self, arg):
        global myTurn
        if (myTurn <= turn):
            print("You act!")
            myTurn = turn+10
        else:
            print("You are not ready to act yet...")

if __name__ == '__main__':
    prompt().cmdloop()
