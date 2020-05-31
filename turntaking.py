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
        # Some gap for now to create a break between input command and any response
        print()
        print()
        print()
        return cmd.Cmd.precmd(self, line)

    def postcmd(self, stop, line):
        """All the handling for each round's resolution"""
        global now, nowTurn
        # print("[debug] nowTurn",nowTurn,", pc.turn",pc.turn,", enemy.turn",enemy.turn)
        # print("[debug] pc.stamina",pc.stamina,"enemy.stamina",enemy.stamina)
        
        print() # A single gap after the user's command is resolved
        
        # Did user win?
        if check_death():
            return True

        # Enemy takes their turn and if they aren't ready to act then they refresh
        enemy.randomact(pc)

        # Did user lose?
        if check_death():
            return True

        # Increment the current turn number
        nowTurn = nowTurn+1

        # Reset the user stance on their turn
        if (pc.myTurn()):
            pc.stance = False # Clear the stance when its your turn again. This is shortterm handling until we create a duration for stances 

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
        # print("[debug] My Stamina:",pc.stamina,"Turn:",pc.turn)
        # print("[debug] Enemy Stamina:",enemy.stamina,"Turn:",enemy.turn)
        # print("[debug] Current Turn:",nowTurn)
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
        print("\t*** You both knock each other out!!! IT'S A TIE?!! ***")
        return True

    # Did the enemy kill you?
    if pc.hp < 1:
        to_char(pc, "<--- ...you fall to the ground, DEAD! YOU LOSE")
        print()
        to_char(pc, "But I guess you get up again? Cuz we just keep fighting 'round here.")
        return True

    # Did you kill the enemy?
    if enemy.hp < 1:
        to_char(pc, "...the enemy falls to the ground, DEAD! YOU WIN")
        return True        

def to_char(char, msg, user=True):
    """Displays a message to the char, only if they are the user."""
    # Optional argument user can be turned off to print if the char arg is the enemy instead
    if not user:
        if char == enemy:
            if intuition():
                print(" "+msg)
    else:
        if char == pc:
            print(" "+msg)

def intuition():
    """Determine whether the user is able to notice something"""
    # For now we will use opposed hp checks to represent alertness and the ability to conceal yourself as influenced by health/pain
    # Note: For now we aren't passing chars into this function because the subjectivity is one way. If later we want to develop mechanics around the enemy having intuition too, then we can add char args
    if challenge(pc.hp, enemy.hp):
        return True
    else:
        # print("[debug] User was too oblivious to notice something!")
        return False

def dice(number, sides):
    """Random number generator for any number of dice of with any number of sides"""
    rolled = 0
    for x in range(number):
        rolled += random.randint(1,sides)
        # print("Rolled: ",rolled)
    return rolled

def challenge(cstat, tstat):
    """Oppose a cstat vs tstat with dice rolls, and return a number of successes based on the results"""
    # 1. Define how many sides the dice will have
    # 2. Roll a number of dice for the char and the opponent equal to the value of the stat being challenged
    # 3. For each roll above the opponent's highest, add a success
    # 5. Return the number of successes, which can be used to influence the potency of a win
    global char
    challenge_dice = 100 # number of sides for the dice used in contests
    success = 0
    cstat = int(cstat)
    tstat = int(tstat)

    # Challenger rolls
    charRoll = [0]
    for x in range(0, cstat):
        charRoll.append(dice(1,challenge_dice))
        # print("[debug] CHALLENGER ROLL:",charRoll)
    charRoll.sort()
    # char_highest = charRoll[-1] # not needed now that we only measure successes
    # print("[debug] HIGHEST ROLL: ",char_highest)

    # Opponent rolls
    targRoll = [0]
    for x in range(0, tstat):
        targRoll.append(dice(1,challenge_dice))
        # print("[debug] TARGET ROLL:",targRoll)
    targRoll.sort()
    targ_highest = targRoll[-1]
    # print("[debug] HIGHEST ROLL: ",targ_highest)

    # Check for bonus successes
    # print("[debug]",charRoll,"vs",targ_highest)
    for x in charRoll:
        if x > targ_highest:
            success = success+1
    # print("[debug] Challenge Success:",success)
    return success

class create_action(object):
    """Creates an attack."""
    def __init__(self, name, level):
        self.level = level
        self.name = name

    def attack(self, char, tchar):
        """Try to attack and if it is not blocked then return True"""
        if char.tryAct(self.level):
            char.wait(self.level)
            char.tire(self.level)

            to_char(char, "You attempt to "+self.name+"...")
            to_char(tchar, "<--- The enemy attempts to "+self.name+"...")
            # try to hit: 
            # - attacker uses their stamina plus the power of their attack
            # - defender uses their stamina minus their turn waittime which serves as a reaction penalty
            cpow = self.level
            tpow = tchar.turn-nowTurn if tchar.turn-nowTurn > 0 else 1

            attackResult = 0
            attackResult = challenge(cpow, tpow)
            if attackResult:
                tryDamage(char, tchar, attackResult)
            else: # didnt hit
                to_char(char, "...but they avoid the attack.")
                to_char(tchar, "<--- ...but you avoid the attack!")
                return False 
        else: # didnt act
            return False

