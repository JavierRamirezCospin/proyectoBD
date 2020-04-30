import tkinter
from tkinter import font
import psycopg2
import random

##################################################################################################################
                                        #Funciones para el sistema
##################################################################################################################
def logout(View,currentUser):
    View.quit()
    currentUser = {}
    loginView()

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

        lastCID = lastCID + 1
        lastCID = int(lastCID)
        supportRepId = random.randint(3,5)
        supportRepId = int(supportRepId)
        rol = 1
        rol = int(rol)
        Username = newuserEntry.get()
        Username += ''
        password = newpasswordEntry.get()
        password += ''
        FirstName = newFirstNameEntry.get()
        FirstName += ''
        State = newStateEntry.get()
        State += ''
        Fax = newFaxEntry.get()
        Fax += ''
        Company = newCompanyEntry.get()
        Company += ''
        LastName = newLastNameEntry.get()
        LastName += ''
        Address = newAddressEntry.get()
        Address += ''
        City = newCityEntry.get()
        City += ''
        Country = newCountryEntry.get()
        Country += ''
        PostalCode = newPostalEntry.get()
        PostalCode += ''
        Phone = newPhoneEntry.get()
        Phone += ''
        Email = newEmailEntry.get()
        Email += ''
        
        newCustomer = {'CustomerId':lastCID,
                       'FirstName':FirstName,
                       'LastName':LastName,
                       'Company':Company,
                       'Address':Address,
                       'City':City,
                       'State':State,
                       'Country':Country,
                       'PostalCode':PostalCode,
                       'Phone':Phone,
                       'Fax':Fax,
                       'Email':Email,
                       'Username':Username,
                       'password':password,
                       'SupportRepId':supportRepId,
                       'rol':rol}
        cur.execute("""INSERT INTO Customer (CustomerId,FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, Username, password, SupportRepId, rol)
                    VALUES (%(CustomerId)i,
                    %(FirstName)s,
                    %0(LastName)s,
                    %(Company)s,
                    %(Address)s,
                    %(City)s,
                    %(State)s,
                    %(Country)s,
                    %(PostalCode)s,
                    %(Phone)s,
                    %(Fax)s,
                    %(Email)s,
                    %(Username)s,
                    %(password)s,
                    %(SupportRepId)i,
                    %(rol)i)""",newCustomer)
        print("\n->User registered succesfully!")
    except:
        print("\n->Registration failed!")

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
                currentUser['type'] = 'admin' 
                adminView(currentUser)
                
        cur.execute("""SELECT Username
                        FROM Customer""")
        customers = cur.fetchall()
        for r in customers:
            if user == r[0]:
                userCredentials = {'username':user}
                currentUser['name'] = user
                cur.execute("""SELECT rol
                                FROM Customer
                                WHERE Username = %(username)s""",userCredentials)
                rol = cur.fetchall()
                for r in rol:
                    userType = r[0]
                    
                if userType == 1:
                    currentUser['type'] = 'Tier 1'
                elif userType == 2:
                    currentUser['type'] = 'Tier 2'
                elif userType == 3:
                    currentUser['type'] = 'Tier 3'
                else:
                    currentUser['type'] = 'Custom'
    except:
        print("Login Failed")

