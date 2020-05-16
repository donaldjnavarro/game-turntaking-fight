# Initial Concept
By creating cooldowns on a player's ability to have their turn, we can create diversity to the speed of actions a player can take: Should they take quick/weak actions, or commit to a more significant action that will afford their opponent a longer window to react.

## Features
---------------------
### Action Cooldowns
- Each action has its own length of time until the actor can take another action

### Time Visibility
- My Speed: The user can see how long until their next action
- Enemy Speed: The user gets semi-reliable view into how long until their opponent's next action

### Vigor
- Uses:
  - Action Cost: Actions have a Vigor cost in addition to a Time Requirement
  - Opposed Challenges: To determine who wins physical contests, ie if your attack hits or not, or perhaps how much it damages
- Max Vigor: Each actor has a personal max
- Refreshing Vigor: Vigor is replenished each tick, so if you don't spend much vigor with your action then you will "rest" with a net gain
  - Refreshing on individual ticks also means that there may be reasons to wait even when you can act, which feels more organic

#### Damaging Vigor
- Actions that damage your opponent's Vigor are a good way to "wear your opponent down" before a decisive action

### Rushed Actions
- A use can spend extra Vigor to reduce the cooldown on an Action

### Blocks and Preparations
- Some actions may be designed to enhance your own stats for a short period, or against certain types of actions from your opponent
- Gameplay: Timing the usage of defensive skills before an attack 

### Stuns
- Temporarily unable to use Actions with a Vigor Cost

### Feints
- Enemy can use an action to send a fake attack message that actually begins a defensive stance for a short duration
- ? This would require introducing misses else the user can see the attack did no damage?
  - OR are feints best used against opponents who are blocking? and/or fake-blocking as a feint?
- Why not feint all the time? Needs a high Vigor cost?

## Example Code
// time: how long after this action until you can act again
// cost: how much Vigor this action spends
var action = {
  "block":  {"time":  1, "cost": -1, "effect": "defense"},
  "jab":    {"time":  1, "cost":  0, "effect": "damage"},
  "punch":  {"time":  2, "cost":  1, "effect": "damage"}
}
--------------------

# Questions
- Is Vigor also HP or do these need to be separate metrics?
- Should the damage inflicted by an action be assigned to the action? Or should it be based on the Vigor cost alone?
  - Should the user be able to increase the Vigor cost of any action and thereby emphasize the damage it can do?
    - Should this be the default way costs of actions are determined? Modular actions? EX: <light> <punch> ? Or should there be preparation actions "prepare strength" that increase the next action's power?
      - Preparation actions could have a "chance to display" that determines whether the opponent gets a message showing that you are using a preparation. This chance to display could introduce a subset of learnable skills for feinting and for avoiding telegraphing
  - Should a similar system be used to measure the effects of defenses? Should defenses reduce incoming damage by the Time spent? Or should a user have an option to spend Vigor on a defense to enhance it?
- Should actors receive Vigor every time increment? And acting has a "net cost" to reduce Vigor, but if both actors commit to actions without fueling them with Vigor, then they can "rest"

# TODO LIST
- TODO: Vary the amount of damage done
- TODO: Vary success rate of attacks
- TODO: Change hp to a wound system
- TODO: Reduce or randomize the effectiveness of blocking
- TODO: Change char data to class for both the user and the enemy; move all my* enemy* variables into the class
- TODO: Add personality templates for enemies: Different templates have different fighting preferences, and emotes for the user to try to interpret to predict their fighting style
- TODO: ? Add score keeping ? Incentivize winning faster instead of maximum caution? or do incentives need to be more organic.. dev some downside to blocking too much..
- TODO: Using HELP should not increment time OR SHOULD IT (Thinking about options require ingame hesitation! mwahaha)
- TODO: Remove do_ cmds and consolidate them into their functions outside of the cmdloop
  - Value? Is the only value making the code more traceable?