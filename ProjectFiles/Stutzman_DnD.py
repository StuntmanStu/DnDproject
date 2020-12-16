#Imports
from distutils.core import setup, sys
import sys, traceback
import shutil
import time
import tkinter, tkinter.filedialog, tkinter.constants
import random
try:
	from tkinter import *
	try:
		# Python2
		import tkinter as tk
		import ttk
	except ImportError:
		# Python3
		import tkinter as tk
		import tkinter.ttk as ttk
except:
	from Tkinter import *
	try:
		import Tkinter as tk
		import ttk
	except:
		import Tkinter as tk
		import Tkinter.ttk as ttk

# XML Reading libraries
import xml.etree.ElementTree as ET

#window settings
DnD = tk.Tk ()
DnD.title("Dungeon and Dragons: Combat Simulator")
frame = ttk.Frame(DnD, padding = 2)

#variables
turnCounter = 0
playerName = ('Wizard')
enemyName = "Orcs"
whoseTurn = StringVar()
whoseTurn.set ('Select your character')
playerHit = 0
enemyHit = 0
critCounter = 0
whoseAction = StringVar()
whoseAction.set ('Roll to see if you hit!')
val = StringVar()
val.set('Please select your character')
val2 = StringVar()
val2.set('Please select your enemy')

#Player variables 
playerAC = 0
playerStrMod = 3
playerConMod = 2
playerHitMod = 5
playerDmg = 0
playerHitDie = 0
playerHealth = 0
playerHealthDisplay = StringVar()
playerHealthDisplay.set ('Your health is ' + str(playerHealth))
playerHitDice = 1
playerHitDiceHeal = random.randint(1,12)
playerHit = 0
playerHitDiceDisplay = StringVar()
playerHitDiceDisplay.set ("Hit Dice left: " + str(playerHitDice))
playerTotalHeal = 0
playerAcDisplay = StringVar()
playerAcDisplay.set("Your Armor Class is " +str(playerAC))
playerRole = StringVar()
playerRole.set('Select a character')
charBool = False
weapBool = False
playerDamMod = 0
weaponName = ('')

#Enemy variables
enemyAC = 0
enemyHealth = 0
enemyHitDie = 0
enemyDmg = 0
enemyStrMod = 3
enemyHit = 0
enemyHealthDisplay = StringVar()
enemyHealthDisplay.set ("His health is " + str(enemyHealth))
enemyAcDisplay = StringVar()
enemyAcDisplay.set("His Armor Class is " +str(enemyAC))
enemyRoleDisplay = StringVar()
enemyRoleDisplay.set("Select an enemy")
enemyBool = False
weap2Bool = False

class char(object):
	def __init__(self, index, name, role, armor, health, conMod, damMod):
		self.index = int(index)
		self.name = name
		self.role = role
		self.armor = int(armor)
		self.health = int(health)
		self.conMod = int(conMod)
		self.damMod = int(damMod)

chars = []

class weapon(object):
	def __init__(self, index, name, dice, damage):
		self.index = index
		self.name = name
		self.dice = dice
		self.damage = damage

weapons = []

def loadCharFromXml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    for charEL in root.iter('char'):
        newChar = char(charEL.find('index').text, charEL.find('name').text, charEL.find('role').text, charEL.find('armor').text, charEL.find('health').text, charEL.find('conMod').text, charEL.find('damMod').text)
        chars.append(newChar)
        print(newChar.name)
        
def loadWeaponFromXml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    for weapEL in root.iter('weapon'):
        newWeap = weapon(weapEL.find('index').text, weapEL.find('name').text, weapEL.find('dice').text, weapEL.find('damage').text)
        weapons.append(newWeap)
        print(newWeap.name)

def fillCharComboBox():
    charNames = []
    for charr in chars:
        charNames.append(charr.name)
    
    cbChar['values'] = charNames
    print(cbChar['values'])

def fillChar2ComboBox():
    charNames = []
    for charr2 in chars:
        charNames.append(charr2.name)
    
    cbChar2['values'] = charNames
    
def fillWeapComboBox():
    weapNames = []
    for weapp in weapons:
        weapNames.append(weapp.name)
    
    cbWeapon['values'] = weapNames
    print(cbWeapon['values'])
	
def fillWeap2ComboBox():
    weapNames = []
    for weapp in weapons:
        weapNames.append(weapp.name)
    
    cbWeapon2['values'] = weapNames
    print(cbWeapon['values'])
			
