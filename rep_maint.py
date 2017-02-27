import sys
import sqlite3
import pandas as pd
import numpy as np


database = '/Users/Sam/Desktop/repairs_maint_equip.db'
conn = sqlite3.connect(database)
c = conn.cursor()

def commit():
	c.commit()

def disconnect():
	c.close()
	conn.close()

def excelopt():
	yorn = str(input('Would you like an excel form created?\ny or n:'))
	if yorn == "n":
		print('Excel sheet not created')
	if yorn == "y":
		# excel connect options and what to name sheet/wb and where to save
		print('Excel sheet created')	

def insert_info():
	ins = str(input('Please enter the location you would like to input into:\n1 : Parts\n2 : Equipment\n3 : Repair Record\n'))

#Parts	
	if ins.lower() == "1":
		#before anything, check to see if we already have part information can simply update inventory count, this section is not ready to go!!!!
		rfid = str(input("Enter the last 4 digits of RFID:\n"))
		laborHours = int(input("Enter the quantity of labor hours\n"))
		partNumber = str(input("Enter part number:\n"))      #add loop for input for repairs that have more than 1 part used
		numberOfParts = int(input("Enter number of parts used:\n"))
		dategot = str(input("Enter the date in form MM/DD/YYYY:\n"))
		print('Preparing to enter record:  Last 4 of RFID:'+rfid+'  Part number: '+partNumber+'  Quantity: '+str(numberOfParts)+'  Repair date: '+dategot+'  Labor Hours: '+str(laborHours)+"\n")

		try:
			c.execute('INSERT INTO partsInventory (equipmentRFID, laborHours, partNumber, numberOfPartsUsed, date) VALUES (?,?,?,?,?)', [rfid, laborHours, partNumber, numberOfParts, dategot])
		except:
			print('Error: Record not inserted\n')

		readyToCommit = str(input('Ready to commit?\nEnter y or n: \n'))
		if readyToCommit.lower() == "y":
			try:
				conn.commit()
				print('Last 4 of RFID:'+rfid+'  Part number: '+partNumber+'  Quantity: '+str(numberOfParts)+'  Repair date: '+dategot+'  Labor Hours: '+str(laborHours)+'  have been inserted into repairRecords\n')
			except:
				print('record not commited\n')

		if readyToCommit.lower() == "n":
			print('Record not commited\n')
#equipment
	if ins.lower() == "2":
		rfid = str(input("Enter the last 4 digits of RFID:\n"))
		laborHours = int(input("Enter the quantity of labor hours\n"))
		partNumber = str(input("Enter part number:\n"))      #add loop for input for repairs that have more than 1 part used
		numberOfParts = int(input("Enter number of parts used:\n"))
		dategot = str(input("Enter the date in form MM/DD/YYYY:\n"))
		print('Preparing to enter record:  Last 4 of RFID:'+rfid+'  Part number: '+partNumber+'  Quantity: '+str(numberOfParts)+'  Repair date: '+dategot+'  Labor Hours: '+str(laborHours)+"\n")

		try:
			c.execute('INSERT INTO repairRecords (equipmentRFID, laborHours, partNumber, numberOfPartsUsed, date) VALUES (?,?,?,?,?)', [rfid, laborHours, partNumber, numberOfParts, dategot])
		except:
			print('Error: Record not inserted\n')

		readyToCommit = str(input('Ready to commit?\nEnter y or n: \n'))
		if readyToCommit.lower() == "y":
			try:
				conn.commit()
				print('Last 4 of RFID:'+rfid+'  Part number: '+partNumber+'  Quantity: '+str(numberOfParts)+'  Repair date: '+dategot+'  Labor Hours: '+str(laborHours)+'  have been inserted into repairRecords\n')
			except:
				print('record not commited\n')

		if readyToCommit.lower() == "n":
			print('Record not commited\n')
