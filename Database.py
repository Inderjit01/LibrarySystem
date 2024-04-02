# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 08:29:35 2024

@author: inder
"""

#maintaining database
import sqlite3
from datetime import datetime, timedelta


class LibraryDatabase:
    #connect to my database
    def __init__(self, db_file): 
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        
    #will create three tables books, borrowers, and checkouts if this is the first time running    
    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books(
                      ISBN TEXT PRIMARY KEY,
                      Title TEXT,
                      Author TEXT,
                      Genre TEXT,
                      Year_Published INTEGER,
                      Total_copies INTEGER
                      )
                      ''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS borrowers (
                       Borrower_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                       Name TEXT,
                       Email TEXT,
                       Phone TEXT        
                       )
                       ''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS checkouts(
                        Checkout_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Borrower_ID INTEGER,
                        ISBN TEXT,
                        Checkout_Date TEXT,
                        Return_Date TEXT,
                        Late_Fee INTEGER,
                        FOREIGN KEY (Borrower_ID) REFERENCES borrowers(Borrower_ID),
                        FOREIGN KEY (ISBN) REFERENCES books (ISBN)
                        )
                        ''')
                       
        self.conn.commit()

    #This is for quick data inserting for testing
    def fast_data_insert(self):
    
    
        self.cursor.execute('''INSERT INTO books VALUES
                            ('978-1984801258', 'Python Crash Course', 'Eric Matthes', 'Programming', 2019, 5),
                            ('978-0596516130', 'Learning SQL', 'Alan Beaulieu', 'Database', 2009, 3)
                            ''')
        self.cursor.execute('''INSERT INTO borrowers VALUES
                            (NULL, 'John Doe', 'john@yahoo.com', '123-456-7890'),
                            (NULL, 'Jane Smith', 'jane@example.com', '987-654-3210')
                            ''')
        self.cursor.execute('''INSERT INTO checkouts VALUES
                            (NULL, 1, '978-1984801258', '2024-03-25', '2024-04-01', 0)
                            ''')
        self.conn.commit()
                 
    def close_connection(self):
        self.conn.close()
    
    #This is to add a new book to the database                  
    def insert(self):
        try:
            print("Enter the below information about the book")
            isbn = input("ISBN: ")
            if len(isbn) > 14 or len(isbn) < 14:
                print("A ISBN has to be 13 digits long. Please try again.")
                self.insert()
            self.cursor.execute('''SELECT * from books WHERE ISBN = ?''', (isbn,))
            existingBook = self.cursor.fetchone()
            
            def addingBook(isbn):
                #This is if we are adding a duplicate book
                if existingBook:
                    print("The book is already in the system.")
                    print("There are",  existingBook[5], "copies.")
                    print("How many copies would you like to add?")
                    addingCopies = int(input(""))
                    addingCopies += existingBook[5]
                    self.cursor.execute('''UPDATE books SET Total_copies = ? WHERE ISBN = ?''', (addingCopies, isbn))
                    self.conn.commit()
                    print("Added", addingCopies, "new books")
                #This will add a brand new book to this database
                else:
                    title = input("Title: ")
                    author = input("Author: ")
                    genre = input("Genre: ")
                    try:
                        year = int(input("Year Published: "))
                    except ValueError:
                        print("Year must be a number.")
                        addingBook(isbn)
                    confirmation = ("Is the below information correct Yes/No \n"
                                    "ISBN: {} \n"
                                    "Title: {} \n"
                                    "Author: {} \n"
                                    "Genre: {} \n"
                                    "Year: {} \n"
                                    "\n"
                                    ).format(isbn, title, author, genre, year)
                    userConfirmation = input(confirmation)
                    if userConfirmation.lower() == "yes":
                        self.cursor.execute('''INSERT INTO books VALUES(?, ?, ?, ?, ?, 1)''', (isbn, title, author, genre, year))
                        self.conn.commit()
                    elif userConfirmation.lower() == "no":
                        print("Action Cancelled.")
                    else:
                        print("Invalid response. Try again")
                    self.insert()

            addingBook(isbn)
        except:
            print("Invalid Input")
        
    #select and findbook looks for book information
    def select(self):
        print("Enter the ISBN to find the book you are looking for. If you do not know the ISBN leave ISBN blank and fill in the additional information if you know it.")
        isbn = input("ISBN: ")
        if len(isbn) != 0 and (len(isbn) > 14 or len(isbn) < 14):
            print("Invalid ISBN. ISBN must be 14 characters.")
            self.select()
        self.findBook(isbn)

    
    def findBook(self, isbn):
        if isbn:
            self.cursor.execute('''SELECT * FROM books WHERE ISBN = ?''', (isbn,))
            bookdata = self.cursor.fetchall()
            if bookdata:
                print()
                print("Below is the book information.")
                book = bookdata[0]
                bookinformation = ("ISBN: {}\n"
                                   "Title: {}\n"
                                   "Author: {}\n"
                                   "Genre: {}\n"
                                   "Year: {}\n"
                                   "Copies: {}\n"
                                   ).format(book[0], book[1], book[2], book[3], book[4], book[5])
                print(bookinformation)
            else:
                print("Cound not find ISBN. Try again")
                self.select()
        else:
            print("Enter as much information as you can about the book.")
            title = input("Title: ")
            author = input("Author: ")
            genre = input("Genre: ")
            year = input("Year: ")
            
            queue = "SELECT * FROM books WHERE"
            conditions = []
            values = []
            
            if title:
                conditions.append("Title = ?")
                values.append(title)
            if author:
                conditions.append("Author = ?")
                values.append(author)
            if genre:
                conditions.append("Genre = ?")
                values.append(genre)
            if year:
                conditions.append("Year = ?")
                values.append(year)
            
            queue += " " + " AND ". join(conditions)
            self.cursor.execute(queue, tuple(values))
            books = self.cursor.fetchall()
            
            if books:
                for book in books:
                    bookInformation = book
                    displayInformation = ("ISBN: {}\n"
                                       "Title: {}\n"
                                       "Author: {}\n"
                                       "Genre: {}\n"
                                       "Year: {}\n"
                                       "Copies: {}\n"
                                       ).format(bookInformation[0], bookInformation[1], bookInformation[2], bookInformation[3], bookInformation[4], bookInformation[5])
                    print(displayInformation)
            else:
                print("Could not find any information. Try Again")
                self.select()

                      
    #This allows the user to update information if a mistake was made        
    def update(self):
        print("Enter the ISBN for the book you want to change information about. If you do not know it leave it blank.")
        isbn = input("ISBN: ")
        if len(isbn) != 0 and (len(isbn) > 14 or len(isbn) < 14):
            print("Invalid ISBN. ISBN must be 14 characters.")
            self.select()
        if not isbn:
            self.findBook(isbn)
        def updateBook(isbn):
            if isbn:
                self.cursor.execute('''SELECT * FROM books WHERE ISBN = ?''', (isbn,))
                books = self.cursor.fetchall()
                if books:
                    book = books[0]
                    conformation = ("Would you like to update the below book. (Yes/No) \n"
                                        "ISBN: {} \n"
                                        "Title: {}\n"
                                        "Author: {}\n"
                                        "Genre: {}\n"
                                        "Year: {}\n"
                                        ).format(book[0], book[1], book[2], book[3], book[4])
                    userConfirmation = input(conformation)
                    if userConfirmation.lower() == "yes":
                        query = '''UPDATE books SET'''
                        values = []
                        
                        title = input("Title: ")
                        author = input("Author: ")
                        genre = input("Genre: ")
                        year = input("Year: ")
                        
                        if title:
                            query += " Title = ?,"
                            values.append(title)
                        if author:
                            query += " Author = ?,"
                            values.append(author)
                        if genre:
                            query += "Genre = ?,"
                            values.append(genre)
                        if year:
                            query += "Year = ?,"
                            values.append(year)

                        query = query.rstrip(",") + " WHERE ISBN = ?"
                        values.append(isbn)
                       
                        self.cursor.execute(query, tuple(values))
                        self.conn.commit()
                        print("User has been updated to the below information.")
                        self.cursor.execute('''SELECT * FROM books WHERE ISBN = ?''', (isbn,))
                        bookInformation = self.cursor.fetchone()

                        if bookInformation:
                            information = ("ISBN: {} \n"
                                           "Title: {}\n"
                                           "Author: {}\n"
                                           "Genre: {}\n"
                                           "Year: {} \n"
                                           "Copies: {} \n"
                                           ).format(bookInformation[0], bookInformation[1], bookInformation[2], bookInformation[3], bookInformation[4], bookInformation[5])
                            print(information)
                        else:
                            print("No user Found")                         
                        
                    elif userConfirmation.lower() == "no":
                        print("Request Canceled. Returning to menu.")
                        self.update()
                        
                    else:
                        print("Invalid input. Try again.")
                        updateBook(isbn)
                    
                else:
                    print("Cound not find any books with the ISBN. Try again.")
                    self.update()
            
        updateBook(isbn)
            
    #This will completely delete a book from the database    
    def delete(self):
        def deleteBook(userConfirmation, book, isbn):
            if userConfirmation.lower() == "yes":
                try:
                    deleteCopies = int(input("How many copies would you like to delete. You can remove {} of them: ".format(book[5])))
                    if deleteCopies <= book[5]:
                        copies = book[5] - deleteCopies
                        self.cursor.execute("""UPDATE books SET Total_copies = ? WHERE ISBN = ?""", (copies, isbn,))
                        self.conn.commit()
                        print("{} now has {} copies.".format(isbn, copies))
                    else:
                        print("Invalid number of copies entered. Maximum available: {}".format(book[5]))
                except ValueError:
                    print("Please enter a valid number.")
                    deleteBook(userConfirmation, book, isbn)
                    
            elif userConfirmation.lower() == "no":
                print("Request Canceled.")
                self.delete()
            else:
                print("Invalid response. Please try again.")
                deleteBook(isbn)
        
        def findBookToDelete(isbn):
            self.cursor.execute('''SELECT * FROM books WHERE ISBN = ?''', (isbn,))
            book = self.cursor.fetchone()
            
            if book:
                bookInformation = ("Is the below book the one you want to delete? (Yes/No) \n"
                                   "ISBN: {} \n"
                                   "Title: {} \n"
                                   "Author: {} \n"
                                   "Genre: {} \n"
                                   "Year: {} \n"
                                   "Copies: {} \n"
                                   ).format(book[0], book[1], book[2], book[3], book[4], book[5])
                userConfirmation = input(bookInformation)
                deleteBook(userConfirmation, book, isbn)
            else:
                print("Could not find any books. Try again.")
                self.delete()
                
        print("Enter the ISBN for the book you want to change information about. If you do not know it leave it blank.")
        isbn = input("ISBN: ")
        if len(isbn) != 0 and (len(isbn) > 14 or len(isbn) < 14):
            print("Invalid ISBN. ISBN must be 14 characters.")
            self.delete()
        if not isbn:
            self.findBook(isbn)
        findBookToDelete(isbn)
                
    #This will allow a borrower to check out a book    
    def checkout(self):
        def findBookInformation():
            print("Enter the isbn of the book you want to check out. If you do not know it leave it blank.")
            isbn = input("ISBN: ")
            if len(isbn) == 14 or len(isbn) == 0:
                if len(isbn) == 14:
                    self.cursor.execute('''SELECT * FROM books WHERE ISBN = ?''', (isbn,))
                    book = self.cursor.fetchone()
                    if book:
                        return book
                    else:
                        print("Invalid ISBN. Try again")
                        bookInformation()
                else:
                    self.findBook(isbn)
        def findBorrowerInformation():
            print("Enter the Library ID of the user. If you do not know it leave it blank")
            try:
                borrower = int(input("Library_ID: "))
            except:
                print("Invalid ID. Try again.")
                findBorrowerInformation()
            self.cursor.execute('''SELECT * FROM borrowers WHERE Borrower_ID = ?''', (borrower,))
            borrowerInformation = self.cursor.fetchone() 
            if borrowerInformation:
                return borrowerInformation
            else:
                print("Invalid Library ID. Try again")
                findBorrowerInformation()
        def bookCheckoutCount(isbn):
            self.cursor.execute('''Select ISBN FROM checkouts WHERE ISBN = ?''', (isbn,))
            books = self.cursor.fetchall()
            count = 0
            for book in books:
                count += 1
            return count
            
            
        bookInformation = findBookInformation()
        borrowerInformation = findBorrowerInformation()
        count = bookCheckoutCount(bookInformation[0])
        if count >= bookInformation[5]:
            print("Cannot check out this book no copies are available.")
        else:
            current_date = datetime.now()
            return_date = current_date + timedelta(weeks=2)
            formatted_current_date = current_date.strftime("%Y-%m-%d")
            formatted_return_date = return_date.strftime("%Y-%m-%d")
            
            self.cursor.execute('''INSERT INTO checkouts VALUES(NULL, ?, ?, ?, ?, 0)''', (borrowerInformation[0], bookInformation[0], formatted_current_date, formatted_return_date))  
            self.conn.commit()
            print("Succesfully checked out.")
            print()
        
    #This will allow borrowers to return there books    
    def returnBook (self):
        print("Enter the Library ID in order to return a book.")
        try:
            borrower = int(input("Library ID: "))
        except:
            print("Invalid Input. Library_ID must be a integer. Try again")
            self.returnBook()
        
        def returningBook(borrower):
            print("Enter ISBN of book being returned.")
            isbn = input("ISBN: ")
            self.cursor.execute('''SELECT * FROM checkouts WHERE Borrower_ID = ? AND ISBN = ?''', (borrower, isbn))
            checkOutInformation = self.cursor.fetchone()
            
            if checkOutInformation:
                checkout_date = datetime.strptime(checkOutInformation[3], "%Y-%m-%d")
                return_date = datetime.strptime(checkOutInformation[4], "%Y-%m-%d")
                today = datetime.now()
    
                if today > return_date:
                    days_late = (today - return_date).days
                    late_fee_per_day = 1  # Set your late fee per day here
                    late_fee = days_late * late_fee_per_day
                    print("The book is returned late. Late fee: $", late_fee)
                    userConfirmation = input("Did the user pay? (Yes/No)")
                    if userConfirmation.lower() == "yes":
                        self.cursor.execute('''DELETE * FROM checkouts WHERE Borrower_ID = ? AND ISBN = ?''', (borrower, isbn))
                        self.conn.commit()
                        print("The book has been returned.")
                    elif userConfirmation.lower() == "no":
                        print("Return request canceled.")
                    else:
                        print("Invalid input.")
                        returningBook()
                else:
                    self.cursor.execute('''DELETE FROM checkouts WHERE Borrower_ID = ? AND ISBN = ?''', (borrower, isbn))
                    self.conn.commit()
                    print("The book is returned on time.")
            else:
                print("No checkout record found for this book.")
                returningBook(borrower)
            
        
        def findCheckedOutBooks(borrower):
            self.cursor.execute('''SELECT * FROM checkouts WHERE Borrower_ID = ?''', (borrower,))
            checkOutBooks = self.cursor.fetchall()
            if checkOutBooks:
                for book in checkOutBooks:
                    print("Below are the books checked out by this person.")
                    bookISBN = book[2]
                    self.cursor.execute('''SELECT Title FROM books WHERE ISBN = ?''', (bookISBN,))
                    title = self.cursor.fetchone()
                    print("ISBN:", bookISBN, "Title:", title[0])
                returningBook(borrower)
        
            
            else:
                print("This person does not have any checked out books.")
        
        findCheckedOutBooks(borrower)              
                
    #This method will allow you to find user information based on ID, name, or email, or phoneNumber
    def findUserInformation(self):
        print("Enter the below information. If you don't know the information leave it blank")
        libraryID = input("Libary Card Number: ")
        name = input("Name: ")
        email = input("Email: ")
        phone = input("Phone Number: ")
        
        
        query = '''SELECT * FROM borrowers WHERE'''
        conditions = []
        values = []
        
        
        if libraryID:
            conditions.append("Borrower_ID = ?")
            values.append(libraryID)
        if name:
            conditions.append("Name = ?")
            values.append(name)
        if email:
            conditions.append("Email = ?")
            values.append(email)
        if phone:
            conditions.append("Phone = ?")
            values.append(phone)
        
        if conditions:
            query += " " + " AND ".join(conditions)
            self.cursor.execute(query, tuple(values))
            user_information = self.cursor.fetchall()
            
            if user_information:
                print("")
                print("Below is the information found.")
                for user in user_information: 
                    print('')
                    print("LibraryID: ", user[0])
                    print("Name: ", user[1])
                    print("Email: ", user[2])
                    print("Phone Number: ", user[3]) 
            else:
                print("No user found")
                self.findUserInformation()
        else:
            print("No search criteria provided.")
        return
            
    #This will add a new borrower    
    def addUser(self):
        print("Enter the below information to create a new user.")
        name = input("Name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        if name and email and phone:
            print("")
            userConfirmation = input("Is the below information correct. (Yes/No) \n"
                                     "Name: " + name + "\n"
                                     "Email: " + email + "\n"
                                     "Phone: " + phone + "\n"
                                     ) 
            if userConfirmation.lower() == "yes":
                self.cursor.execute('''INSERT INTO borrowers VALUES(NULL, ?, ?, ?)''', (name, email, phone))
                self.conn.commit()
                print("Succesfully added", name)
            else:
                return
        else:
            print("Invalid. Missing information")
        return 
        
    #This will borrowers to remove their accounts         
    def deleteUser(self):
        print("To delete a user, you must know the library card number. If you do not know the ID, leave it blank. To return press 0")
        library_ID = input("Library ID: ")
    
        if library_ID == "0":
            print("Returning to the main menu.")
            return
        if library_ID == "":
            self.findUserInformation()
        
        def deletionConfirmation(library_ID):
            try:
                library_ID = int(library_ID)
                self.cursor.execute('''SELECT * FROM borrowers WHERE Borrower_ID = ?''', (library_ID,))
                userInformation = self.cursor.fetchall()
                if userInformation is not None:
                    user = userInformation[0]  # Get the first user from the list
                    confirmation = ("Is the below user the one you want to delete? (Yes/No)\n"
                                    "Library ID: {}\n"
                                    "Name: {}\n"
                                    "Email: {}\n"
                                    "Phone: {}\n"
                                    ).format(user[0], user[1], user[2], user[3])
                    userConfirmation = input(confirmation)
                    if userConfirmation.lower() == "yes":
                        try:
                            self.cursor.execute('''DELETE FROM borrowers WHERE Borrower_ID = ?''', (library_ID,))
                            self.conn.commit()
                            print("User has been deleted")
                        except Exception as e:
                            print("An error occured when deleting the user:", e)
                    elif userConfirmation.lower() == "no":
                        print("Deletion cancelled.")
                    else:
                        print("Invalid response. Try again")
                        deletionConfirmation(library_ID)
                        
                
            except:
                print("Invalid input. Please enter a valid integer ID.")
        
        deletionConfirmation(library_ID)
    
        self.deleteUser()
        
    #This will allow borrowers to update their information if something is wrong.    
    def updateUser(self):
        print("Enter library ID. If you do not know it leave it blank. Press 0 to return to main menu")
        library_ID = input("Library ID: ")
        
        if library_ID == "0":
            return
        
        if not library_ID:
            self.findUserInformation()
            
        def updateConfirmation(library_ID):
            if library_ID:
                try:
                    library_ID = int(library_ID)
                    self.cursor.execute('''SELECT * FROM borrowers WHERE Borrower_ID = ?''', (library_ID,))
                    user = self.cursor.fetchone()
                    confirmation = ("Would you like to update this person information: (Yes/No) \n"
                                    "Library ID: {}\n"
                                    "Name: {} \n"
                                    "Email: {} \n"
                                    "Phone: {} \n"
                                    ).format(user[0], user[1], user[2], user[3])
                    userConfirmation = input(confirmation)
                    
                    if userConfirmation.lower() == "yes":
                        print("Leave the information you do not want to change blank.")
                        query = 'UPDATE borrowers SET'
                        values = []
                        
                        name = input("Name: ")
                        email = input("Email: ")
                        phone = input("Phone: ")
                        
                        if name:
                            query += " Name = ?,"
                            values.append(name)
                        if email:
                            query += " Email = ?,"
                            values.append(email)
                        if phone:
                            query += " Phone = ?,"
                            values.append(phone)
                            
                        query = query.rstrip(",") + " WHERE Borrower_ID = ?"
                        values.append(library_ID)
                       
                        self.cursor.execute(query, tuple(values))
                        self.conn.commit()
                        print("User has been updated to the below information.")
                        self.cursor.execute('''SELECT * FROM borrowers WHERE Borrower_ID = ?''', (library_ID,))
                        userInformation = self.cursor.fetchone()

                        if userInformation:
                            information = ("Library ID: {} \n"
                                           "Name: {}\n"
                                           "Email: {}\n"
                                           "Phone: {}\n"
                                           ).format(userInformation[0], userInformation[1], userInformation[2], userInformation[3])
                            print(information)
                        else:
                            print("No user Found")
                        
                    elif userConfirmation.lower() == "no":
                        print("Request canceled.")
                        self.updateUser()
                    else:
                        print("Invalid response try again.")
                        updateConfirmation(library_ID)
                except:
                    print("Invaild input.")
        updateConfirmation(library_ID)
        self.updateUser()
            
        
    #If i want to look at all the data
    def print_database(self):
        print("Books:")
        self.cursor.execute("SELECT * FROM books")
        print(self.cursor.fetchall())
        
        print("Borrowers:")
        self.cursor.execute("SELECT * FROM borrowers")
        print(self.cursor.fetchall())
        
        print("Checkouts:")
        self.cursor.execute("SELECT * FROM checkouts")
        print(self.cursor.fetchall())
    
        