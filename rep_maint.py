#import section
import sys
import json
import sqlite3

# path to database
database = '/Users/Sam/Desktop/repairs_maint_equip.db'
# define functions here

# connects to database and initializes cursor

conn = sqlite3.connect(database)
c = conn.cursor()

def commit():
	c.commit()

def disconnect():
	c.close()
	conn.close()

def list_all_parts():
	c.execute('SELECT * FROM partsInventory ORDER BY manufacturer')
	for row in c.fetchall():
		print(row)

def list_parts_by_manufacturer():
	print('Enter Manufacturer from list')
	man = str(input('Parts from B&S Parts\nBilly Goat Parts\nEcho Parts\nKawasaki Parts\nKohler Parts\nLittle Wonder Parts\nMiscellaneous\nOregon Parts\nRobin Subaru Parts\nRotory Parts\nSnapper Pro Parts\nSnapper Residential Parts\nStihl Parts\nWright Manufacturing Equipment\n'))
	
	c.execute("SELECT * FROM partsInventory WHERE (manufacturer LIKE ?)", [man])  # man could also be (,man) (must be tuple)
	rowcount = 0
	for row in c.fetchall():
		print(row)
		rowcount = rowcount + 1
	print('There are ', rowcount, 'records in this selection.')



while True:
	#def main():
	partopt = str(input('Enter:\n1 : parts for all manufacturers\n2 : parts for specific manufacturer\n'))
	if partopt=="1":
		list_all_parts()
		break
	if partopt=="2":
		list_parts_by_manufacturer()
		break
	else: 
		print("Enter valid option")
		continue

#commit()

	




#main()