#repair record
	if ins.lower() == "3":
		rfid = str(input("Enter the last 4 digits of RFID:\n"))
		mto = str(input('More than 1 part used in repair?\nEnter y or n: \n'))
		if mto.lower() == "y":
			partsList = []
			print("Press enter after each part number has been entered \nand type 'done' when all part numbers for repair have been added.\n")
			while True:
				partNumber = input("Enter part number:\n")
				if partNumber.lower() == "done":
					break
				partsList.append(partNumber)
				

			print(partsList)
		if mto.lower() == "n":
			partNumber = str(input("Enter part number:\n"))      #add loop for input for repairs that have more than 1 part used
		laborHours = int(input("Enter the quantity of labor hours\n"))
		numberOfParts = int(input("Enter number of parts used:\n"))
		dategot = str(input("Enter the date in form MM/DD/YYYY:\n"))
		print('Preparing to enter record:  Last 4 of RFID:'+rfid+'  Part number: '+partNumber+'  Quantity: '+str(numberOfParts)+'  Repair date: '+dategot+'  Labor Hours: '+str(laborHours)+"\n")

		try:
			c.execute('INSERT INTO repairRecords (equipmentRFID, laborHours, partNumber, numberOfPartsUsed, date) VALUES (?,?,?,?,?)', [rfid, laborHours, partNumber, numberOfParts, dategot])
		except:
			print('Error: Record not inserted\n')

		readyToCommit = str(input('Ready to commit?\nEnter y or n: \n'))
		if readyToCommit.lower() == "y":
			try:
				conn.commit()
				print('Last 4 of RFID:'+rfid+'  Part number: '+partNumber+'  Quantity: '+str(numberOfParts)+'  Repair date: '+dategot+'  Labor Hours: '+str(laborHours)+'  have been inserted into repairRecords\n')
			except:
				print('record not commited\n')

		if readyToCommit.lower() == "n":
			print('Record not commited\n')

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
	man = str(input('Parts from B&S Parts\nBilly Goat Parts\nEcho Parts\nKawasaki Parts\nKohler Parts\nLittle Wonder Parts\nMiscellaneous\nOregon Parts\nRobin Subaru Parts\nRotory Parts\nSnapper Pro Parts\nSnapper Residential Parts\nStihl Parts\nWright Manufacturing Equipment\n\n'))
	c.execute("SELECT onHand, notificationQuantity, manufacturer, partNumber, description, netUnitPrice FROM partsInventory WHERE (manufacturer LIKE ?)", [man])  # man could also be (,man) (must be tuple)
	rowcount = 0
	for row in c.fetchall():
		print(row)
		rowcount += 1
	print('There are ', rowcount, 'records in this selection.')

def reorder_check():
	reorder = 0
	print('The parts listed below are below reorder limits and should be ordered:')
	c.execute('SELECT onHand, notificationQuantity, manufacturer, partNumber, description, netUnitPrice FROM partsInventory WHERE notificationQuantity > onHand')
	for row in c.fetchall():     
		if type(row[1]) == None or row[1] == str("") or row[1] == None or row[1] == " ":  #check for null
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
	partopt = str(input('Enter:\n1 : Reorder Check\n2 : Insert Record\n3 : Parts (All Manufacturers)\n4 : Parts (Specific Manufacturer)\n9 : Exit Program\n\n'))
	if partopt=="1":
		print('Reorder Check:')
		reo = str(input('Would you like to:\n'))
		reorder_check()
		excelopt()
	if partopt=="2":
		print('Insert Record:\n')
		insert_info()
	if partopt=="3":
		print('List All Parts:\n')
		list_all_parts()
		excelopt()
	if partopt=="4":
		print('List Parts by Manufacturer:\n')
		list_parts_by_manufacturer()
		excelopt()
	if partopt=="9":
		sys.exit()
	if partopt!="1" or partopt!="2" or partopt!="3" or partopt!="4" or partopt!="9":
		print("Enter valid option:")
		continue

