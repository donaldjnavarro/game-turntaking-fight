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
        global turn
        #----------------------
        # Enemy acts if ready
        if (enemy.turn < turn): 
            enemy.stance = False
            enemyActions = [block, jab, punch, uppercut]
            random.choice(enemyActions)("enemy", "user")

        # Did enemy kill the user?
        if (pc.hp < 1):
            print("\n\tYou fall to the ground, defeated!!!!!!!!!!!!!!!")
            print()
            print("But I guess you get up again? Cuz we just keep fighting 'round here.")
            return True
        #-----------------------
        # End of Round Routine
        turn = turn+1
        # 1. Inform the user if they are ready to act
        # 2. Inform the user how long until they will be ready to act
        if (pc.turn < turn):
            print("...you are ready to act.")
            pc.stance = False # Clear the stance when its your turn again. This is shortterm handling until we create a duration for stances 
        else:
            print("Preparing to act:",(pc.turn - turn)*".")
        print("< My HP:",pc.hp,"|| Enemy HP:",enemy.hp,">")

        # Did you kill the enemy?
        if (enemy.hp < 1):
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
    if char == "user":
        if (pc.turn < turn):
            return True
        else:
            print("You are not ready to act yet...")
            return False
    if char == "enemy":
        if (enemy.turn < turn):
            return True
        else:
            return False

def wait(char, time):
    global turn
    if char == "user":
        pc.turn = turn+time
    if char == "enemy":
        enemy.turn = turn+time

def attack(target, damage):
    if target == "enemy":
        if enemy.stance == "blocking":
            print("The enemy blocks your attack!")
            return False
        else:
            enemy.hp = enemy.hp - damage
            return True
    if target == "user":
        if pc.stance == "blocking":
            print("You block the enemy's attack!")
            return False
        else:
            pc.hp = pc.hp - damage
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
    if try_act(char):
        if char == "user":
            print("You get ready to defend yourself.")
            pc.stance = "blocking"
        if char == "enemy":
            enemy.stance = "blocking"
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

class create_char(object):
    """Creates a character: a player or npc."""
    def __init__(self):
        self.hp = 100
        self.stamina = 100
        self.stance = False
        self.turn = 1

if __name__ == '__main__':
    print()
    print("Tips:")
    print("- Type \"help\" to see the available commands.")
    print("- Time passes when any command is entered.")
    play = True
    while play == True:
        turn = 1
        pc = create_char()
        enemy = create_char()
        enemy.turn = 5 # arbitrary offset so we start by alternating turns
        print()
        print("An enemy approaches. Time to fight!")
        prompt().cmdloop()
