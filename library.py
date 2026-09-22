from database import get_connection
from datetime import date
from abc import ABC, abstractmethod


# ============================================================
# CUSTOM EXCEPTION
# ============================================================

class BookNotFound(Exception):
    pass


# ============================================================
# BOOK CLASS
# ============================================================

class Book:

    def __init__(self, book_id, isbn, title, author, category,
                 copies_available):

        self.book_id = book_id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.category = category
        self.copies_available = copies_available

    def display_book(self):

        print("Book ID:", self.book_id)
        print("ISBN:", self.isbn)
        print("Title:", self.title)
        print("Author:", self.author)
        print("Category:", self.category)
        print("Copies Available:", self.copies_available)


# ============================================================
# DIGITAL BOOK - INHERITANCE
# ============================================================

class DigitalBook(Book):

    def __init__(self, book_id, isbn, title, author, category,
                 copies_available, file_format):

        super().__init__(
            book_id,
            isbn,
            title,
            author,
            category,
            copies_available
        )

        self.file_format = file_format

    def display_book(self):

        super().display_book()
        print("Book Type: Digital Book")
        print("File Format:", self.file_format)


# ============================================================
# REFERENCE BOOK - INHERITANCE
# ============================================================

class ReferenceBook(Book):

    def __init__(self, book_id, isbn, title, author, category,
                 copies_available):

        super().__init__(
            book_id,
            isbn,
            title,
            author,
            category,
            copies_available
        )

    def display_book(self):

        super().display_book()
        print("Book Type: Reference Book")


# ============================================================
# MEMBER CLASS
# ============================================================

class Member:

    def __init__(self, member_id, name, email,
                 member_type, status):

        self.member_id = member_id
        self.name = name
        self.email = email
        self.member_type = member_type
        self.status = status

    def display_member(self):

        print("Member ID:", self.member_id)
        print("Name:", self.name)
        print("Email:", self.email)
        print("Member Type:", self.member_type)
        print("Status:", self.status)


# ============================================================
# STUDENT - INHERITANCE
# ============================================================

class Student(Member):

    def __init__(self, member_id, name, email,
                 status, course):

        super().__init__(
            member_id,
            name,
            email,
            "Student",
            status
        )

        self.course = course

    def display_member(self):

        super().display_member()
        print("Course:", self.course)


# ============================================================
# FACULTY - INHERITANCE
# ============================================================

class Faculty(Member):

    def __init__(self, member_id, name, email,
                 status, department):

        super().__init__(
            member_id,
            name,
            email,
            "Faculty",
            status
        )

        self.department = department

    def display_member(self):

        super().display_member()
        print("Department:", self.department)


# ============================================================
# ISSUE TRANSACTION CLASS
# ============================================================

class IssueTransaction:

    def __init__(
        self,
        transaction_id,
        book_id,
        member_id,
        issue_date,
        return_date
    ):

        self.transaction_id = transaction_id
        self.book_id = book_id
        self.member_id = member_id
        self.issue_date = issue_date
        self.return_date = return_date

    def display_transaction(self):

        print("Transaction ID:", self.transaction_id)
        print("Book ID:", self.book_id)
        print("Member ID:", self.member_id)
        print("Issue Date:", self.issue_date)
        print("Return Date:", self.return_date)


# ============================================================
# LIBRARY CLASS
# ============================================================

