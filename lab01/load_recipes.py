"""
	Bonus task: load all the available coffee recipes from the folder 'recipes/'
	File format:
		first line: coffee name
		next lines: resource=percentage

	info and examples for handling files:
		http://cs.curs.pub.ro/wiki/asc/asc:lab1:index#operatii_cu_fisiere
		https://docs.python.org/3/library/io.html
		https://docs.python.org/3/library/os.path.html
"""

import re


RECIPES_FOLDER = "recipes"


def getInfo(coffee_type):
	file_name = RECIPES_FOLDER + "/" + coffee_type + ".txt"
	used_ingredients = {}
	
	if coffee_type not in ["americano", "cappuccino", "espresso"]:
		print("this coffee type does not exist")
		return "err" 

	file = open(file_name, "r")
	coffee_name = file.readline().strip('\n')

	if coffee_name == coffee_type:
			for line in file:
					elems = line.split('=')
					used_ingredients[elems[0]] = int(elems[1])

	file.close()

	return used_ingredients