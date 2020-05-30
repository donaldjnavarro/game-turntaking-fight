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
        pc.rest()
        return False # Do nothing and let time proceed if the user inputs enter without typing

    def precmd(self, line):
        print()
        print()
        print()
        return cmd.Cmd.precmd(self, line)

    def postcmd(self, stop, line):
        global now, nowTurn
        # print("[debug] nowTurn",nowTurn,", pc.turn",pc.turn,", enemy.turn",enemy.turn)
        # print("[debug] pc.stamina",pc.stamina,"enemy.stamina",enemy.stamina)
        print()
        
        # Did user win?
        if check_death():
            return True

        # Enemy takes their turn and if they aren't ready to act then they refresh
        if not enemy.randomact(pc):
            enemy.rest()

        # Did user lose?
        if check_death():
            return True

        #-----------------------
        # End of Round Routine
        nowTurn = nowTurn+1
        # 1. Inform the user if they are ready to act
        # 2. Inform the user how long until they will be ready to act
        if (pc.myTurn()):
            status = "and ready to act!"
            pc.stance = False # Clear the stance when its your turn again. This is shortterm handling until we create a duration for stances 
        else:
            status = "and preparing to act."+(pc.turn - nowTurn)*"."
            if pc.stance: 
                status = "and "+pc.stance+" "+status
        
        # global tempPromptLength
        # myTempPrompt = "| You are "+pc.checkhp()+" and "+pc.checkstamina()+" "+status
        # enemyTempPrompt = "| Your opponent is "+enemy.checkhp()+" and "+enemy.checkstamina()
        # tempPromptLength = len(myTempPrompt) if (len(myTempPrompt) > len(enemyTempPrompt)) else len(enemyTempPrompt)
        # print(" "+"-"*tempPromptLength)
        # print(myTempPrompt)
        # print(enemyTempPrompt)
        # print(" "+"-"*tempPromptLength)

        # newprompt
        linebreak = 31
        print(" "+"-"*linebreak)
        print("| Health  | "+"> "*int(pc.hp))
        print("| Stamina | "+"< "*int(pc.stamina))
        stanceDisplay = "fighting" if pc.stance == False else pc.stance
        print("| Stance  | "+stanceDisplay.title())
        waiting = "READY" if pc.myTurn() else ((pc.turn - nowTurn+1)*".")
        print("| Waiting | "+waiting)
        print(" "+"-"*linebreak)
        print("| Enemy   | "+"> "*int(enemy.hp))
        print(" "+"-"*linebreak)
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
    """Check if anyone died. If this returns true then we need to exit the game loop"""
    # Did everyone die?!
    if pc.hp < 1 and enemy.hp < 1:
        print("\tYou both knock each other out!!!!!!!!!!! IT'S A TIE!")
        return True

    # Did the enemy kill you?
    if pc.hp < 1:
        print("\tYou fall to the ground, defeated!!!!!!!!!!!!!!!")
        print()
        print("But I guess you get up again? Cuz we just keep fighting 'round here.")
        return True

    # Did you kill the enemy?
    if enemy.hp < 1:
        print("\tThe enemy falls to the ground, defeated!!!!!!!!!!!!!!!")
        return True        

def to_char(char, msg):
    """Displays a message to the char, only if they are the user."""
    if char == pc:
        print(" "+msg)

def dice(number, sides):
    """Random number generator for any number of dice of with any number of sides"""
    rolled = 0
    for x in range(number):
        rolled += random.randint(1,sides)
        # print("Rolled: ",rolled)
    return rolled

def challenge(cstat, tstat):
    """Handle all conflicts and resolve them with dice rolls"""
    # 1. Define how many sides the dice will have
    # 2. Roll a number of dice for the char and the opponent equal to the value of the stat being challenged
    # 3. Take the highest roll from the char and the opponent and compare them, the highest wins
    # 4. return true if the player wins, return false if the player loses, return nothing if it is a tie
    global char
    combat_dice = 100
    highest_roll = 0

    cstat = int(cstat)
    tstat = int(tstat)
    for x in range(0, cstat):
        roll = dice(1,combat_dice)
        # print("[debug] ATTACKER ROLL",roll)
        if roll > highest_roll:
            highest_roll = roll
    char_roll = highest_roll

    highest_roll = 0
    for x in range(0, tstat):
        roll = dice(1,combat_dice)
        # print("[debug] TARGET ROLL",roll)
        if roll > highest_roll:
            highest_roll = roll
    enemy_roll = highest_roll

    if char_roll > enemy_roll:
        return True
    elif enemy_roll > char_roll:
        return False

