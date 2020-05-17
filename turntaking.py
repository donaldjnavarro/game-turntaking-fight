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
        pc.stamina = pc.stamina+1 if pc.stamina < 100 else 100
        return False # Do nothing and let time proceed if the user inputs enter without typing

    def postcmd(self, stop, line):
        global turn
        
        # Enemy takes their turn and if they aren't ready to act then they refresh
        if not enemy.randomact(pc):
            enemy.stamina = enemy.stamina+1 if enemy.stamina < 100 else 100

        # Check win and lose conditions
        if check_death():
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
        print("< My HP:",pc.hp,"Stamina:",pc.stamina,"|| Enemy HP:",enemy.hp,"Stamina:",enemy.stamina,">")
        return cmd.Cmd.postcmd(self, stop, line)

    def do_jab(self, arg):
        """A light punch that is weak but fast"""
        pc.jab(enemy)
    def do_punch(self, arg):
        """A medium punch, not too fast, but not too weak"""
        pc.punch(enemy)
    def do_uppercut(self, arg):
        """A powerful punch, commit to WIN!"""
        pc.uppercut(enemy)
    def do_block(self, arg):
        """Protect yourself from incoming attacks"""
        pc.block()

def check_death():
    """Check if anyone died"""
    # Did everyone die?!
    if pc.hp < 1 and enemy.hp < 1:
        print("\n\tYou both knock each other out!!!!!!!!!!! IT'S A TIE!")
        return True

    # Did the enemy kill you?
    if pc.hp < 1:
        print("\n\tYou fall to the ground, defeated!!!!!!!!!!!!!!!")
        print()
        print("But I guess you get up again? Cuz we just keep fighting 'round here.")
        return True

    # Did you kill the enemy?
    if enemy.hp < 1:
        print("\n\tThe enemy falls to the ground, defeated!!!!!!!!!!!!!!!")
        return True        

def to_char(char, msg):
    """Displays a message to the char, only if they are the user"""
    if char == pc:
        print(msg)

class create_char(object):
    """Creates a character: a player or npc."""
    def __init__(self):
        self.hp = 20
        self.stamina = 100
        self.stance = False
        self.turn = 0

    def try_act(self, cost):
        """Try to take an action and return True if it is your turn"""
        global turn
        if (self.turn < turn):
            if self.stamina > cost:
                return True
            else:
                to_char(self, "You are too tired to do that...")
                return False
        else:
            to_char(self, "You are not ready to act yet...")
            return False

    def attack(self, tchar, cost):
        """Try to attack and if it is not blocked then return True"""
        if self.try_act(cost):
            self.turn = turn+cost
            self.stamina = self.stamina - cost
            if tchar.stance == "blocking":
                to_char(tchar, "You block the enemy's attack")
                to_char(pc, "The enemy blocks your attack") if tchar is enemy else False
                return False
            else:
                return True

    def jab(self, tchar):
        if self.attack(tchar, 5):
            to_char(self, "You throw a jab!")
            to_char(tchar, "The enemy throws a jab!")
            tchar.hp = tchar.hp - 5

    def punch(self, tchar):
        if self.attack(tchar, 10):
            to_char(self, "You throw a punch!")
            to_char(tchar, "The enemy throws a punch!")
            tchar.hp = tchar.hp - 10

    def uppercut(self, tchar):
        if self.attack(tchar, 15):
            to_char(self, "You throw a uppercut!")
            to_char(tchar, "The enemy throws a uppercut!")
            tchar.hp = tchar.hp - 15

    def block(self, tchar=False):
        cost = 5
        if self.try_act(cost):
            to_char(self, "You get ready to defend yourself.")
            self.stance = "blocking"
            print("The enemy gets ready to defend themselves.") if self is enemy else False
            self.turn = turn+cost

    def randomact(self, tchar):
        """Attempt to take a random action"""
        if (self.turn < turn): 
            self.stance = False
            actions = [self.block, self.jab, self.punch, self.uppercut]
            random.choice(actions)(tchar)
            return True
            
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
        enemy.turn = 3 # arbitrary offset so we start by alternating turns
        print()
        print("An enemy approaches. Time to fight!")
        prompt().cmdloop()
