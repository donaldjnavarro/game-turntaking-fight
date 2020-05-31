# Design Outline

## Time
- Time is incremented within the prompt class, during the postcmd check
- try_act function determines if its actually someones turn and is used before taking any actions

## Death
- Death of the player and the enemy are checked within the prompt class, during the postcmd check

## Commands
- Commands are defined within the prompt class, but they link directly to functions outside of this class so the functions can be shared by the enemies. This should all probably be consolidated into the create_char class functions.

## Combat

### Attacks
- attack() function determines if an attack lands
- Success is determined by an opposed challenge between (stamina + attack energy) vs (stamina + block mod)
- Additional attack successes cause tryStun to try to increase the target's wait timer based on a challenge between those successes and the target's hp

## Subjectivity
- to_char attempts to print messages, but only if the arg it is passed is the user
- to_char has an optional False arg for messages that are intended to display if the actor is the enemy
  - Intuition mechanics are placed within this section of to_char in order to control how many of the enemy's actions the user gets to see

## Enemy AI
- The enemy always rests when Stamina is low
- The enemy currently just selects an action at random