class create_attack(object):
    """Creates an attack."""
    def __init__(self, name, level):
        self.time =  level
        self.energy = level
        self.dmg = level
        self.name = name

    def attack(self, char, tchar):
        """Try to attack and if it is not blocked then return True"""
        if char.try_act(self.energy):
            char.wait(self.time)
            char.tire(self.energy)

            to_char(char, "You attempt to "+self.name+"...")
            to_char(tchar, " <--- The enemy attempts to "+self.name+"...")
            # try to hit
            cpow = char.stamina+self.energy
            tpow = tchar.stamina
            # print("[debug]",cpow,"vs",tpow)
            if challenge(cpow, tpow):
                # if hit succeeded
                if blocked(self, char, tchar) is not True:
                    to_char(char, "...the "+self.name+" hits!")
                    to_char(tchar, " <--- the "+self.name+" hits you!\n")
                    damage(tchar, self.dmg)
                    return True
                else:
                    return False
            else:
                to_char(char, "...but they avoid the "+self.name+".")
                to_char(tchar, " <--- but you avoid the "+self.name+".")
                return False
        else:
            return False

def blocked(attack, char, tchar):
    """Check whether an attack is blocked based on an opposed challenge"""
    if tchar.stance == "blocking":
        power = char.stamina + attack.energy
        if challenge(tchar.stamina+1, power):
            # +1 is currently representing the Energy cost of Block
            to_char(tchar, " <--- you block the enemy's attack.")
            to_char(pc, "the enemy blocks your attack.") if tchar is enemy else False
            return True
        else:
            to_char(tchar, " <--- you try to block but are overwhelmed...")
            to_char(pc, "the enemy tries to block but you overwhelm their defense...") if tchar is enemy else False
            return False
    else:
        return False

def damage(tchar, dmg):
    """Deals damage to tchar. It is called within attack() so it shouldn't normally be called on its own"""
    tchar.hp = tchar.hp - dmg

class create_char(object):
    """Creates a character: a player or npc"""
    def __init__(self):
        self.hp = 10
        self.stamina = 10
        self.stance = False
        self.turn = 0

    def myTurn(self):
        """Check if it is the character's turn now"""
        global nowTurn
        if (self.turn < nowTurn):
            return True
        else:
            return False

    def try_act(self, cost):
        """Try to take an action and return True if it is your turn"""
        global nowTurn
        if self.myTurn():
            if self.stamina >= cost:
                return True
            else:
                to_char(self, "You are too tired to do that...")
                return False
        else:
            to_char(self, "You are not ready to act yet...")
            return False

    def wait(self, time):
        """Applies a cooldown until the char's next action"""
        self.turn = nowTurn + time

    def tire(self, cost):
        """Reduces the char's stamina by the cost"""
        self.stamina = self.stamina - cost

    def rest(self):
        """Attempt to ignore wounds to recover Stamina"""
        if self.stamina < 10:
            if challenge(self.hp, 1): # recover chance based on lack of wounds
                to_char(self, "You bide your time and regain some energy.")
                self.stamina = self.stamina+1 
            else:
                to_char(self, "You try to focus, but are too disoriented.")

    def block(self, tchar=False):
        """Assume a blocking stance"""
        energy = 1
        if self.try_act(energy):
            to_char(self, "You get ready to defend yourself.")
            self.stance = "blocking"
            print("<- The enemy gets ready to defend themselves.") if self is enemy else False
            self.wait(energy)
            self.tire(energy)

    def jab(self, tchar):
        jab.attack(self, tchar)

    def punch(self, tchar):
        punch.attack(self, tchar)

    def uppercut(self, tchar):
        uppercut.attack(self, tchar)

    def randomact(self, tchar):
        """Attempt to take a random action. Used to randomize enemy behavior"""
        if (self.turn < nowTurn): 
            self.stance = False
            actions = [self.block, self.jab, self.punch, self.uppercut]
            random.choice(actions)(tchar)
            return True

if __name__ == '__main__':
    print()
    print(" "+"-"*47)
    print("| Tips:")
    print("|   Type \"help\" to see the available commands.")
    print("|   Time passes when any command is entered.")
    print(" "+"-"*47)
    play = True
    jab = create_attack("jab", 1)
    punch = create_attack("punch", 2)
    uppercut = create_attack("uppercut", 3)

    while play == True:
        nowTurn = 1
        pc = create_char()
        enemy = create_char()
        enemy.turn = random.randint(1,3) # Enemy's first turn is random
        print()
        print("An enemy approaches. Time to fight!")
        prompt().cmdloop()
