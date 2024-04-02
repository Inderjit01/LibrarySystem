#This file is for User Interface
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 10:52:06 2024

@author: inder
"""
#UserInterface 

from Database import LibraryDatabase
import sys

class CommandLineInterface:
    
    def __init__(self):
        print("Welcome to Inderjit's library sytem version 1.0.")
        self.db = LibraryDatabase("library.db")
        self.mainMenu()
        
    def mainMenu(self):
        print("What would you like to do?")
        print("")
        print("1:Checkout/Return Book  2:Manage Books  3:User Information  4:Close Program")
        try:
            userInput = int(input())
            if 0 < userInput < 5:
                switcher = {
                    1: self.checkingReturning,
                    2: self.manageBooks,
                    3: self.userInformation,
                    4: self.termination
                }
                switcher.get(userInput)() 
            else:
                print("This is not a vaild option try a number from 1-4.")
                self.mainMenu()
        except ValueError:
            print("This is not a vaild option try a number from 1-4.")
            self.mainMenu()
         
    #this will allow the user to checkout and return book        
    def checkingReturning(self):
        print("1:Checkout Book  2:Return Book  3:Return to Main Menu")
        try:
            userInput = int(input())
            if 0 < userInput < 4:
                switcher = {
                    1: self.db.checkout,
                    2: self.db.returnBook,
                    3: self.mainMenu
                    }
                switcher.get(userInput)()
                self.mainMenu()
            else:
                print("This is not a valid option try a number from 1-3.")
                self.checkingReturning()
        except ValueError:
            print("This is not a valid option try a number from 1-3.")
            self.checkingReturning()
        
     
    #this will allow the user to manage the books,    
    def manageBooks(self):
        print("1:Insert New Book  2:Find Book  3: Update Book Information  4:Delete Book  5: Return to main menu")
        try:
            userInput = int(input())
            if 0 < userInput < 6:
                switcher = {
                    1: self.db.insert,
                    2: self.db.select,
                    3: self.db.update,
                    4: self.db.delete,
                    5: self.mainMenu
                    }
                switcher.get(userInput)()
                self.mainMenu()
            else:
                print("This is not a valid option try a number from 1-5.")
                self.manageBooks()
        except ValueError:
            print("This is not a valid option try a number from 1-5.")
            self.manageBooks()

    #This will allow the user to manage the borrowers    
    def userInformation(self):
        print("1:Look Up User Information  2:Add New User  3: Delete User  4: Update User Information  5: Return to main menu")
        try:   
            userInput = int(input())
            if 0 < userInput < 6:
                switcher = {
                    1: self.db.findUserInformation,
                    2: self.db.addUser,
                    3: self.db.deleteUser, 
                    4: self.db.updateUser, 
                    5: self.mainMenu
                    }
                switcher.get(userInput)()
                self.mainMenu()
            else:
                print("This is nor a valid option try a number from 1-5.")
                self.userInformation()
        except ValueError:
            print("This is nor a valid option try a number from 1-5.")
            self.userInformation()
    
    def termination(self):
        self.db.close_connection()
        print("The program has closed.")
        sys.exit()
    
    