# Day 3: Library management system

# details of books

import json

class BookNotFound (Exception):
       pass

with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\books.json", "r") as file:
     books = json.load(file)

with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\issued_books.json", "r") as file:
    issued_books = json.load(file)

with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\members.json", "r") as file:
    members = json.load(file)

# Functions

def add_book():
        print("Add a book to the library")
        id = int(input("Enter the book id: "))
        Bookname = input("Enter the book name: ")
        author = input("enter the author name: ")
        year = int(input("Enter the year of publications: "))
        price = int(input("ENter the price of the book: "))

        book = { "Bookid": id, "Bookname": Bookname, "author": author, "year": year, "price": price}

        books.append(book)

        with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\books.json", "w") as file:
            json.dump(books, file, indent=4)
        print("Book added successfully!")

       
def search_book():
    print("search a book in the library")
    bookname = input("Enter the bookname to search:")
    try:
        for saq in books:
            if saq["Bookname"].lower() == bookname.lower():
                  print("The book is available in the library")
                  print("book details are:")
                  print("Book id:", saq["Bookid"])
                  print("Book name:", saq["Bookname"])
                  print("author name:", saq["author"])
                  print("year of publications:", saq["year"])
                  print("price of the book:", saq["price"])
                  break

        else:
            raise BookNotFound("The book is not found")
    except BookNotFound as error:
           print(error)
            

def delete_book():
        print("Delete a book from the library")
        bookname = input("Enter the bookname to delete:")
        for saq in books:
            if bookname.lower() == saq["Bookname"].lower():
                books.remove(saq)
                print("The book has been deleted successfully!")
                break
        else:
            print("Invalid bookname! ")

            with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\books.json", "w") as file:
                                        json.dump(books, file, indent=4)

def issue_book():
        print("Issue a book from the library")
        bookname = input("Enter the bookname to issue:")
        for saq in books:
            if bookname.lower() == saq["Bookname"].lower():
                books.remove(saq)
                issued_books.append(saq)
                print("The book has been issued successfully!")
                print("-", saq)
                with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\books.json", "w") as file:
                    json.dump(books, file, indent=4)
                with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\issued_books.json", "w") as file:
                    json.dump(issued_books, file, indent=4)
                break
        else:
            print("Invalid Bookname")

        

def return_book():
    bookname = input("Enter the book name to return: ")

    for saq in issued_books:

        if bookname.lower() == saq["Bookname"].lower():

            print("Returning the book to the library...")

            issued_books.remove(saq)
            books.append(saq)

            print("The book has been returned successfully!")

            with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\books.json", "w") as file:
                json.dump(books, file, indent=4)

            with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\issued_books.json", "w") as file:
                json.dump(issued_books, file, indent=4)

            break

    else:
        print("The book is not issued from the library.")

def view_books():
     print("The available book in the library are: ")
     for saq in books:
          if len(books) != 0:
               print("book details are:")
               print("Book id:", saq["Bookid"])
               print("Book name:", saq["Bookname"])
               print("author name:", saq["author"])
               print("year of publications:", saq["year"])
               print("price of the book:", saq["price"])
          else:
               print("No books available in the library")

               with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\books.json", "w") as file:
                                                       json.dump(books, file, indent=4)

def view_issued_books():
     if len(issued_books) == 0:
        print("No books issued in the library")
     else:
        for saq in issued_books:
                print("The issued book in the library are: ")
                print("Book ID:", saq["Bookid"])
                print("Book Name:", saq["Bookname"])
                print("Author:", saq["author"])
                print("Year:", saq["year"])
                print("Price:", saq["price"])
                print()

        with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\books.json", "w") as file:
                                                  json.dump(books, file, indent=4)
        with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\issued_books.json", "w") as file:
                            json.dump(issued_books, file, indent=4)

def update_book():
     print("Update a book in the library")
     bookname = input("Enter the bookname to update:")
     for saq in books:
          id = int(input("Enter the book id:"))
          Bookname = input("Enter the book name:")
          author = input("enter the author name:")
          year = int(input("Enter the year of publications:"))
          price = int(input("Enter the price of the book:"))

          saq["Bookid"] = id
          saq["Bookname"] = Bookname
          saq["author"] = author
          saq["year"] = year
          saq["price"] = price
          print("The book has been updated successfully!")

          with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\books.json", "w") as file:
                json.dump(books, file, indent=4)
                break

def members_details():
    print("Fill the member details")
    membername = input("Enter the name of member:")
    member_id = int(input("Enter the member id:"))
    membership_type = input("Enter the membership type (Regular/premium):")
    contact_no = int(input("Enter the contact number:"))
    location = input("Enter the city name:")

    members.append({
               "name": membername,
               "id": member_id,
               "membership_type": membership_type,
               "contact_no": contact_no,
               "location": location
           })
    with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\members.json", "w") as file:
           json.dump(members, file, indent=4)

def members_view():
       print("The members in the librray are:")
       for member in members:
            print("Member name:", member["name"])
            print("Member id:", member["id"])
            print("Membership type:", member["membership_type"])
            print("Contact number:", member["contact_no"])
            print("Location:", member["location"])
            print()

            with open("C:\\Users\\saqli\\Downloads\\workspace\\Library management sys\\members.json", "w") as file:
                 json.dump(members, file, indent=4)
                 break

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
print("8. update a book")
print("9. Add a member")
print("10.view all members")
print("11. exit")

while True:
    try:
           Menu = int(input("Enter your choice to perform the operation: "))
    except ValueError:
           print("Invalid Input! Please enter a valid number.")
           continue

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

    elif Menu == 6:
        view_books()

    elif Menu == 7:
        view_issued_books()

    elif Menu == 8:
         update_book()

    elif Menu == 9:
         members_details()

    elif Menu == 10:
         members_view()

    elif Menu == 11:
        print("Exiting the Library management system...")
        break
