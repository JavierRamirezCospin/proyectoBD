import tkinter
from tkinter import font
import psycopg2
import random

def registerUser(con):
    cur = con.cursor()
    try:
        cur.execute("""SELECT CustomerId
                        FROM Customer
                        ORDER BY CustomerId DESC
                        LIMIT 1""")
        CID = cur.fetchall()
        for cid in CID:
            lastCID = cid[0]

        lastCID += 1
        supportRepId = random.randint(3,5)
        rol = 1
        Username = newuserEntry.get()
        password = newpasswordEntry.get()
        FirstName = newFirstNameEntry.get()
        LastName = newLastNameEntry.get()
        Address = newAddressEntry.get()
        City = newCityEntry.get()
        Country = newCountryEntry.get()
        PostalCode = newPostalEntry.get()
        Phone = newPhoneEntry.get()
        Email = newEmailEntry.get()
        
        newCustomer = {'CustomerId':lastCID,
                       'FirstName':FirstName,
                       'LastName':LastName,
                       'Address':Address,
                       'City':City,
                       'Country':Country,
                       'PostalCode':PostalCode,
                       'Phone':Phone,
                       'Email':Email,
                       'Username':Username,
                       'password':password,
                       'SupportRepId':SupportRedId,
                       'rol':rol}
        #cur.execute("""INSERT INTO Customer (CustomerId, FirstName, LastName, Address, City, Country, PostalCode, Phone, Email, Username, password, SupportRepId, rol)
                    #VALUES ()
                #)
        print("User registered succesfully!")
    except:
        print("Registration failed!")

def loginUser(con):
    try:
        message = "User not found"
        currentUser = {}
        user = userEntry.get()
        cur = con.cursor()
        cur.execute("""SELECT Username
                        FROM Employee""")
        admins = cur.fetchall()
        for r in admins:
            if user == r[0]:
                currentUser['name'] = user
                for name, us in currentUser.items():
                    print(name + ": " + us)
                
        cur.execute("""SELECT Username
                        FROM Customer""")
        customers = cur.fetchall()
        for r in customers:
            if user == r[0]:
                userCredentials = {'username':user}
                cur.execute("""SELECT rol
                                FROM Customer
                                WHERE Username = %(username)s""",userCredentials)
                rol = cur.fetchall()
                for r in rol:
                    print(user + " " + str(r[0]))
    except:
        print("Login Failed")

def registerView():
    global newuserEntry, newpasswordEntry, newFirstNameEntry, newLastNameEntry, newAddressEntry, newCityEntry, newCountryEntry, newPostalEntry, newPhoneEntry, newEmailEntry
    registerWindow = tkinter.Tk()
    registerWindow.geometry("750x1000")
    registerWindow.title("Register Page")
    space00 = tkinter.Label(registerWindow, text="")
    space00.pack()
    title = tkinter.Label(registerWindow, text="REGISTER")
    title.config(font=("Steamer", 22, "bold"))
    title.pack()
    space0 = tkinter.Label(registerWindow, text="")
    space0.pack()
    Instructions = tkinter.Label(registerWindow, text="Username")
    Instructions.config(font=("Helvetica", 11))
    Instructions.pack()
    newuserEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newuserEntry.pack()
    space1 = tkinter.Label(registerWindow, text="")
    space1.pack()
    Instructions2 = tkinter.Label(registerWindow, text="Password")
    Instructions2.config(font=("Helvetica", 11))
    Instructions2.pack()
    newpasswordEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newpasswordEntry.pack()
    space2 = tkinter.Label(registerWindow, text="")
    space2.pack()
    Instructions3 = tkinter.Label(registerWindow, text="First Name")
    Instructions3.config(font=("Helvetica", 11))
    Instructions3.pack()
    newFirstNameEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newFirstNameEntry.pack()
    space3 = tkinter.Label(registerWindow, text="")
    space3.pack()
    Instructions4 = tkinter.Label(registerWindow, text="Last Name")
    Instructions4.config(font=("Helvetica", 11))
    Instructions4.pack()
    newLastNameEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newLastNameEntry.pack()
    space4 = tkinter.Label(registerWindow, text="")
    space4.pack()
    Instructions5 = tkinter.Label(registerWindow, text="Address")
    Instructions5.config(font=("Helvetica", 11))
    Instructions5.pack()
    newAddressEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newAddressEntry.pack()
    space5 = tkinter.Label(registerWindow, text="")
    space5.pack()
    Instructions6 = tkinter.Label(registerWindow, text="City")
    Instructions6.config(font=("Helvetica", 11))
    Instructions6.pack()
    newCityEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newCityEntry.pack()
    space6 = tkinter.Label(registerWindow, text="")
    space6.pack()
    Instructions7 = tkinter.Label(registerWindow, text="Country")
    Instructions7.config(font=("Helvetica", 11))
    Instructions7.pack()
    newCountryEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newCountryEntry.pack()
    space7 = tkinter.Label(registerWindow, text="")
    space7.pack()
    Instructions8 = tkinter.Label(registerWindow, text="Postal Code")
    Instructions8.config(font=("Helvetica", 11))
    Instructions8.pack()
    newPostalEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newPostalEntry.pack()
    space8 = tkinter.Label(registerWindow, text="")
    space8.pack()
    Instructions9 = tkinter.Label(registerWindow, text="Phone")
    Instructions9.config(font=("Helvetica", 11))
    Instructions9.pack()
    newPhoneEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newPhoneEntry.pack()
    space9 = tkinter.Label(registerWindow, text="")
    space9.pack()
    Instructions10 = tkinter.Label(registerWindow, text="Email")
    Instructions10.config(font=("Helvetica", 11))
    Instructions10.pack()
    newEmailEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newEmailEntry.pack()
    space10 = tkinter.Label(registerWindow, text="")
    space10.pack()
    loginBtn = tkinter.Button(registerWindow, text="REGISTER", padx=15, pady=5, command = lambda: registerUser(con))
    loginBtn.pack()
    space11 = tkinter.Label(registerWindow, text="")
    space11.pack()
    loginBtn = tkinter.Button(registerWindow, text="BACK", padx=15, pady=5, command = lambda: registerUser(con))
    loginBtn.pack()
    registerWindow.mainloop()

