# Invoicer
Command-line program that creates invoices for private music students.

How it works:
1) Run program in terminal
2) Follow the prompts:
  a) Enter student name
  b) Enter invoice number
  c) Enter number of lessons
  d) Enter the date and duration of each lesson
4) Program saves pdf of invoice as Student_NameDate.pdf

Setup:
1) html invoice template needs relevant company info (invoice_temp.html)
2) requires sqlite3 database of student information (students.db)
  a) I populate this via a CSV file from a spreadsheet


