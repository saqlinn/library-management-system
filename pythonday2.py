# Day 2: Library management system

# details of books

books = ["Spdier man", "Iron man", "captain america", "Thor"]

# Menu of Library Management system
print("Welcome to the Library management system")
print("Select an option to perform the following operations:")
print("1. view all books")
print("2. Add a book")
print("3. Search a book")
print("4. Exit")

while True:
    Menu = int(input("Enter your choice to perform the operation: "))

    if Menu == 1:
        print("The available book in the library are: ")
        for saq in books:
            print("-",saq)

    elif Menu == 2:
        print("Add a book to the library")
        bookname = input("Enter the name of book: ")
        books.append(bookname)
        print("Book added successfully!")

    elif Menu == 3:
        print("search a book in the library")
        bookname = input("Enter the bookname to search:")
        if bookname in books:
            print("The book is available in the library")
        else:
            print("Invalid bookname! The book is not available in the library")

    elif Menu == 4:
        print("Exiting the library management system. Thank You!")
        break

    else:
        print("Invalid Number! Please enter the correct number to perform the operation")