def rollDice(numDice, dieSize) :
	result = 0
	for loop in range(0, numDice):
		loop += 1
		result = result + random.randint(1,dieSize)
	return result

def charSelect(self):
	global playerAC
	global playerHealth
	global charBool
	global playerDamMod
	for charr in chars:
		if (charr.name == comboBoxPlayer.get()):
			playerAC = int(charr.armor)
			playerAcDisplay.set("Your Armor Class is " +str(playerAC))
			playerName = (charr.name)
			whoseTurn.set ('It is ' + charr.name + ' turn!')
			playerRole.set('You are a ' + charr.role)
			playerHealth = int(charr.health)
			playerHealthDisplay.set ('Your health is ' + str(playerHealth))
			playerDamMod = charr.damMod
			charBool = True
            
def char2Select(self):
	global enemyHealth
	global enemyAC
	global enemyBool
	for charr2 in chars:
		if (charr2.name == comboBoxPlayer2.get()):
			enemyAC = int(charr2.armor)
			enemyName = charr2.name
			enemyHealth = int(charr2.health)
			enemyHealthDisplay.set ('Your health is ' + str(enemyHealth))
			enemyRoleDisplay.set('You are a ' + charr2.role)
			enemyAcDisplay.set("Your Armor Class is " +str(enemyAC))
			enemyBool = True
         
def weapSelect(self):
	global weapBool
	global playerDamDice
	global playerDiceSize
	global weaponName
	for weapp in weapons:
		if (weapp.name == comboBoxWeapon.get()):
			weapBool = True
			playerDamDice = int(weapp.dice)
			playerDiceSize = int(weapp.damage)
			weaponName = weapp.name

def weap2Select(self):
	global weap2Bool
	for weapp in weapons:
		if (weapp.name == comboBoxWeapon2.get()):
			weap2Bool = True
            
#reset button functions
def reset():
	global playerHealth
	global playerHitDice
	global enemyHealth
	global enemyStatus
	global whoseAction
	global turnCounter
	playerHealth = 14
	playerHitDice = 1
	enemyHealth = 15
	#enemyStatus.set ('Perfectly fine')
	#enemyDefense.set ('Not the ' + enemyName + ' Turn!')
	whoseAction.set ('Ready to attack')
	#playerStatus.set ('Perfectly fine')
	enemyHealthDisplay.set ("His health is " + str(enemyHealth))
	playerHealthDisplay.set ('Your health is ' + str(playerHealth))
	whoseTurn.set ('Select your character')
	playerHitDie = 0	
	playerHitDiceDisplay.set ("# of Hit Dice left: " + str(playerHitDice))
	turnCounter = 0
	cbChar.set("Select Player")
	cbChar2.set("Select Enemy")
	cbWeapon.set("Select Weapon")
	cbWeapon2.set("Select Weapon")
	charBool = False
	char2Bool = False
	WeapBool = False
	Weap2Bool = False
	
	
#Hit Dice Heal
def healDice():
	global playerHealth
	global playerHitDice
	global playerTotalHeal
	if (playerHitDice > 0 and playerHealth < 14 and playerHealth > 0):
		playerTotalHeal = playerHitDiceHeal + playerConMod
		playerHealth = playerHealth + (playerTotalHeal)
		playerHitDice = playerHitDice - 1
		playerHealthDisplay.set ('Your health is ' + str(playerHealth))
		playerHitDiceDisplay.set ("# of Hit Dice left: " + str(playerHitDice))
		whoseAction.set('You healed for ' + str(playerTotalHeal))
		if (playerHealth > charr.health):
			playerHealth = charr.health
			playerHealthDisplay.set ('Your health is ' + str(playerHealth))
			print (playerHealth)
			print (playerHitDice)
		
