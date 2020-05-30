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
- attack function determines if an attack lands
- attack success is determined by an opposed challenge between (stamina + attack energy) vs (stamina + block mod)

## Subjectivity
- to_char attempts to print messages, but only if the target it is passed is the user
  - This probably needs to be improved to handle a more diverse number of scenarios in a more streamlined way