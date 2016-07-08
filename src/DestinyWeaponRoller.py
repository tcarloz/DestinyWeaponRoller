#!/usr/bin/env python
import json, signal, sys, os, re
from random import randint

###########################################
# Last changes:                           #
#  - Removed the need for weaponList.json #
#    the script auto explore the path to  #
#    find the available weapon file       #
###########################################

#This script will try to load any .json file in the same path as itself and load them
#It will then provide a menu to select which weapon to roll. entering q will quit the script
#to be valid the .json file need to have a format like this:
# {"weaponName": "My Weapon name",
#  "columns":[
#    { "name": "Column 1",
#      "rows":[
#        {"name": "row 1",
#         "perks":[
#           "Perk1",
#           "Perk2"]
#        },
#        {"name": "row 2",
#         "perks":[
#           "Perk1",
#           "Perk2"]
#        }
#      ]
#    }
#  ]
#}


def jsonFromFile(fileName):
  returnString = ""
  with open(fileName) as myFile:
    for line in myFile.read():
      returnString += line.rstrip('\n\t')
  return json.loads(returnString)

def randColumn(aColumn):
    returnString = aColumn['name']+'\n'
    for aRow in aColumn['rows']:
        returnString += "\t"+aRow['name']+" : "+aRow['perks'][randint(0,len(aRow['perks'])-1)]+'\n'
    return returnString

def printMenu(weaponList):
    counter = 0
    print "What Weapon should we roll today? (enter q to quit)\n"
    for weapon in weaponList:
        print str(counter) +" -> "+weapon['weaponName']+"\n"
        counter += 1

def loadWeaponList():
    weaponList = list()
    #first loop on all the file and directory in the same path as the script
    for f in os.listdir('.'):
        #if the item is a file
        if os.path.isfile(f):
            #if the file has a .json extension
            if re.search('\.json$', f):
                try:
                    #try to read using our json parser
                    decodedFile = jsonFromFile(f)
                    #check that we at least have the weapon name for our .json file
                    if 'weaponName' in decodedFile:
                        #add it to the list
                        weaponList.append(decodedFile)
                except Exception as e:
                    print "Invalid Json format for file "+f
    return weaponList

def main():
    #try to load weapon list by finding .json file in the same directory
    weaponList = loadWeaponList()
    while 1:
        #print the weapon selection menu
        printMenu(weaponList)
        #ask user for input about the what weapon to roll
        weaponSelected = raw_input('? ')
        if weaponSelected == 'q':
            #if we type q we exit the script
            sys.exit()
        try:
            weaponNumber = -1
            try:
                #we try to cast the user input into int
                weaponNumber = int(weaponSelected)
            except Exception as e:
                #if we have an exception the user probably has typed something invalid
                print "You probably didn't enter a proper Number"
            if weaponNumber != -1:
                #we check that we have a positiv integer not bigger that the size of our list
                if weaponNumber < len(weaponList) and weaponNumber >= 0:
                    myWeapon = weaponList[weaponNumber]
                    tryCount = 0
                    try:
                        while 1:
                            tryCount += 1
                            print "Roll number: "+str(tryCount)
                            for columns in myWeapon['columns']:
                                print randColumn(columns)
                            raw_input("Press Enter for next weapon. Ctrl+C to exit\n")
                    except KeyboardInterrupt:
                        #here we catch the keyboard interrupt if the user do Ctrl+c
                        print "\nYou have done "+str(tryCount)+" roll of "+myWeapon['weaponName']
                else:
                    print "Invalid weapon number.\n"
        except Exception as e:
            print e

if __name__ == "__main__":
    main()