def loginView():
    global userEntry, passwordEntry
    window = tkinter.Tk()
    window.geometry("750x800")
    window.title("Login Page")
    appTitle = "WHATEVS"
    space00 = tkinter.Label(window, text="")
    space00.pack()
    space0 = tkinter.Label(window, text="")
    space0.pack()
    space1 = tkinter.Label(window, text="")
    space1.pack()
    title = tkinter.Label(window, text=appTitle)
    title.config(font=("Steamer", 50, "bold"))
    title.pack()
    space2 = tkinter.Label(window, text="")
    space2.pack()
    space3 = tkinter.Label(window, text="")
    space3.pack()
    Instructions = tkinter.Label(window, text="Username")
    Instructions.config(font=("Helvetica", 13))
    Instructions.pack()
    userEntry = tkinter.Entry(window, font="Helvetica 20")
    userEntry.pack()
    space4 = tkinter.Label(window, text="")
    space4.pack()
    Instructions2 = tkinter.Label(window, text="Password")
    Instructions2.config(font=("Helvetica", 13))
    Instructions2.pack()
    passwordEntry = tkinter.Entry(window, font="Helvetica 20")
    passwordEntry.pack()
    space5 = tkinter.Label(window, text="")
    space5.pack()
    loginBtn = tkinter.Button(window, text="LOGIN", bg="#c8c8c8",padx=30, pady=10, command = lambda: loginUser(con))
    loginBtn.pack()
    space6 = tkinter.Label(window, text="")
    space6.pack()
    space7 = tkinter.Label(window, text="")
    space7.pack()
    space8 = tkinter.Label(window, text="")
    space8.pack()
    Instructions2 = tkinter.Label(window, text="No account? Register Now!")
    Instructions2.config(font=("Helvetica", 15))
    Instructions2.pack()   
    space9 = tkinter.Label(window, text="")
    space9.pack()
    loginBtn = tkinter.Button(window, text="REGISTER", bg="#c8c8c8", padx=30, pady=10, command=registerView)
    loginBtn.pack()
    window.mainloop()

def adminView():
    adminWindow = tkinter.Tk()
    adminWindow.geometry("1350x800")
    adminWindow.title("Admin View")
    space00 = tkinter.Label(window, text="")
    space00.pack()
    adminWindow.mainloop()
    
try:
    global con
    con = psycopg2.connect(
        host = "127.0.0.1",
        database = "proyecto1",
        user = "postgres",
        password = "uvg123",
        port = 5432
    )
    print("Connected Succesfully to DB!")
    loginView()
except:
    print("Connection to Database failed!")