class Library:

    # --------------------------------------------------------
    # ADD BOOK
    # Required SQL: INSERT
    # --------------------------------------------------------

    def add_book(self):

        print("\n----- Add Book -----")

        try:

            isbn = input("Enter ISBN: ")
            title = input("Enter book title: ")
            author = input("Enter author: ")
            category = input("Enter category: ")

            copies = int(
                input("Enter number of copies: ")
            )

            if copies < 0:
                print("Copies cannot be negative.")
                return

            connection = get_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO books
                (
                    isbn,
                    title,
                    author,
                    category,
                    copies_available,
                    created_date
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                isbn,
                title,
                author,
                category,
                copies,
                date.today()
            )

            cursor.execute(query, values)

            connection.commit()

            print("Book added successfully!")

        except ValueError:

            print("Invalid input. Copies must be a number.")

        except Exception as error:

            print("Error:", error)

        finally:

            try:
                cursor.close()
                connection.close()
            except:
                pass


    # --------------------------------------------------------
    # SEARCH BOOK
    # Required SQL: SELECT + WHERE
    # --------------------------------------------------------

    def search_book(self):

        print("\n----- Search Book -----")

        title = input("Enter book title: ")

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT *
            FROM books
            WHERE LOWER(title) = LOWER(%s)
        """

        cursor.execute(query, (title,))

        book = cursor.fetchone()

        try:

            if book is None:
                raise BookNotFound(
                    "The book is not found."
                )

            print("\nBook found!")

            print("Book ID:",
                  book["book_id"])

            print("ISBN:",
                  book["isbn"])

            print("Title:",
                  book["title"])

            print("Author:",
                  book["author"])

            print("Category:",
                  book["category"])

            print("Copies:",
                  book["copies_available"])

        except BookNotFound as error:

            print(error)

        finally:

            cursor.close()
            connection.close()


    # --------------------------------------------------------
    # DELETE BOOK
    # --------------------------------------------------------

    def delete_book(self):

        print("\n----- Delete Book -----")

        try:

            book_id = int(
                input("Enter book ID: ")
            )

            connection = get_connection()
            cursor = connection.cursor()

            query = """
                DELETE FROM books
                WHERE book_id = %s
            """

            cursor.execute(
                query,
                (book_id,)
            )

            connection.commit()

            if cursor.rowcount == 0:

                print("Book not found.")

            else:

                print(
                    "Book deleted successfully!"
                )

        except ValueError:

            print("Book ID must be a number.")

        except Exception as error:

            print("Error:", error)

        finally:

            try:
                cursor.close()
                connection.close()
            except:
                pass


    # --------------------------------------------------------
    # UPDATE BOOK
    # --------------------------------------------------------

    def update_book(self):

        print("\n----- Update Book -----")

        try:

            book_id = int(
                input("Enter book ID: ")
            )

            title = input(
                "Enter new title: "
            )

            author = input(
                "Enter new author: "
            )

            category = input(
                "Enter new category: "
            )

            connection = get_connection()
            cursor = connection.cursor()

            query = """
                UPDATE books

                SET
                    title = %s,
                    author = %s,
                    category = %s

                WHERE book_id = %s
            """

            values = (
                title,
                author,
                category,
                book_id
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            if cursor.rowcount == 0:

                print("Book not found.")

            else:

                print(
                    "Book updated successfully!"
                )

        except ValueError:

            print("Invalid book ID.")

        finally:

            try:
                cursor.close()
                connection.close()
            except:
                pass


    # --------------------------------------------------------
    # UPDATE STOCK
    # Required SQL: UPDATE
    # --------------------------------------------------------

    def update_stock(self):

        print("\n----- Update Stock -----")

        try:

            book_id = int(
                input("Enter book ID: ")
            )

            new_stock = int(
                input("Enter new stock: ")
            )

            if new_stock < 0:

                print(
                    "Stock cannot be negative."
                )

                return

            connection = get_connection()
            cursor = connection.cursor()

            query = """
                UPDATE books

                SET copies_available = %s

                WHERE book_id = %s
            """

            cursor.execute(
                query,
                (new_stock, book_id)
            )

            connection.commit()

            if cursor.rowcount == 0:

                print("Book not found.")

            else:

                print(
                    "Stock updated successfully!"
                )

        except ValueError:

            print("Please enter valid numbers.")

        finally:

            try:
                cursor.close()
                connection.close()
            except:
                pass


    # --------------------------------------------------------
    # VIEW AVAILABLE BOOKS
    # Required SQL:
    # WHERE copies_available > 0
    # --------------------------------------------------------

    def view_available_books(self):

        print(
            "\n----- Available Books -----"
        )

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT *
            FROM books
            WHERE copies_available > 0
        """

        cursor.execute(query)

        books = cursor.fetchall()

        if len(books) == 0:

            print(
                "No books available."
            )

        else:

            for book in books:

                print("\n----------------")

                print(
                    "Book ID:",
                    book["book_id"]
                )

                print(
                    "ISBN:",
                    book["isbn"]
                )

                print(
                    "Title:",
                    book["title"]
                )

                print(
                    "Author:",
                    book["author"]
                )

                print(
                    "Category:",
                    book["category"]
                )

                print(
                    "Copies:",
                    book["copies_available"]
                )

        cursor.close()
        connection.close()


    # --------------------------------------------------------
    # ISSUE BOOK
    # --------------------------------------------------------

    def issue_book(self):

        print("\n----- Issue Book -----")

        try:

            book_id = int(
                input("Enter book ID: ")
            )

            member_id = int(
                input("Enter member ID: ")
            )

            connection = get_connection()

            cursor = connection.cursor(
                dictionary=True
            )

            # Check book

            cursor.execute(
                """
                SELECT *
                FROM books
                WHERE book_id = %s
                """,
                (book_id,)
            )

            book = cursor.fetchone()

            if book is None:

                print("Book not found.")

                return

            # Check stock

            if book["copies_available"] <= 0:

                print(
                    "No copies available."
                )

                return

            # Check member

            cursor.execute(
                """
                SELECT *
                FROM members
                WHERE member_id = %s
                AND status = 'Active'
                """,
                (member_id,)
            )

            member = cursor.fetchone()

            if member is None:

                print(
                    "Active member not found."
                )

                return

            # Reduce stock

            cursor.execute(
                """
                UPDATE books

                SET copies_available =
                    copies_available - 1

                WHERE book_id = %s
                """,
                (book_id,)
            )

            # Create transaction

            cursor.execute(
                """
                INSERT INTO issue_transactions
                (
                    book_id,
                    member_id,
                    issue_date
                )

                VALUES (%s, %s, %s)
                """,
                (
                    book_id,
                    member_id,
                    date.today()
                )
            )

            connection.commit()

            print(
                "Book issued successfully!"
            )

        except ValueError:

            print(
                "Book ID and Member ID must be numbers."
            )

        finally:

            try:
                cursor.close()
                connection.close()
            except:
                pass


    # --------------------------------------------------------
    # RETURN BOOK
    # --------------------------------------------------------

    def return_book(self):

        print("\n----- Return Book -----")

        try:

            transaction_id = int(
                input(
                    "Enter transaction ID: "
                )
            )

            connection = get_connection()

            cursor = connection.cursor(
                dictionary=True
            )

            # Find transaction

            cursor.execute(
                """
                SELECT *
                FROM issue_transactions

                WHERE transaction_id = %s

                AND return_date IS NULL
                """,
                (transaction_id,)
            )

            transaction = cursor.fetchone()

            if transaction is None:

                print(
                    "Active transaction not found."
                )

                return

            # Increase stock

            cursor.execute(
                """
                UPDATE books

                SET copies_available =
                    copies_available + 1

                WHERE book_id = %s
                """,
                (transaction["book_id"],)
            )

            # Set return date

            cursor.execute(
                """
                UPDATE issue_transactions

                SET return_date = %s

                WHERE transaction_id = %s
                """,
                (
                    date.today(),
                    transaction_id
                )
            )

            connection.commit()

            print(
                "Book returned successfully!"
            )

        except ValueError:

            print(
                "Transaction ID must be a number."
            )

        finally:

            try:
                cursor.close()
                connection.close()
            except:
                pass


    # --------------------------------------------------------
    # BORROW HISTORY
    # Required SQL: SELECT + JOIN
    # --------------------------------------------------------

    def borrow_history(self):

        print(
            "\n----- Borrow History -----"
        )

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT

                it.transaction_id,

                b.title AS book_title,

                m.name AS member_name,

                it.issue_date,

                it.return_date

            FROM issue_transactions it

            JOIN books b
                ON it.book_id = b.book_id

            JOIN members m
                ON it.member_id = m.member_id

            ORDER BY it.issue_date DESC
        """

        cursor.execute(query)

        transactions = cursor.fetchall()

        if len(transactions) == 0:

            print(
                "No borrow history found."
            )

        else:

            for transaction in transactions:

                print("\n----------------")

                print(
                    "Transaction ID:",
                    transaction[
                        "transaction_id"
                    ]
                )

                print(
                    "Book:",
                    transaction[
                        "book_title"
                    ]
                )

                print(
                    "Member:",
                    transaction[
                        "member_name"
                    ]
                )

                print(
                    "Issue Date:",
                    transaction[
                        "issue_date"
                    ]
                )

                print(
                    "Return Date:",
                    transaction[
                        "return_date"
                    ]
                )

        cursor.close()
        connection.close()


    # --------------------------------------------------------
    # TOP BORROWED BOOKS
    # Required SQL:
    # COUNT + GROUP BY + ORDER BY
    # --------------------------------------------------------

    def top_borrowed_books(self):

        print(
            "\n----- Top Borrowed Books -----"
        )

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT

                b.book_id,

                b.title,

                COUNT(it.transaction_id)
                AS borrow_count

            FROM issue_transactions it

            JOIN books b
                ON it.book_id = b.book_id

            GROUP BY
                b.book_id,
                b.title

            ORDER BY
                borrow_count DESC
        """

        cursor.execute(query)

        books = cursor.fetchall()

        if len(books) == 0:

            print(
                "No borrowing data available."
            )

        else:

            for book in books:

                print("\n----------------")

                print(
                    "Book ID:",
                    book["book_id"]
                )

                print(
                    "Book:",
                    book["title"]
                )

                print(
                    "Times Borrowed:",
                    book["borrow_count"]
                )

        cursor.close()
        connection.close()


    # --------------------------------------------------------
    # ADD MEMBER
    # --------------------------------------------------------

    def add_member(self):

        print("\n----- Add Member -----")

        try:

            name = input(
                "Enter member name: "
            )

            email = input(
                "Enter email: "
            )

            member_type = input(
                "Enter member type: "
            )

            status = input(
                "Enter status (Active/Inactive): "
            )

            connection = get_connection()

            cursor = connection.cursor()

            query = """
                INSERT INTO members
                (
                    name,
                    email,
                    member_type,
                    status
                )

                VALUES (%s, %s, %s, %s)
            """

            values = (
                name,
                email,
                member_type,
                status
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            print(
                "Member added successfully!"
            )

        except Exception as error:

            print(
                "Error:",
                error
            )

        finally:

            try:
                cursor.close()
                connection.close()
            except:
                pass


    # --------------------------------------------------------
    # VIEW MEMBERS
    # --------------------------------------------------------

    def view_members(self):

        print("\n----- Members -----")

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            "SELECT * FROM members"
        )

        members = cursor.fetchall()

        if len(members) == 0:

            print(
                "No members found."
            )

        else:

            for member in members:

                print("\n----------------")

                print(
                    "Member ID:",
                    member["member_id"]
                )

                print(
                    "Name:",
                    member["name"]
                )

                print(
                    "Email:",
                    member["email"]
                )

                print(
                    "Member Type:",
                    member["member_type"]
                )

                print(
                    "Status:",
                    member["status"]
                )

        cursor.close()
        connection.close()


