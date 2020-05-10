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
        global turn, enemyTurn, stance
        untilMyTurn = myTurn - turn

        # Enemy acts if ready
        if (enemyTurn <= turn):
            if stance == "blocking":
                print("You block the enemy's attack!!!")
            else:
                print("Enemy acts!")
            enemyTurn = turn+10
        # 1. Inform the user if they are ready to act
        # 2. Inform the user how long until they will be ready to act
        if (myTurn <= turn):
            print("You are ready to act.")
            stance = False # Clear the stance when its your turn again. This is shortterm handling until we create a duration for stances 
        else:
            print("Preparing to act:",untilMyTurn*".")
        turn = turn+1
        return cmd.Cmd.postcmd(self, stop, line)

    def do_act(self, arg):
        if try_act():
            print("You act!")
            wait(10)
    def do_jab(self, arg):
        if try_act():
            print("You throw a light jab!")
            wait(5)
    def do_punch(self, arg):
        if try_act():
            print("You throw a punch!")
            wait(10)
    def do_uppercut(self, arg):
        if try_act():
            print("You throw a fierce uppercut!")
            wait(15)
    def do_block(self, arg):
        global stance
        if try_act():
            print("You prepare for incoming attacks!")
            stance = "blocking"
            wait(5)

def try_act():
    global myTurn
    if (myTurn <= turn):
        return True
    else:
        print("You are not ready to act yet...")
        return False

def wait(time):
    global myTurn, turn
    myTurn = turn+time

if __name__ == '__main__':
    prompt().cmdloop()