def registerView():
    global newuserEntry, newpasswordEntry, newFaxEntry, newFirstNameEntry, newLastNameEntry, newAddressEntry, newStateEntry, newCityEntry, newCountryEntry, newPostalEntry, newPhoneEntry, newEmailEntry, newCompanyEntry
    registerWindow = tkinter.Tk()
    for i in range(7):
        registerWindow.columnconfigure(i,weight=1)
    registerWindow.geometry("850x950")
    registerWindow.title("Register Page")
    space00 = tkinter.Label(registerWindow, text=" ").grid(row=0,column=5)
    titleReg = tkinter.Label(registerWindow, text="REGISTER")
    titleReg.grid(row=2,column=3)
    titleReg.config(font=("Steamer",40,"bold"))
    space0 = tkinter.Label(registerWindow, text=" ").grid(row=4,column=3)
    Instructions = tkinter.Label(registerWindow, text="Username")
    Instructions.grid(row=6,column=2)
    Instructions.config(font=("Helvetica", 18))
    newuserEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newuserEntry.grid(row=7,column=2)
    space1 = tkinter.Label(registerWindow, text="")
    Instructions2 = tkinter.Label(registerWindow, text="Password")
    Instructions2.grid(row=6,column=4)
    Instructions2.config(font=("Helvetica", 18))
    newpasswordEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newpasswordEntry.grid(row=7,column=4)
    space2 = tkinter.Label(registerWindow, text="").grid(row=8,column=2)
    Instructions3 = tkinter.Label(registerWindow, text="First Name")
    Instructions3.grid(row=9,column=2)
    Instructions3.config(font=("Helvetica", 18))
    newFirstNameEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newFirstNameEntry.grid(row=10,column=2)
    space3 = tkinter.Label(registerWindow, text="")
    Instructions4 = tkinter.Label(registerWindow, text="Last Name")
    Instructions4.grid(row=9,column=4)
    Instructions4.config(font=("Helvetica", 18))
    newLastNameEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newLastNameEntry.grid(row=10,column=4)
    space4 = tkinter.Label(registerWindow, text="").grid(row=11,column=2)
    Instructions5 = tkinter.Label(registerWindow, text="Address")
    Instructions5.grid(row=12,column=2)
    Instructions5.config(font=("Helvetica", 18))
    newAddressEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newAddressEntry.grid(row=13,column=2)
    space5 = tkinter.Label(registerWindow, text="")
    Instructions6 = tkinter.Label(registerWindow, text="City")
    Instructions6.grid(row=12,column=4)
    Instructions6.config(font=("Helvetica", 18))
    newCityEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newCityEntry.grid(row=13,column=4)
    space6 = tkinter.Label(registerWindow, text="").grid(row=14,column=2)
    Instructions7 = tkinter.Label(registerWindow, text="Country")
    Instructions7.grid(row=15,column=2)
    Instructions7.config(font=("Helvetica", 18))
    newCountryEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newCountryEntry.grid(row=16,column=2)
    Instructions12 = tkinter.Label(registerWindow, text="State")
    Instructions12.grid(row=15,column=4)
    Instructions12.config(font=("Helvetica", 18))
    newStateEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newStateEntry.grid(row=16,column=4)
    space7 = tkinter.Label(registerWindow, text="").grid(row=17,column=2)
    Instructions8 = tkinter.Label(registerWindow, text="Postal Code")
    Instructions8.grid(row=18,column=2)
    Instructions8.config(font=("Helvetica", 18))
    newPostalEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newPostalEntry.grid(row=19,column=2)
    space8 = tkinter.Label(registerWindow, text="")
    Instructions9 = tkinter.Label(registerWindow, text="Phone")
    Instructions9.grid(row=18,column=4)
    Instructions9.config(font=("Helvetica", 18))
    newPhoneEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newPhoneEntry.grid(row=19,column=4)
    space9 = tkinter.Label(registerWindow, text="").grid(row=20,column=20)
    Instructions10 = tkinter.Label(registerWindow, text="Email")
    Instructions10.grid(row=21,column=2)
    Instructions10.config(font=("Helvetica", 18))
    newEmailEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newEmailEntry.grid(row=22,column=2)
    space10 = tkinter.Label(registerWindow, text="").grid(row=23,column=2)
    Instructions11 = tkinter.Label(registerWindow, text="Company")
    Instructions11.grid(row=21,column=4)
    Instructions11.config(font=("Helvetica", 18))
    newCompanyEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newCompanyEntry.grid(row=22,column=4)
    Instructions12 = tkinter.Label(registerWindow, text="Fax")
    Instructions12.grid(row=24,column=2)
    Instructions12.config(font=("Helvetica", 18))
    newFaxEntry = tkinter.Entry(registerWindow, font="Helvetica 11")
    newFaxEntry.grid(row=25,column=2)
    space10 = tkinter.Label(registerWindow, text="").grid(row=26,column=2)
    loginBtn = tkinter.Button(registerWindow, text="REGISTER", padx=15, pady=5, command = lambda: registerUser(con))
    loginBtn.grid(row=27,column=3)
    space11 = tkinter.Label(registerWindow, text="").grid(row=28,column=3)
    backBtn = tkinter.Button(registerWindow, text="BACK", padx=15, pady=5, command = lambda: loginView(con))
    backBtn.grid(row=29,column=3)
    registerWindow.mainloop()

