from jinja2 import Environment, FileSystemLoader
import datetime
import sqlite3
import pdfkit

# Connect to database and set up environment
con = sqlite3.connect("students.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

# UPDATE empty guardian values to None
cur.execute("UPDATE students SET guardian = NULLIF(guardian, '')")

# Set up jinja2 templating environment
templateLoader = FileSystemLoader(searchpath="./")
env = Environment(loader=templateLoader)

today = datetime.date.today().strftime("%B %d, %Y")

# Get student name and test against database
while True:
    student = input("Student Name: ")
    res = cur.execute(f"SELECT * FROM students WHERE name = '{student}'")
    row = res.fetchone()
    if row is None:
        print("No such student!")
        continue
    else:
        break

#Get remaining input from user
invoice_no = input("Invoice Number: ")
lessons = input("Number of lessons: ")

payer = student

if row['guardian'] is not None:
    payer = row['guardian']


# Convert input into dictionary
my_dict = {}
for x in range(int(lessons)):
    d = input(f"Lesson {x + 1} date: ")
    while True:
        try:
            l = int(input("Lesson duration: "))
        except ValueError:
            print("Please enter an integer")
        else:
            break
    my_dict[x + 1] = [d]
    my_dict[x + 1].extend([f"{l}"])

# Calculate total
rate = 1
total = 0
for key in my_dict:
    total += (int(my_dict[key][1]) * rate)


# Populate template
template = env.get_template('invoice_temp.html')     
output = template.render(
    invoice_no=invoice_no, 
    date=today, 
    my_dict=my_dict, 
    rate=rate, 
    total=total,
    payer=payer,
    address_1=row['address_1'],
    address_2=row['address_2'],
    address_3=row['address_3'],
    phone=row['phone'],
    email=row['email']
    ) 

# Write html file
with open('temp.html', 'w') as f:
    f.write(output)

options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-botton': '0.75in',
    'margin-left': '0.75in'
}

string = student + (datetime.date.today().strftime('%Y-%m-%d'))
f_name = string.replace(" ", "_")

pdfkit.from_file('temp.html', f'{f_name}.pdf')

print("Done")