#player attack
def playerStrike():
	global enemyHealth
	global playerHitDie
	global playerDmg
	global playerHit
	global turnCounter
	global critCounter
	playerHitDie = random.randint(1,20)
	if(charBool == True):
		if(weapBool == True):
			if(enemyBool == True):
				playerDmg = rollDice(playerDamDice, playerDiceSize) + playerDamMod
				if (turnCounter == 1):
					whoseAction.set ('Its not youre turn. It is ' +enemyName + "'s turn")
				if (turnCounter == 0 and playerHit == 0):
					print ("your attacking" + enemyName)
					if (playerHitDie >= enemyAC):
						playerHit = playerHit + 1;
						whoseAction.set('You hit ' + enemyName + ', now roll damage.')
						print(whoseAction.get())
						print("Now Damage")
					if (playerHitDie < enemyAC):
						whoseAction.set('You missed, its ' + enemyName + ' turn.')
						print(whoseAction.get())
						turnCounter = turnCounter + 1
						whoseTurn.set ('It is ' + enemyName + ' turn!')
						print(turnCounter)
						print ("missed")
					if (playerHitDie == 20):
						critCounter = 1
						whoseAction.set ('You rolled a natural 20!')
			else:
				whoseAction.set('You must select an enemy')
		else:
			whoseAction.set('You must select a weapon')
	else:
		whoseAction.set('You must select a character first')
		
#player damage
def playerDealsDamage():
	global playerHit
	global playerDmg
	global enemyHealth
	global turnCounter
	global critCounter
	global playerDmg
	if (turnCounter == 1):
		whoseAction.set ('Its not your turn!')
	if (playerHit == 1 and turnCounter == 0 and critCounter == 0):
		enemyHealth = enemyHealth - playerDmg
		whoseAction.set ('You did ' + str(playerDmg) + ' to ' + enemyName)
		enemyHealthDisplay.set ('His health is ' + str(enemyHealth))
		turnCounter = turnCounter + 1
		whoseTurn.set ('It is ' + enemyName + ' turn!')
		print('you attack with ' + weaponName)
		if (enemyHealth <= 0):
			whoseTurn.set (enemyName + ' is dead, your win! now reset and try again')
	if (critCounter == 1):
		enemyHealth = enemyHealth - 2*(playerDmg)
		whoseAction.set ('You crit  ' + enemyName + ' for ' + str(playerDmg))
		critCounter = critCounter - 1
		enemyHealthDisplay.set ('His health is ' + str(enemyHealth))
		turnCounter = turnCounter + 1
		if (enemyHealth <= 0):
			whoseTurn.set (enemyName + ' is dead, your win! now reset and try again')
		
#player attack
def enemyStrike():
	global playerHealth
	global enemyHitDie
	global enemyDmg
	global enemyHit
	global turnCounter
	global critCounter
	enemyHitDie = random.randint(1,20)
	if(weap2Bool == True):
		if (turnCounter == 0):
			whoseAction.set ('Its not youre turn')
		if (turnCounter == 1 and enemyHit == 0):
			print ("your attacking")
			if (enemyHitDie >= int(playerAC)):
				enemyHit = enemyHit + 1;
				whoseAction.set('You hit, now roll damage')
				print(whoseAction.get())
				print("Now Damage")
			if (enemyHitDie < playerAC):
				whoseAction.set('You missed, its the '  + str(playerName) + ' turn.')
				print(whoseAction.get())
				turnCounter = turnCounter - 1
				whoseTurn.set ('It is ' + str(playerName) + ' turn!')
				print(turnCounter)
				print ("missed")
		if (enemyHit == 20):
			critCounter = 1
			whoseAction.set ('He rolled a natural 20!')
	else:
		whoseAction.set('Select a weapon')
		
#player damage
def enemyDamage():
	global enemyHit
	global enemyDmg
	global playerHealth
	global turnCounter
	global critCounter
	enemyDmg = (random.randint(1,12)+enemyStrMod)
	if (turnCounter == 0):
		enemyStatus.set ('Its not your turn!')
	if (enemyHit == 1 and turnCounter == 1 and critCounter == 0):
		playerHealth = playerHealth - enemyDmg
		enemyDmgStr = str(enemyDmg)
		whoseAction.set ('You did ' + str(enemyDmg) + ' to ' + playerName)
		playerHealthDisplay.set ('Your health is ' + str(playerHealth))
		turnCounter = turnCounter - 1
		whoseTurn.set ('It is ' + playerName + ' turn!')
		enemyHit = enemyHit - 1
		if (playerHealth <= 0):
			whoseTurn.set (playerName + ' is dead, your lose! now reset and try again')
	if (critCounter == 1):
		playerHealth = playerHealth - 2*(enemyDmg)
		whoseAction.set ('He crit  ' + playerName + ' for ' + str(enemyDmg))
		critCounter = critCounter -	 1
		turnCounter = turnCounter - 1
		whoseTurn.set ('It is ' + playerName + ' turn!')
		if (enemyHealth <= 0):
			whoseTurn.set (str(playerName) + ' is dead, your lose! now reset and try again')

