# Day 1: Library Management system

bookname = input("Enter the name of book: ")
author = input("Enter the name of author: ")
price = float(input("Enter the price of the book: "))
total_Records = int(input("Enter the total records of book: "))


membername = input("Enter the name of member: ")
age = int(input("Enter the age of member: "))
place = input("Enter the place of member: ")
contact_no = int(input("Enter the contact number of member: "))
membership_type = input("Enter the membership type (Regular/Premium):")


library_name = input("Enter the name of library: ")
library_location = input("Enter the location of Library: ")
Total_members = int(input("Enter the total number of members in the library: "))
Total_books = int(input("Enter the total number of books in the library: "))

print("\n ======== Book Details ========= ")
print("The bookname :",bookname)
print("The Author name :", author)
print("The price of the book :",price)
print("The Total copies of the book :",total_Records)

print("\n ======== Member Details ========= ")
print("The member name :", membername)
print("The age of member :", age)
print("The place of member :", place)
print("The contact numbe of member :", contact_no)
print("The membership type of member :", membership_type)

print("\n ======== Library Details ========= ")
print("The Library name :", library_name)
print("The Libray Location :", library_location)
print("The Total Number of members in the library :", Total_members)
print("The Total Number of books in the librray :", Total_books)