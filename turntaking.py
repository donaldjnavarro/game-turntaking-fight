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
            random.choice(enemyActions)(enemy, pc)

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
        jab(pc, enemy)
    def do_punch(self, arg):
        """A medium punch, not too fast, but not too weak"""
        punch(pc, enemy)
    def do_uppercut(self, arg):
        """A powerful punch, commit to WIN!"""
        uppercut(pc, enemy)
    def do_block(self, arg):
        """Protect yourself from incoming attacks"""
        block(pc, enemy)

def attack(target, damage):
    if target.stance == "blocking":
        to_char(target, "You block the enemy's attack")
        to_char(pc, "The enemy blocks your attack") if target is enemy else False
        # if target == pc:
        #     print("You block the enemy's attack!")
        #     return False
        # if target == enemy:
        #     print("The enemy blocks your attack!")
        #     return False
    else:
        target.hp = target.hp - damage
        return True

def jab(char, tchar):
    if char.try_act():
        to_char(char, "You throw a jab!")
        to_char(tchar, "The enemy throws a jab!")
        attack(tchar, 5)
        char.turn = turn+5

def punch(char, tchar):
    if char.try_act():
        to_char(char, "You throw a punch!")
        to_char(tchar, "The enemy throws a punch!")
        attack(tchar, 10)
        char.turn = turn+10

def block(char, tchar):
    if char.try_act():
        if char == pc:
            print("You get ready to defend yourself.")
            pc.stance = "blocking"
        if char == enemy:
            enemy.stance = "blocking"
            if random.randint(0,1): # Replace this with a dynamic mechanic that determines whether you notice them preparing a defense
                print("The enemy gets ready to defend themselves.")
        char.turn = turn+5

def uppercut(char, tchar):
    if char.try_act():
        to_char(char, "You throw a uppercut!")
        to_char(tchar, "The enemy throws a uppercut!")
        attack(tchar, 15)
        char.turn = turn+15

def to_char(char, msg):
    """Displays a message to the character, only if they are the user"""
    if char == pc:
        print(msg)

class create_char(object):
    """Creates a character: a player or npc."""
    def __init__(self):
        self.hp = 100
        self.stamina = 100
        self.stance = False
        self.turn = 1

    def try_act(self):
        global turn
        if (self.turn < turn):
            return True
        else:
            to_char(self, "You are not ready to act yet...")
            return False

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