loadCharFromXml('Stutzman_DnD.xml')
loadWeaponFromXml('Stutzman_DnD.xml')

Label(DnD, height = 2).grid(row=0)

#Player Buttons and labels
#optionbox
comboBoxPlayer = StringVar()
cbChar = ttk.Combobox(DnD, textvariable = comboBoxPlayer, height = 4, width = 15)
fillCharComboBox()
cbChar.set("Select Character")
cbChar.grid(row = 1, column = 0, columnspan = 2)
cbChar.bind('<<ComboboxSelected>>', charSelect)



comboBoxWeapon = StringVar()
cbWeapon = ttk.Combobox(DnD, textvariable = comboBoxWeapon, height = 4, width = 15)
fillWeapComboBox()
cbWeapon.set("Select Weapon")
cbWeapon.grid(row = 2, column = 0, columnspan = 2)
cbWeapon.bind('<<ComboboxSelected>>', weapSelect)

Label(DnD, textvariable = playerRole, height = 5,).grid(row = 3, column = 0, columnspan = 2)
Label(DnD, textvariable = playerHealthDisplay, width = 15, height = 5, borderwidth = 2, relief = RIDGE).grid(row = 4, column = 0)
Label(DnD, textvariable = playerAcDisplay, height = 5, borderwidth = 2, relief = RIDGE).grid(row = 4, column = 1)

Label(DnD, textvariable = whoseTurn, height = 2, width = 50, borderwidth = 5, relief = RIDGE).grid(row = 5, columnspan = 4)
Label(DnD, textvariable = whoseAction, height = 2, width = 50, borderwidth = 5, relief = RIDGE).grid(row = 6, columnspan = 4)

Button(DnD, text = "Attack!", command = playerStrike, height = 5, width = 10).grid(row = 7, column = 0)
Button(DnD, text = "Damages!", command = playerDealsDamage, height = 5, width = 10).grid(row = 7, column = 1)
Label(DnD, textvariable = playerHitDiceDisplay, height = 2, borderwidth = 5, relief = RIDGE).grid(row = 8, columnspan = 2)
Button(DnD, text = "Heal yo self!", command = healDice, height = 5, width = 25).grid(row = 9, columnspan = 2)

Label(DnD, width = 5).grid(row = 0, column = 1)

#Enemy Buttons and labels
#optionbox
comboBoxPlayer2 = StringVar()
cbChar2 = ttk.Combobox(DnD, textvariable = comboBoxPlayer2, height = 4, width = 15)
fillChar2ComboBox()
cbChar2.set("Select Enemy")
cbChar2.grid(row = 1, column = 2, columnspan = 2)
cbChar2.bind('<<ComboboxSelected>>', char2Select)

comboBoxWeapon2 = StringVar()
cbWeapon2 = ttk.Combobox(DnD, textvariable = comboBoxWeapon2, height = 4, width = 15)
fillWeap2ComboBox()
cbWeapon2.set("Select Weapon")
cbWeapon2.grid(row = 2, column = 2, columnspan = 2)
cbWeapon2.bind('<<ComboboxSelected>>', weap2Select)

Label(DnD, textvariable = enemyRoleDisplay, height = 5).grid(row = 3, column = 2, columnspan = 2)
Label(DnD, textvariable = enemyHealthDisplay, width = 15, height = 5, borderwidth = 2, relief = RIDGE).grid(row = 4, column = 2)
Label(DnD, textvariable = enemyAcDisplay, height = 5, borderwidth = 2, relief = RIDGE).grid(row = 4, column = 3)

Button(DnD, text = "Attack!", command = enemyStrike, height = 5, width = 10).grid(row = 7, column = 2)
Button(DnD, text = "Damages!", command = enemyDamage, height = 5, width = 10).grid(row = 7, column = 3)

#Exit reset and mainloop
Button(DnD, text = "Try again?", command=reset, height = 2, width = 50).grid(row = 10, column = 0, columnspan = 4)
Button(DnD, text = "Run like a coward!", command=sys.exit, height = 2, width = 50).grid(row = 11, column = 0, columnspan = 4)
DnD.mainloop()