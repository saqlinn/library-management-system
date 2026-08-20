# Day 3: Library management system

# details of books

books = ["Spdier man", "Iron man", "captain america", "Thor"]
issued_books = []

# Functions

def add_book():
        print("Add a book to the library")
        bookname = input("Enter the name of book: ")
        books.append(bookname)
        print("Book added successfully!")

def search_book():
        print("search a book in the library")
        bookname = input("Enter the bookname to search:")
        if bookname in books:
            print("The book is available in the library")
        else:
            print("Invalid bookname! The book is not available in the library")

def delete_book():
        print("Delete a book from the library")
        bookname = input("Enter the bookname to delete:")
        if bookname in books:
            books.remove(bookname)
            print("The book has been deleted successfully!")
        else:
            print("Invalid bookname! ")

def issue_book():
        print("Issue a book from the library")
        bookname = input("Enter the bookname to issue:")
        if bookname in books:
            books.remove(bookname)
            issued_books.append(bookname)
            print("The book has been issued successfully!")
        else:
            print("Invalid Bookname")

def return_book():
        print("return a book to the library")
        bookname = input("Enter the bookname to return:")
        if bookname in issued_books:
            issued_books.remove(bookname)
            books.append(bookname)
            print("The book has been returned successfully!")
        else:
            print("Invalid Bookname")

def view_books():
     print("The available book in the library are: ")
     for saq in books:
          print("-", saq)

def view_issued_books():
     print("The issued book in the library are: ")
     for saq in issued_books:
          print("-", saq)
# Menu of Library Management system

print("Welcome to the Library management system")
print("Select an option to perform the following operations:")
print("1. Add a book")
print("2. Search a book")
print("3. Delete a book")
print("4. Issue a book")
print("5. Return a book")
print("6. view all books")
print("7. view all issued books")
print("8. Exit")

while True:
    Menu = int(input("Enter your choice to perform the operation: "))

    if Menu == 1:
        add_book()

    elif Menu == 2:
        search_book()

    elif Menu == 3:
        delete_book()

    elif Menu == 4:
        issue_book()

    elif Menu == 5:
        return_book()
        break

    elif Menu == 6:
        view_books()

    elif Menu == 7:
        view_issued_books()

    elif Menu == 8:
        print("Exiting the Library management system...")
        break

    else:
         print("Invalid Number!")

        