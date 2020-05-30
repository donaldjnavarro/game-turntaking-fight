#### Damaging Vigor
- Actions that damage your opponent's Vigor are a good way to "wear your opponent down" before a decisive action

### Rushed Actions
- A use can spend extra Vigor to reduce the cooldown on an Action

### Blocks and Preparations
- Some actions may be designed to enhance your own stats for a short period, or against certain types of actions from your opponent
  - Gameplay: Timing the usage of defensive skills before an attack 
- Intimidate: Impose a reduction in your opponents selection of skills. Reduce the list by one and make the strongest be the last item? Or actually create an aggressiveness metric for all skills and use it to modulate behavior
  - How would intimidate be a worthwhile use of an action? Just a very low cost/time action? Or perhaps a no stamina action? But then would you ever not?

### Stuns
- Temporarily unable to use Actions with a Vigor Cost

### Feints
- Enemy can use an action to send a fake attack message that actually begins a defensive stance for a short duration
- ? This would require introducing misses else the user can see the attack did no damage?
  - OR are feints best used against opponents who are blocking? and/or fake-blocking as a feint?
- Why not feint all the time? Needs a high Vigor cost?

# Questions
- Should the user be able to increase the Vigor cost of any action and thereby emphasize the damage it can do?
  - Should this be the default way costs of actions are determined? Modular actions? EX: <light> <punch> ? Or should there be preparation actions "prepare strength" that increase the next action's power?
    - Preparation actions could have a "chance to display" that determines whether the opponent gets a message showing that you are using a preparation. This chance to display could introduce a subset of learnable skills for feinting and for avoiding telegraphing
- What is the difference between taking wounds and taking vigor damage?

# TODO LIST
- TODO: Stun chance when hit = challenge(damage taken, hp) to increase victim's turn_wait
  - What should influence the number of rounds the turn_wait is increased? If damage influences the challenge success then it shouldnt also influence the number of rounds...
- TODO: Cooldown should have a chance of "taking another turn"
  - Base this on pain or stamina to reflect reflexes
  - This is important to create a degree of unpredictability to cooldowns, but only a slight amount of unpredictability. The strength of the attack and the health/energy of the actor should influence the cooldown length much more than RNG
- TODO: Change block to adding a bonus to the opposed stamina check instead of always blocking. This bonus mirrors the bonus the attacker gets from the cost of the attack
  - Should block increase the challenge roll or provide an additional challenge roll to resist damage?
- TODO: Add intuition check that determines whether enemy actions and warnings display 
- TODO: Change hp to a wound system
  - Each wound causes a pain rank which affects stamina? Reduces stamina cap? Magnifies stamina costs?
- TODO: Add personality templates for enemies: Different templates have different fighting preferences, and emotes for the user to try to interpret to predict their fighting style
- TODO: Using HELP should not increment time
