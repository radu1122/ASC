"""
A command-line controlled coffee maker.
"""

from operator import truediv
import re
import sys
import load_recipes as recipes

"""
Implement the coffee maker's commands. Interact with the user via stdin and print to stdout.

Requirements:
    - use functions
    - use __main__ code block
    - access and modify dicts and/or lists
    - use at least once some string formatting (e.g. functions such as strip(), lower(),
    format()) and types of printing (e.g. "%s %s" % tuple(["a", "b"]) prints "a b"
    - BONUS: read the coffee recipes from a file, put the file-handling code in another module
    and import it (see the recipes/ folder)

There's a section in the lab with syntax and examples for each requirement.

Feel free to define more commands, other coffee types, more resources if you'd like and have time.
"""

"""
Tips:
*  Start by showing a message to the user to enter a command, remove our initial messages
*  Keep types of available coffees in a data structure such as a list or dict
e.g. a dict with coffee name as a key and another dict with resource mappings (resource:percent)
as value
"""

# Commands
EXIT = "exit"
LIST_COFFEES = "list"
MAKE_COFFEE = "make"  #!!! when making coffee you must first check that you have enough resources!
HELP = "help"
REFILL = "refill"
RESOURCE_STATUS = "status"

# Coffee examples
ESPRESSO = "espresso"
AMERICANO = "americano"
CAPPUCCINO = "cappuccino"

# Resources examples
WATER = "water"
COFFEE = "coffee"
MILK = "milk"
FULL = 100
ALL = "all"
# Coffee maker's resources - the values represent the fill percents
RESOURCES = {WATER: FULL, COFFEE: FULL, MILK: FULL}

COFFEE_TYPES = ["americano", "cappuccino", "espresso"]

def listCoffees():
    print(COFFEE_TYPES)
    
def makeCoffee():
    print("Which coffee?")

    coffee_type = sys.stdin.readline().strip("\n")
    used_ingredients = recipes.getInfo(coffee_type)

    if used_ingredients == "err":
        return 

    can_make_coffee = True

    for ingredient in RESOURCES:
        if RESOURCES[ingredient] < used_ingredients[ingredient]:
            can_make_coffee = False
            print("Not enough %s!" % ingredient)
            break

    if can_make_coffee:
        for ingredient in RESOURCES:
            RESOURCES[ingredient] -= used_ingredients[ingredient]

        print("Here's your %s!" % coffee_type)
        
def refill():
    print("Which resource? Type 'all' for refilling everything")

    resource = sys.stdin.readline().strip("\n")

    if resource in RESOURCES:
        RESOURCES[resource] = FULL
    elif resource == ALL:
        for key in RESOURCES:
            RESOURCES[key] = FULL

def resourceStatus():
    for ingredient, amount in RESOURCES.items():
        print("%s: %d%%" % (ingredient, amount))


def helpFn():
    print("Available commands:\n" +
        "'list'\n" +
        "'status'\n" +
        "'refill'\n" +
        "'make'\n" +
        "'exit'")
    
    
commands = {EXIT: exit, LIST_COFFEES: listCoffees, MAKE_COFFEE: makeCoffee, REFILL: refill, RESOURCE_STATUS: resourceStatus, HELP: helpFn}


"""
Example result/interactions:

I'm a smart coffee maker
Enter command:
list
americano, cappuccino, espresso
Enter command:
status
water: 100%
coffee: 100%
milk: 100%
Enter command:
make
Which coffee?
espresso
Here's your espresso!
Enter command:
refill
Which resource? Type 'all' for refilling everything
water
water: 100%
coffee: 90%
milk: 100%
Enter command:
exit
"""

print("I'm a simple coffee maker")
print("Press enter")

isOpen = True

while isOpen:

    command = sys.stdin.readline().strip("\n")
    if command == "exit":
        break;

    if command in commands:
        commands[command]()
    else:
        print("Unknown command!")