def tryBlock(char, tchar, dmg):
    """Check if the char is blocking and attempt to reduce the dmg before returning it"""
    # If they aren't blocking then we're done here
    if tchar.stance != "blocking":
        return dmg

    block = 0
    block = challenge(tchar.stamina+1, dmg)

    impact = 0
    impact = dmg - block

    if block > 0:
        # Blocked some of the impact
        if impact > 0:
            to_char(tchar, "<--- ...you managed to block some of the impact.")
            to_char(char, "...they managed to block some of the impact.") if tchar is enemy else False
        # Blocked all of the impact
        else:
            to_char(tchar, "<--- ...you managed to block the attack!")
            to_char(char, "...they managed to block the attack.") if tchar is enemy else False
    # Failed to block any damage at all
    else:
        to_char(tchar, "<--- ...you try to block but are overwhelmed.")
        to_char(char, "...the enemy tries to block but you overwhelm their defense!") if tchar is enemy else False

    impact = 0 if impact < 0 else impact
    return impact

def tryDamage(char, tchar, power):
    """Deals damage to tchar. It is called within attack() so it shouldn't normally be called on its own"""
    impact = 0
    impact = challenge(power, tchar.stamina)
    impact = tryBlock(char, tchar, impact)

    # Deal damage
    if impact > 0:
        tchar.hp = tchar.hp - impact
        to_char(tchar, "<--- ...ouch! That hurt"+"!"*impact)
        to_char(char, "...that looked like it hurt"+"!"*impact) if tchar is enemy else False

        # Damaged chars drop any stances
        if tchar.stance:
            tchar.stance = False
            to_char(tchar, "<--- ...you are knocked out of your stance.")
            to_char(char, "...they are knocked out of their stance!", False)

        tryStun(tchar, impact)
    else:
        to_char(tchar, "<--- ...luckily, you barely felt that!")
        to_char(char, "...they shrug off the attack.") if tchar is enemy else False

    impact = 0 if impact < 0 else impact
    return impact

def tryStun(tchar, power):
    """Try to add wait time to the tchar, relative to power"""
    stun = tchar.wait(power)
    if stun > 0:
        to_char(tchar, "<--- ...you are stunned"+"!"*stun)
        to_char(tchar, "...they are stunned"+"!"*stun, False)

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

    def tryAct(self, cost):
        """Return True if it is self's turn and they can afford the cost"""
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
        """Applies a cooldown before the char's next action"""
        
        # Don't let them get ahead of the current round through inaction
        if self.turn < nowTurn:
            self.turn = nowTurn

        # Roll challenges to see how many additional rounds to add
        lag = 0
        for x in range(time):
            if challenge(10,self.hp):
                lag = lag+1

        self.turn = self.turn + lag
        return lag


    def tire(self, cost):
        """Reduces the char's stamina by the cost"""
        # Use challenge to randomize the actual stamina spent 
        self.stamina = self.stamina - challenge(cost, 1)

    def rest(self, filler=False):
        """Attempt to ignore wounds to recover Stamina"""
        if self.stamina < 10:
            if challenge(1, 10-self.hp): # chance to recover opposed by wounds
                to_char(self, "You bide your time and regain some energy.")
                to_char(self, "<--- The enemy breathes heavily.", False)
                self.stamina = self.stamina+1 
            else:
                to_char(self, "You try to focus, but are too disoriented.")
                to_char(self, "<--- The enemy blinks and tries to shake off the pain.", False)

    def block(self, tchar=False, level=1):
        """Assume a blocking stance"""
        if self.tryAct(level):
            to_char(self, "You get ready to defend yourself.")
            self.stance = "blocking"
            to_char(self, "<--- The enemy gets ready to defend themselves.", False)
            self.wait(level)
            self.tire(level)
            return True
        else:
            return False

    def jab(self, tchar):
        if jab.attack(self, tchar):
            return True
        else:
            return False

    def punch(self, tchar):
        if punch.attack(self, tchar):
            return True
        else:
            return False

    def uppercut(self, tchar):
        if uppercut.attack(self, tchar):
            return True
        else:
            return False

    def randomact(self, tchar):
        """Attempt to take a random action. Used to randomize enemy behavior"""
        if (self.turn < nowTurn):
            self.stance = False
            actions = [self.block, self.jab, self.punch, self.uppercut, self.rest]
            # 1. If they are under a certain stamina threshold, then just rest
            if self.stamina < 5:
                self.rest()
            # 2. If not resting, then attack
            else:
                random.choice(actions)(tchar)


if __name__ == '__main__':
    print()
    print(" "+"-"*47)
    print("| Tips:")
    print("|   Type \"help\" to see the available commands.")
    print("|   Time passes when any command is entered.")
    print(" "+"-"*47)
    play = True
    jab = create_action("jab", 2)
    punch = create_action("punch", 3)
    uppercut = create_action("uppercut", 4)
    block = create_action("block", 1)

    while play == True:
        nowTurn = 1
        pc = create_char()
        enemy = create_char()
        enemy.turn = random.randint(1,3) # Enemy's first turn is random
        print()
        to_char(pc, "An enemy approaches. Time to fight!")
        prompt().cmdloop()
