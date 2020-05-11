import cmd
turn = 1
myTurn = 5
enemyTurn = 10
myHp = 100
enemyHp = 100
stance = False

class prompt(cmd.Cmd):
    """
    GLOBAL PROMPT:
    - This is the primary input prompt that contains the global commands that should be available no matter where in the game the user is.
    - All of the functions in this class with "do_" prefix will be run when the user inputs their name
    - If user inputs a blank value, then the prompt does nothing and loops.
    - If another class inherits this class, then all of these functions will be available in their prompt, in addition to any functions within the child class.
    """

    prompt = ": "

    def do_quit(self, arg):
        """Close the program. Nothing is saved."""
        quit()
    
    def emptyline(self):
        # return cmd.Cmd.emptyline(self) # this will repeat the last entered command
        return False # Do nothing and let time proceed if the user inputs enter without typing

    def postcmd(self, stop, line):
        global turn, enemyTurn, stance
        untilMyTurn = myTurn - turn
        #----------------------
        # Enemy acts if ready
        if (enemyTurn < turn):
            if stance == "blocking":
                print("You block the enemy's attack!!!")
            else:
                print("The enemy punches you!")
                attack("user", 10)
            enemyTurn = turn+10
        #-----------------------
        # End of Round Routine
        turn = turn+1
        # 1. Inform the user if they are ready to act
        # 2. Inform the user how long until they will be ready to act
        if (myTurn < turn):
            print("...you are ready to act.")
            stance = False # Clear the stance when its your turn again. This is shortterm handling until we create a duration for stances 
        else:
            print("Preparing to act:",untilMyTurn*".")
        print("< My HP:",myHp,"|| Enemy HP:",enemyHp,">")
        return cmd.Cmd.postcmd(self, stop, line)

    def do_jab(self, arg):
        if try_act():
            print("You throw a light jab!")
            attack("enemy", 5)
            wait(5)
    def do_punch(self, arg):
        if try_act():
            print("You throw a punch!")
            attack("enemy", 10)
            wait(10)
    def do_uppercut(self, arg):
        if try_act():
            print("You throw a fierce uppercut!")
            attack("enemy", 15)
            wait(15)
    def do_block(self, arg):
        global stance
        if try_act():
            print("You prepare for incoming attacks!")
            stance = "blocking"
            wait(5)

def try_act():
    global myTurn
    if (myTurn < turn):
        return True
    else:
        print("You are not ready to act yet...")
        return False

def wait(time):
    global myTurn, turn
    myTurn = turn+time

def attack(target, damage):
    global enemyHp, myHp
    if target == "enemy":
        enemyHp = enemyHp - damage
    if target == "user":
        myHp = myHp - damage

if __name__ == '__main__':
    prompt().cmdloop()

####### TODO LIST
# TODO: Using HELP should not increment time
# TODO: Vary enemy actions
# TODO: Vary the amount of damage done
# TODO: Vary success rate of attacks
# TODO: Add death handling / win-lose scenarios