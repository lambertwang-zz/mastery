Mastery
=======

Some elements similar to [MARYSUE](https://github.com/catseye/MARYSUE)

World Store > Plot Points > Plot Lines > Simulator > Synthesize > Final

# World Store

A database of all Nouns in the world.

## Nouns ##
What are nouns?

* Noun
    * Name
    * Importance [0..10] (idk?)

* Characters
    * Appearance
    * Location
    * Wardrobe
    * Abilities

* Settings
    * Can be nested(?)
    * List of nested locations
    * Parent location

* Things
    * Type
        * Tool, clothing, weapon, trinket
    * Weight (kg)


### Noun Generation ###

This is where Pathfinder helps out.
In addition to all of the attributes listed above for characters, they also have attributes and skills that Pathfinder characters would have.

Attributes
* Strength
* Agility
* Constitution
* Charisma
* Intellect
* Wisdom

Skills
* Acrobatics
* Appraise
* Bluff
* Climb
* Craft
* Diplomacy
* Disable Device
* Disguise
* Escape Artist
* Fly
* Handle Animal
* Heal
* Intimidate
* Knowledge [Subject]
* Linguistics
* Perception
* Perform
* Profession
* Ride
* Sense Motive
* Sleight of hand
* Spellcraft
* Stealth
* Survival
* Swim
* Use Magic Device

## Dialogue and Memory ##

Characters have "memory"
Each character has a dictionary of what they know about an noun

    Who/What/Where/When/Why + Noun

That means that when an unfamiliar noun comes up in conversation, they may ask questions to develop the dialogue and increase their memory.

They also have 'feelings' toward objects or nouns.

    Love/Hate/Confusion/Anger/Sadness + Noun

These 'memories' are what drives dialogue.

### Relationships ###

Relationships are also generated for characters.

Examples:
    Brother/Sister/Co-worker/Friend/Idol/Leader/Rival/etc.

### Motivations ###


# Plot Points #

Each plot point contains a subset of the world state, like a checkpoint for the story that describes some key things that have to occur by that point. It is defined by certain locations, items, or knowledge that certain characters must have.

# Plot Lines #

Plot lines are the actual paths between each point. They contain specific events.
Events are limited to 4 types:

* Travelling
* Dialogue between party and NPCs
* Dialogue between party and party
* Combat Encounters

# Simulation #

Simulation takes these plot lines and expands them into individual actions that can be

    PlotLine(Goblin Encounter) -> [action(Bob, stab, [Goblin]), action(Goblin, die), action(Bob, loot, [Goblin])]
