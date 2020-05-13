import cmd
import random

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
        global turn, enemyTurn, myStance
        untilMyTurn = myTurn - turn

        print("[debug] enemyTurn:",enemyTurn)
        #----------------------
        # Enemy acts if ready
        if (enemyTurn < turn): 
            enemyActions = [block, jab, punch, uppercut]
            random.choice(enemyActions)("enemy", "user")

        # Did enemy kill the user?
        if (myHp < 1):
            print("\n\tYou fall to the ground, defeated!!!!!!!!!!!!!!!")
            print()
            print("But I guess you get up again? Cuz we just keep fighting 'round here.")
            return True
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

        # Did you kill the enemy?
        if (enemyHp < 1):
            print("\n\tThe enemy falls to the ground, defeated!!!!!!!!!!!!!!!")
            return True
        return cmd.Cmd.postcmd(self, stop, line)

    def do_jab(self, arg):
        """A light punch that is weak but fast"""
        jab("user", "enemy")
    def do_punch(self, arg):
        """A medium punch, not too fast, but not too weak"""
        punch("user", "enemy")
    def do_uppercut(self, arg):
        """A powerful punch, commit to WIN!"""
        uppercut("user", "enemy")
    def do_block(self, arg):
        """Protect yourself from incoming attacks"""
        block("user", "enemy")

def try_act(char):
    global myTurn

    if char == "user":
        if (myTurn < turn):
            return True
        else:
            print("You are not ready to act yet...")
            return False
    if char == "enemy":
        if (enemyTurn < turn):
            return True
        else:
            return False

def wait(char, time):
    global myTurn, turn, enemyTurn
    if char == "user":
        myTurn = turn+time
    if char == "enemy":
        enemyTurn = turn+time

def attack(target, damage):
    global enemyHp, myHp
    if target == "enemy":
        if enemyStance == "blocking":
            print("The enemy blocks your attack!")
            return False
        else:
            enemyHp = enemyHp - damage
            return True
    if target == "user":
        if myStance == "blocking":
            print("You block the enemy's attack!")
            return False
        else:
            myHp = myHp - damage
            return True

def jab(char, tchar):
    if try_act(char):
            if char == "user":
                print("You throw a jab!")
            if char == "enemy":
                print("The enemy throws a jab!")
            attack(tchar, 5)
            wait(char, 5)

def punch(char, tchar):
    if try_act(char):
            if char == "user":
                print("You throw a punch!")
            if char == "enemy":
                print("The enemy throws a punch!")
            attack(tchar, 10)
            wait(char, 10)

def block(char, tchar):
    global stance
    if try_act(char):
        if char == "user":
            print("You get ready to defend yourself")
            myStance = "blocking"
        if char == "enemy":
            enemyStance = "blocking"
            if random.randint(0,1): # Replace this with a dynamic mechanic that determines whether you notice them preparing a defense
                print("The enemy gets ready to defend themselves.")
        wait(char, 5)

def uppercut(char, tchar):
    if try_act(char):
            if char == "user":
                print("You throw an uppercut!")
            if char == "enemy":
                print("The enemy throws an uppercut!")
            attack(tchar, 15)
            wait(char, 15)

if __name__ == '__main__':
    print()
    print("Tips:")
    print("- Type \"help\" to see the available commands")
    print("- Time passes when any command is entered.")
    play = True
    while play == True:
        turn = 1
        myTurn = 5
        enemyTurn = 10
        myHp = 10
        enemyHp = 10
        myStance = False
        enemyStance = False
        print()
        print("An enemy approaches. Time to fight!")
        prompt().cmdloop()