# ============================================================
# MAIN MENU
# ============================================================

library = Library()


while True:

    print("\n================================")
    print("      LIBRARY MANAGEMENT")
    print("================================")

    print("1. Add Book")
    print("2. Search Book")
    print("3. Delete Book")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. View Available Books")
    print("7. Update Book")
    print("8. Update Stock")
    print("9. Add Member")
    print("10. View Members")
    print("11. Borrow History")
    print("12. Top Borrowed Books")
    print("13. Exit")

    try:

        menu = int(
            input(
                "Enter your choice: "
            )
        )

    except ValueError:

        print(
            "Invalid input! "
            "Please enter a number."
        )

        continue


    if menu == 1:

        library.add_book()


    elif menu == 2:

        library.search_book()


    elif menu == 3:

        library.delete_book()


    elif menu == 4:

        library.issue_book()


    elif menu == 5:

        library.return_book()


    elif menu == 6:

        library.view_available_books()


    elif menu == 7:

        library.update_book()


    elif menu == 8:

        library.update_stock()


    elif menu == 9:

        library.add_member()


    elif menu == 10:

        library.view_members()


    elif menu == 11:

        library.borrow_history()


    elif menu == 12:

        library.top_borrowed_books()


    elif menu == 13:

        print(
            "Exiting Library Management System..."
        )

        break


    else:

        print(
            "Invalid choice! "
            "Please select 1-13."
        )