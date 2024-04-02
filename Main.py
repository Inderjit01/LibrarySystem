# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 08:04:10 2024

@author: inder
"""

#My first self project

from Database import LibraryDatabase
from UserInterface import CommandLineInterface

def main():
    db = LibraryDatabase("library.db")
    db.create_tables()
    ui = CommandLineInterface()
    db.close_connection() 

if __name__ == "__main__":
    main()
    