def loginView(con):
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

def adminView(currentUser):
    adminWindow = tkinter.Tk()
    adminWindow.geometry("1350x800")
    adminWindow.title("Admin View")
    space00 = tkinter.Label(adminWindow, text="")
    space00.pack()
    showUser = tkinter.Label(adminWindow, text="Welcome " + currentUser['name'].title() + "!")
    showUser.config(font=("Helvetica", 26, "bold"))
    showUser.pack()
    showUserType = tkinter.Label(adminWindow, text="User type: " + currentUser['type'])
    showUserType.config(font=("Helvetica", 20, "bold"))
    showUserType.pack()
    space0 = tkinter.Label(adminWindow, text="")
    space0.pack()
    space1 = tkinter.Label(adminWindow, text="")
    space1.pack()
    registerArtist = tkinter.Button(adminWindow, text="Register New Artist", width=20, height=1)
    registerArtist.pack()
    registerAlbum = tkinter.Button(adminWindow, text="Register New Album", width=20, height=1)
    registerAlbum.pack()
    registerSong = tkinter.Button(adminWindow, text="Register New Song", width=20, height=1)
    registerSong.pack()
    modifyArtist = tkinter.Button(adminWindow, text="Modify Artist", width=20, height=1)
    modifyArtist.pack()
    modifyAlbum = tkinter.Button(adminWindow, text="Modify Album", width=20, height=1)
    modifyAlbum.pack()
    modifySong = tkinter.Button(adminWindow, text="Modify Song", width=20, height=1)
    modifySong.pack()
    removeArtist = tkinter.Button(adminWindow, text="Remove Artist", width=20, height=1)
    removeArtist.pack()
    removeAlbum = tkinter.Button(adminWindow, text="Remove Album", width=20, height=1)
    removeAlbum.pack()
    removeSong = tkinter.Button(adminWindow, text="Remove Song", width=20, height=1)
    removeSong.pack()
    deactivateSong = tkinter.Button(adminWindow, text="Deactivate Song", width=20, height=1)
    deactivateSong.pack()
    activateSong = tkinter.Button(adminWindow, text="Activate Song", width=20, height=1)
    activateSong.pack()
    manageUsers = tkinter.Button(adminWindow, text="Change User permission", width=20, height=1)
    manageUsers.pack()
    space2 = tkinter.Label(adminWindow, text="")
    space2.pack()
    space3 = tkinter.Label(adminWindow, text="")
    space3.pack()
    logoutBtn = tkinter.Button(adminWindow, text="LOGOUT", width=20, height=1, command = lambda: logout(adminWindow,currentUser))
    logoutBtn.pack()
    adminWindow.mainloop()

def newArtistView(currentUser):

def newAlbumView(currentUser):

def newSongView(currentUser):


##################################################################################################################
                                                #Programa
##################################################################################################################
    
try:
    global con
    print("->Connecting to DB...")
    con = psycopg2.connect(
        host = "127.0.0.1",
        database = "proyecto1",
        user = "postgres",
        password = "uvg123",
        port = 5432
    )
    print("->Connected Succesfully to DB!")
    loginView(con)
except:
    print("->Connection to Database failed!")
    print("->Check connection settings...")
