import sys
import sqlite3

database = '/Users/Sam/Desktop/repairs_maint_equip.db'
conn = sqlite3.connect(database)
c = conn.cursor()

def commit():
	c.commit()

def disconnect():
	c.close()
	conn.close()

def list_all_parts():
	rcount = 0
	c.execute('SELECT onHand, notificationQuantity, manufacturer, partNumber, description, netUnitPrice FROM partsInventory ORDER BY manufacturer')
	for row in c.fetchall():
		rcount += 1
		print(row)
		#print(type(row[2]))
		print('There are', rcount, ' parts in our inventory')

def list_parts_by_manufacturer():
	print('Enter Manufacturer from list')
	man = str(input('Parts from B&S Parts\nBilly Goat Parts\nEcho Parts\nKawasaki Parts\nKohler Parts\nLittle Wonder Parts\nMiscellaneous\nOregon Parts\nRobin Subaru Parts\nRotory Parts\nSnapper Pro Parts\nSnapper Residential Parts\nStihl Parts\nWright Manufacturing Equipment\n'))
	c.execute("SELECT onHand, notificationQuantity, manufacturer, partNumber, description, netUnitPrice FROM partsInventory WHERE (manufacturer LIKE ?)", [man])  # man could also be (,man) (must be tuple)
	rowcount = 0
	for row in c.fetchall():
		print(row)
		rowcount += 1
	print('There are ', rowcount, 'records in this selection.')

def reorder_check():
	reorder = 0
	print('The parts listed below are below reorder limits and should be ordered:')
	c.execute('SELECT onHand, notificationQuantity, manufacturer, partNumber, description, netUnitPrice FROM partsInventory WHERE notificationQuantity < onHand')
	ro = c.fetchall()
	for row in c.fetchall():     # This is where i am stuck, will not print  out parts list at all right now; when was able to print parts would print all including null field containing records
		print(type(row[1]))
		if type(row[1]) == 'str':
			continue
		else:
			print(row)
			reorder += 1
	if reorder == 0:
		print('Inventory is sufficient.')
	elif reorder == 1:
		print('There is 1 part to reorder.')
	elif reorder > 1:
		print('There are', reorder,' parts to order')
	elif reorder < 0:
		print('Number is negative, we have a problem :( ')


while True:
	partopt = str(input('Enter:\n1 : reorder check\n2 : parts for all manufacturers\n3 : parts for specific manufacturer\n4 : exit program\n\n'))
	if partopt=="1":
		print('Reorder Check')
		reorder_check()
	if partopt=="2":
		print('List All Parts')
		list_all_parts()
		break
	if partopt=="3":
		print('List Parts by Manufacturer')
		list_parts_by_manufacturer()
		break
	if partopt=="4":
		sys.exit()
	else:
		print("Enter valid option")
		continue

