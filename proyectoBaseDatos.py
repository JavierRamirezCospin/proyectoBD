import tkinter
from tkinter import font
import psycopg2
import random

##################################################################################################################
                                        #Funciones para el sistema
##################################################################################################################
def logOut(View,currentUser):
    View.quit()
    currentUser = {}
    loginView(con)

def insertNewArtist(currentUser):
    try:
        cur = con.cursor()
        name = newArtistName.get()
        cur.execute("""SELECT ArtistId
                    FROM artist
                    ORDER BY ArtistId desc
                    LIMIT 1""")
        IDS = cur.fetchall()
        for ar in IDS:
            lastID = ar[0]
        lastID = lastID + 1
        dictionary = {'ArtistId':lastID,'Name':name}
        cur.execute("""INSERT INTO artist (artistid, name) VALUES (%(ArtistId)s,%(Name)s)""",dictionary)
        con.commit()
        print("->Artist Registered Succesfully!")
    except:
        print("-> Artist Registration Failed!")

def insertNewAlbum(currentUser):
    try:
        cur = con.cursor()
        title = albumTitle.get()
        nameArtist = albumArtistName.get()
        dictionary = {'Name':nameArtist}
        cur.execute("""SELECT artistid
                        FROM artist
                        WHERE name = %(Name)s""",dictionary)
        artistsIDs = cur.fetchall()
        for artistID in artistsIDs:
            arID = artistID[0]
            cur.execute("""SELECT albumid
                            FROM album
                            ORDER BY albumid DESC
                            LIMIT 1""")
            albumIDs = cur.fetchall()
            for albumID in albumIDs:
                lastAlID = albumID[0]
                lastAlID += 1
                dictionary2 = {'AlbumId':lastAlID,'Title':title,'ArtistId':arID}
                cur.execute("""INSERT INTO album (albumid, title, artistid)
                            VALUES (%(AlbumId)s,%(Title)s,%(ArtistId)s)""",dictionary2)
                con.commit()
                print("-> Album Registered Succesfully!")
    except:
        print("-> Album Registration Failed!")

def insertNewSong(currentUser):
    try:
        cur = con.cursor()
        songTitle = newSongTitle.get()
        songAlbum = newSongAlbumName.get()
        mediaType = newSongMediaType.get()
        songGenre = newSongGenre.get()
        songComposer = newSongComposer.get()
        songMilliseconds = newSongMilliseconds.get()
        songMilliseconds = int(songMilliseconds)
        songBytes = newSongBytes.get()
        songBytes = int(songBytes)
        songPrice = newSongPrice.get()
        songPrice = float(songPrice)
        cur.execute("""SELECT trackid
                FROM track
                ORDER BY trackid DESC
                LIMIT 1""")
        tracksIDs = cur.fetchall()
        for trackID in tracksIDs:
            lastTrackID = trackID[0]
            lastTrackID += 1
            dictionary = {'Title':songTitle,'Name':songGenre,'MediaName':mediaType}
            cur.execute("""SELECT albumid
                            FROM album
                            WHERE title = %(Title)s""",dictionary)
            albumsIDs = cur.fetchall()
            for albumID in albumsIDs:
                rightAlbumID = albumID[0]
                cur.execute("""SELECT genreid
                            FROM genre
                            WHERE name = %(Name)s""",dictionary)
                genresIDs = cur.fetchall()
                for genreID in genresIDs:
                    rightGenreID = genreID[0]
                    cur.execute("""SELECT mediatypeid
                            FROM mediatype
                            WHERE name = %(MediaName)s""",dictionary)
                    mediaTypesIDs = cur.fetchall()
                    for mediaTypeID in mediaTypesIDs:
                        rightMediaType = mediaTypeID[0]
                        lastDictionary = {'TrackId':lastTrackID,
                                          'Name':songTitle,
                                          'AlbumId':rightAlbumID,
                                          'MediaTypeId':rightMediaType,
                                          'GenreId':rightGenreID,
                                          'Composer':songComposer,
                                          'Milliseconds':songMilliseconds,
                                          'Bytes':songBytes,
                                          'UnitPrice':songPrice}
                        print("Done Succesfully!")
    except:
        print("New Song Registration Failed!")

def modifyArtist(currentUser):
    try:
        cur = con.cursor()
        oldArtist = oldArtistName.get()
        newArtist = upArtistName.get()
        dictionary = {'OldName':oldArtist,'Name':newArtist}
        cur.execute("""UPDATE artist
                        SET name = %(Name)s
                        WHERE name = %(OldName)s""",dictionary)
        con.commit()
        print("\n-> Artist Updated Succesfully!")
    except:
        print("\nArtist Update Failed!")

def modifyAlbum(currentUser):
    try:
        cur = con.cursor()   
        oldAlbum = oldAlbumName.get()
        newAlbum = upAlbumName.get()
        newArtist = upAlbumArtist.get()
        lastAlbumID = 0
        dictionary = {'ArtistName':newArtist,'AlbumName':oldAlbum}
        cur.execute("""SELECT albumid
                        FROM album
                        WHERE title = %(AlbumName)s""",dictionary)
        albumIDS = cur.fetchall()
        for albumID in albumIDS:
            lastAlbumID = albumID[0]
        lastAlbumID += 1
        cur.execute("""SELECT artistid FROM artist WHERE name = %(ArtistName)s""",dictionary)
        artistsIDs = cur.fetchall()
        for artistID in artistsIDs:
            rightID = artistID[0]
            finalDictionary = {'OldAlbum':oldAlbum,'albumID':lastAlbumID,'NewAlbum':newAlbum,'ArtistID':rightID}
            cur.execute("""UPDATE album
                            SET albumID = %(albumID)s,
                                title = %(NewAlbum)s,
                                artistid = %(ArtistID)s
                        WHERE title = %(OldAlbum)s""",finalDictionary)
            con.commit()
        print("\n-> Artist Updated Succesfully!")
    except:
        print("\nArtist Update Failed!")

def songDeactivation(currentUser):
    try:
        cur = con.cursor()
        songTitle = deactivateSongTitle.get()
        songComposer = deactivateSongComposer.get()
        dictionary = {'Name':songTitle}
        cur.execute("""SELECT activa
                        FROM track
                        WHERE name = %(Name)s""",dictionary)
        activos = cur.fetchall()
        for activo in activos:
            if activo[0] == 1:
                cur.execute("""UPDATE track
                                SET activa = 2
                                WHERE name = %(Name)s""",dictionary)
                con.commit()
                print("-> Song Deactivated Succesfully!")
            elif activo[0] == 2:
                print("-> Song Already Deactivated!")
    except:
        print("-> Song Deactivation Failed!")

def songActivation(currentUser):
    try:
        cur = con.cursor()
        songTitle = activateSongTitle.get()
        songComposer = activateSongComposer.get()
        dictionary = {'Name':songTitle}
        cur.execute("""SELECT activa
                        FROM track
                        WHERE name = %(Name)s""",dictionary)
        activos = cur.fetchall()
        for activo in activos:
            if activo[0] == 2:
                cur.execute("""UPDATE track
                                SET activa = 1
                                WHERE name = %(Name)s""",dictionary)
                con.commit()
                print("-> Song Activated Succesfully!")
            elif activo[0] == 1:
                print("-> Song is Active!")
    except:
        print("-> Song Activation Failed!")

def changeUserPermission(currentUser):
    try:
        cur = con.cursor()
        usName = permissionUsername.get()
        newPer = permissionNewNumber.get()
        newPer = int(newPer)
        dictionary = {'username':usName,'rol':newPer}
        cur.execute("""SELECT rol
                        FROM customer
                        WHERE username = %(username)s""",dictionary)
        permissions = cur.fetchall()
        for permission in permissions:
            if permission[0] == newPer:
                print("\n-> User Already With That Permission!")
            else:
                cur.execute("""UPDATE customer
                        SET rol = %(rol)s
                        WHERE username = %(username)s""",dictionary)
                con.commit()
                print("\n-> Customer Permission Updated!")
    except:
        print("\n-> User Permission Failed!")
        
def registerUser(con):
    try:
        cur = con.cursor()
        cur.execute("""SELECT CustomerId
                        FROM Customer
                        ORDER BY CustomerId DESC
                        LIMIT 1""")
        customerID = cur.fetchall()
        for cid in customerID:
            lastCustomerID = cid[0]
            lastCustomerID += 1
            supportRepId = random.randint(3,5)
            rol = 1
            Username = newuserEntry.get()
            password = newpasswordEntry.get()
            FirstName = newFirstNameEntry.get()
            State = newStateEntry.get()
            Fax = newFaxEntry.get()
            Company = newCompanyEntry.get()
            LastName = newLastNameEntry.get()
            Address = newAddressEntry.get()
            City = newCityEntry.get()
            Country = newCountryEntry.get()
            PostalCode = newPostalEntry.get()
            Phone = newPhoneEntry.get()
            Email = newEmailEntry.get()
            
            newCustomer = {'CustomerId':lastCustomerID,
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
            cur.execute("""INSERT INTO Customer (CustomerId,
                                                FirstName,
                                                LastName,
                                                Company,
                                                Address,
                                                City,
                                                State,
                                                Country,
                                                PostalCode,
                                                Phone,
                                                Fax,
                                                Email,
                                                Username,
                                                password,
                                                SupportRepId,
                                                rol)
                        VALUES (%(CustomerId)s,
                        %(FirstName)s,
                        %(LastName)s,
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
                        %(SupportRepId)s,
                        %(rol)s)""",newCustomer)
            con.commit()
            print("\n->User registered succesfully!")
    except:
        print("\n->Registration failed!")

def loginUser(con):
    try:
        message = "User not found"
        currentUser = {}
        for name, us in currentUser.items():
            print(name + ": " + us)
        user = userEntry.get()
        password = passwordEntry.get()
        cur = con.cursor()
        cur.execute("""SELECT Username, password
                        FROM Employee""")
        admins = cur.fetchall()
        for r in admins:
            if user == r[0] and password == r[1]:
                currentUser['name'] = user
                currentUser['type'] = 'admin' 
                adminView(currentUser)
                
        cur.execute("""SELECT Username, password
                        FROM Customer""")
        customers = cur.fetchall()
        for r in customers:
            if user == r[0] and password == r[1]:
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
                        customer1View(currentUser)
                    elif userType == 2:
                        currentUser['type'] = 'Tier 2'
                        customer2View(currentUser)
                    elif userType == 3:
                        currentUser['type'] = 'Tier 3'
    except:
        print("Login Failed")

##################################################################################################################
                                        #Vistas del sistema
##################################################################################################################

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

def customer1View(currentUser):
    customer1View = tkinter.Tk()
    customer1View.geometry("1350x800")
    customer1View.title("Customer Tier 1 View")
    for i in range(7):
        customer1View.columnconfigure(i,weight=1)
    space00 = tkinter.Label(customer1View, text="").grid(row=0,column=3)
    showUser = tkinter.Label(customer1View, text="Welcome " + currentUser['name'].title() + "!")
    showUser.grid(row=1,column=1)
    showUser.config(font=("Helvetica", 20, "bold"))
    showUserType = tkinter.Label(customer1View, text="User type: Costumer " + currentUser['type'])
    showUserType.grid(row=2,column=1)
    showUserType.config(font=("Helvetica", 20, "bold"))
    space0 = tkinter.Label(customer1View, text="").grid(row=3,column=1)
    registerArtist = tkinter.Button(customer1View, text="Register New Artist", width=20, height=1, command = lambda: newArtistView(currentUser))
    registerArtist.grid(row=4,column=1)
    registerAlbum = tkinter.Button(customer1View, text="Register New Album", width=20, height=1, command = lambda: newAlbumView(currentUser))
    registerAlbum.grid(row=5,column=1)
    registerSong = tkinter.Button(customer1View, text="Register New Song", width=20, height=1, command = lambda: newSongView(currentUser))
    registerSong.grid(row=6,column=1)
    space1 = tkinter.Label(customer1View, text="").grid(row=7,column=1)
    space2 = tkinter.Label(customer1View, text="").grid(row=8,column=1)
    space3 = tkinter.Label(customer1View, text="").grid(row=9,column=1)
    space4 = tkinter.Label(customer1View, text="").grid(row=10,column=1)
    space5 = tkinter.Label(customer1View, text="").grid(row=11,column=1)
    space6 = tkinter.Label(customer1View, text="").grid(row=12,column=1)
    space7 = tkinter.Label(customer1View, text="").grid(row=13,column=1)
    space8 = tkinter.Label(customer1View, text="").grid(row=14,column=1)
    space9 = tkinter.Label(customer1View, text="").grid(row=15,column=1)
    space10 = tkinter.Label(customer1View, text="").grid(row=16,column=1)
    space11 = tkinter.Label(customer1View, text="").grid(row=17,column=1)
    logoutBtn = tkinter.Button(customer1View, text="LOGOUT", width=20, height=1, bg="#ff9999", command = lambda: logOut(customer1View,currentUser))
    logoutBtn.grid(row=18,column=1)

def customer2View(currentUser):
    customer2View = tkinter.Tk()
    customer2View.geometry("1350x800")
    customer2View.title("Customer Tier 1 View")
    for i in range(7):
        customer2View.columnconfigure(i,weight=1)
    space00 = tkinter.Label(customer2View, text="").grid(row=0,column=3)
    showUser = tkinter.Label(customer2View, text="Welcome " + currentUser['name'].title() + "!")
    showUser.grid(row=1,column=1)
    showUser.config(font=("Helvetica", 20, "bold"))
    showUserType = tkinter.Label(customer2View, text="User type: Costumer " + currentUser['type'])
    showUserType.grid(row=2,column=1)
    showUserType.config(font=("Helvetica", 20, "bold"))
    space0 = tkinter.Label(customer2View, text="").grid(row=3,column=1)
    registerArtist = tkinter.Button(customer2View, text="Register New Artist", width=20, height=1, command = lambda: newArtistView(currentUser))
    registerArtist.grid(row=4,column=1)
    registerAlbum = tkinter.Button(customer2View, text="Register New Album", width=20, height=1, command = lambda: newAlbumView(currentUser))
    registerAlbum.grid(row=5,column=1)
    registerSong = tkinter.Button(customer2View, text="Register New Song", width=20, height=1, command = lambda: newSongView(currentUser))
    registerSong.grid(row=6,column=1)
    modifyArtist = tkinter.Button(customer2View, text="Modify Artist", width=20, height=1, command = lambda: modifyArtistView(currentUser))
    modifyArtist.grid(row=7,column=1)
    modifyAlbum = tkinter.Button(customer2View, text="Modify Album", width=20, height=1, command = lambda: modifyAlbumView(currentUser))
    modifyAlbum.grid(row=8,column=1)
    modifySong = tkinter.Button(customer2View, text="Modify Song", width=20, height=1, command = lambda: modifySongView(currentUser))
    modifySong.grid(row=9,column=1)
    space0 = tkinter.Label(customer2View, text="").grid(row=10,column=1)
    space0 = tkinter.Label(customer2View, text="").grid(row=11,column=1)
    space0 = tkinter.Label(customer2View, text="").grid(row=12,column=1)
    space0 = tkinter.Label(customer2View, text="").grid(row=13,column=1)
    space0 = tkinter.Label(customer2View, text="").grid(row=14,column=1)
    space0 = tkinter.Label(customer2View, text="").grid(row=15,column=1)
    space0 = tkinter.Label(customer2View, text="").grid(row=16,column=1)
    space0 = tkinter.Label(customer2View, text="").grid(row=17,column=1)
    logoutBtn = tkinter.Button(customer2View, text="LOGOUT", width=20, height=1, bg="#ff9999", command = lambda: logOut(customer2View,currentUser))
    logoutBtn.grid(row=18,column=1)
    customer2View.mainloop()

def customer3View(currentUser):
    customer3View = tkinter.Tk()
    customer3View.geometry("1350x800")
    customer3View.title("Customer Tier 1 View")
    for i in range(7):
        customer3View.columnconfigure(i,weight=1)
    space00 = tkinter.Label(customer3View, text="").grid(row=0,column=3)
    showUser = tkinter.Label(customer3View, text="Welcome " + currentUser['name'].title() + "!")
    showUser.grid(row=1,column=1)
    showUser.config(font=("Helvetica", 20, "bold"))
    showUserType = tkinter.Label(customer3View, text="User type: Costumer " + currentUser['type'])
    showUserType.grid(row=2,column=1)
    showUserType.config(font=("Helvetica", 20, "bold"))
    space0 = tkinter.Label(customer3View, text="").grid(row=3,column=1)
    registerArtist = tkinter.Button(customer3View, text="Register New Artist", width=20, height=1, command = lambda: newArtistView(currentUser))
    registerArtist.grid(row=4,column=1)
    registerAlbum = tkinter.Button(customer3View, text="Register New Album", width=20, height=1, command = lambda: newAlbumView(currentUser))
    registerAlbum.grid(row=5,column=1)
    registerSong = tkinter.Button(customer3View, text="Register New Song", width=20, height=1, command = lambda: newSongView(currentUser))
    registerSong.grid(row=6,column=1)
    modifyArtist = tkinter.Button(customer3View, text="Modify Artist", width=20, height=1, command = lambda: modifyArtistView(currentUser))
    modifyArtist.grid(row=7,column=1)
    modifyAlbum = tkinter.Button(customer3View, text="Modify Album", width=20, height=1, command = lambda: modifyAlbumView(currentUser))
    modifyAlbum.grid(row=8,column=1)
    modifySong = tkinter.Button(customer3View, text="Modify Song", width=20, height=1, command = lambda: modifySongView(currentUser))
    modifySong.grid(row=9,column=1)
    deactivateSong = tkinter.Button(customer3View, text="Deactivate Song", width=20, height=1, command = lambda: deactivateSongView(currentUser))
    deactivateSong.grid(row=13,column=1)
    activateSong = tkinter.Button(customer3View, text="Activate Song", width=20, height=1, command = lambda: activateSongView(currentUser))
    activateSong.grid(row=14,column=1)
    space0 = tkinter.Label(customer3View, text="").grid(row=15,column=1)
    space0 = tkinter.Label(customer3View, text="").grid(row=16,column=1)
    space0 = tkinter.Label(customer3View, text="").grid(row=17,column=1)
    logoutBtn = tkinter.Button(customer3View, text="LOGOUT", width=20, height=1, bg="#ff9999", command = lambda: logOut(customer3View,currentUser))
    logoutBtn.grid(row=18,column=1)
    customer2View.mainloop()
    
def adminView(currentUser):
    adminWindow = tkinter.Tk()
    adminWindow.geometry("1350x800")
    adminWindow.title("Admin View")
    for i in range(7):
        adminWindow.columnconfigure(i,weight=1)
    space00 = tkinter.Label(adminWindow, text="").grid(row=0,column=3)
    showUser = tkinter.Label(adminWindow, text="Welcome " + currentUser['name'].title() + "!")
    showUser.grid(row=1,column=1)
    showUser.config(font=("Helvetica", 20, "bold"))
    showUserType = tkinter.Label(adminWindow, text="User type: " + currentUser['type'])
    showUserType.grid(row=2,column=1)
    showUserType.config(font=("Helvetica", 20, "bold"))
    space0 = tkinter.Label(adminWindow, text="").grid(row=3,column=1)
    registerArtist = tkinter.Button(adminWindow, text="Register New Artist", width=20, height=1, command = lambda: newArtistView(currentUser))
    registerArtist.grid(row=4,column=1)
    registerAlbum = tkinter.Button(adminWindow, text="Register New Album", width=20, height=1, command = lambda: newAlbumView(currentUser))
    registerAlbum.grid(row=5,column=1)
    registerSong = tkinter.Button(adminWindow, text="Register New Song", width=20, height=1, command = lambda: newSongView(currentUser))
    registerSong.grid(row=6,column=1)
    modifyArtist = tkinter.Button(adminWindow, text="Modify Artist", width=20, height=1, command = lambda: modifyArtistView(currentUser))
    modifyArtist.grid(row=7,column=1)
    modifyAlbum = tkinter.Button(adminWindow, text="Modify Album", width=20, height=1, command = lambda: modifyAlbumView(currentUser))
    modifyAlbum.grid(row=8,column=1)
    modifySong = tkinter.Button(adminWindow, text="Modify Song", width=20, height=1, command = lambda: modifySongView(currentUser))
    modifySong.grid(row=9,column=1)
    removeArtist = tkinter.Button(adminWindow, text="Remove Artist", width=20, height=1, command = lambda: removeArtistView(currentUser))
    removeArtist.grid(row=10,column=1)
    removeAlbum = tkinter.Button(adminWindow, text="Remove Album", width=20, height=1, command = lambda: removeAlbumView(currentUser))
    removeAlbum.grid(row=11,column=1)
    removeSong = tkinter.Button(adminWindow, text="Remove Song", width=20, height=1, command = lambda: removeSongView(currentUser))
    removeSong.grid(row=12,column=1)
    deactivateSong = tkinter.Button(adminWindow, text="Deactivate Song", width=20, height=1, command = lambda: deactivateSongView(currentUser))
    deactivateSong.grid(row=13,column=1)
    activateSong = tkinter.Button(adminWindow, text="Activate Song", width=20, height=1, command = lambda: activateSongView(currentUser))
    activateSong.grid(row=14,column=1)
    manageUsers = tkinter.Button(adminWindow, text="Change User permission", width=20, height=1, command = lambda: userPermissionView(currentUser))
    manageUsers.grid(row=15,column=1)
    space2 = tkinter.Label(adminWindow, text="").grid(row=16,column=1)
    space3 = tkinter.Label(adminWindow, text="").grid(row=17,column=1)
    logoutBtn = tkinter.Button(adminWindow, text="LOGOUT", width=20, height=1, bg="#ff9999", command = lambda: logOut(adminWindow,currentUser))
    logoutBtn.grid(row=18,column=1)
    adminWindow.mainloop()

def newArtistView(currentUser):
    global newArtistName
    newArtistWindow = tkinter.Tk()
    newArtistWindow.geometry("650x400")
    newArtistWindow.title("Enter New Artist")
    space00 = tkinter.Label(newArtistWindow, text="")
    space00.pack()
    windowTitle = tkinter.Label(newArtistWindow, text="Enter New Artist")
    windowTitle.config(font=("Helvetica",25,"bold"))
    windowTitle.pack()
    space0 = tkinter.Label(newArtistWindow, text="")
    space0.pack()
    Instruction1 = tkinter.Label(newArtistWindow, text="Enter Artist name")
    Instruction1.config(font=("Helvetica",15,"bold"))
    Instruction1.pack()
    newArtistName = tkinter.Entry(newArtistWindow, font="Helvetica 20")
    newArtistName.pack()
    space1 = tkinter.Label(newArtistWindow, text="")
    space1.pack()
    enterArtistBtn = tkinter.Button(newArtistWindow,text="Enter Artist",bg="#c8c8c8",padx=20,pady=10, command = lambda: insertNewArtist(currentUser))
    enterArtistBtn.pack()
    space2 = tkinter.Label(newArtistWindow, text="")
    space2.pack()
    backArtistBtn = tkinter.Button(newArtistWindow,text="Back",bg="#c8c8c8",padx=20,pady=10)
    backArtistBtn.pack()
    newArtistWindow.mainloop()

def newAlbumView(currentUser):
    global albumTitle, albumArtistName
    newAlbumWindow = tkinter.Tk()
    newAlbumWindow.geometry("650x550")
    newAlbumWindow.title("Enter New Album")
    space00 = tkinter.Label(newAlbumWindow, text="")
    space00.pack()
    windowTitle = tkinter.Label(newAlbumWindow, text="Enter new Album")
    windowTitle.config(font=("Helvetica",25,"bold"))
    windowTitle.pack()
    space0 = tkinter.Label(newAlbumWindow, text="")
    space0.pack()
    Instruction1 = tkinter.Label(newAlbumWindow, text="Enter Album name")
    Instruction1.config(font=("Helvetica",15,"bold"))
    Instruction1.pack()
    albumTitle = tkinter.Entry(newAlbumWindow, font="Helvetica 20")
    albumTitle.pack()
    space1 = tkinter.Label(newAlbumWindow, text="")
    space1.pack()
    Instruction2 = tkinter.Label(newAlbumWindow, text="Enter Artist name")
    Instruction2.config(font=("Helvetica",15,"bold"))
    Instruction2.pack()
    albumArtistName = tkinter.Entry(newAlbumWindow, font="Helvetica 20")
    albumArtistName.pack()
    space2 = tkinter.Label(newAlbumWindow, text="")
    space2.pack()
    enterAlbumBtn = tkinter.Button(newAlbumWindow,text="Enter Album",bg="#c8c8c8",padx=20,pady=10, command = lambda: insertNewAlbum(currentUser))
    enterAlbumBtn.pack()
    space3 = tkinter.Label(newAlbumWindow, text="")
    space3.pack()
    backAlbumBtn = tkinter.Button(newAlbumWindow,text="Back",bg="#c8c8c8",padx=20,pady=10)
    backAlbumBtn.pack()
    newAlbumWindow.mainloop()

def newSongView(currentUser):
    global newSongTitle, newSongAlbumName, newSongMediaType, newSongGenre, newSongComposer, newSongMilliseconds, newSongBytes, newSongPrice
    newSongWindow = tkinter.Tk()
    newSongWindow.geometry("650x950")
    newSongWindow.title("Enter New Song")
    space00 = tkinter.Label(newSongWindow, text="")
    space00.pack()
    windowTitle = tkinter.Label(newSongWindow, text="Enter new Song")
    windowTitle.config(font=("Helvetica",22,"bold"))
    windowTitle.pack()
    space0 = tkinter.Label(newSongWindow, text="")
    space0.pack()
    Instruction1 = tkinter.Label(newSongWindow, text="Enter Song Name")
    Instruction1.config(font=("Helvetica",13,"bold"))
    Instruction1.pack()
    newSongTitle = tkinter.Entry(newSongWindow, font="Helvetica 13")
    newSongTitle.pack()
    space1 = tkinter.Label(newSongWindow, text="")
    space1.pack()
    Instruction2 = tkinter.Label(newSongWindow, text="Enter Album Name")
    Instruction2.config(font=("Helvetica",13,"bold"))
    Instruction2.pack()
    newSongAlbumName = tkinter.Entry(newSongWindow, font="Helvetica 13")
    newSongAlbumName.pack()
    space2 = tkinter.Label(newSongWindow, text="")
    space2.pack()
    Instruction3 = tkinter.Label(newSongWindow, text="Enter Media Type")
    Instruction3.config(font=("Helvetica",13,"bold"))
    Instruction3.pack()
    newSongMediaType = tkinter.Entry(newSongWindow, font="Helvetica 13")
    newSongMediaType.pack()
    space3 = tkinter.Label(newSongWindow, text="")
    space3.pack()
    Instruction4 = tkinter.Label(newSongWindow, text="Enter Genre")
    Instruction4.config(font=("Helvetica",13,"bold"))
    Instruction4.pack()
    newSongGenre = tkinter.Entry(newSongWindow, font="Helvetica 13")
    newSongGenre.pack()
    space4 = tkinter.Label(newSongWindow, text="")
    space4.pack()
    Instruction5 = tkinter.Label(newSongWindow, text="Enter Composer")
    Instruction5.config(font=("Helvetica",13,"bold"))
    Instruction5.pack()
    newSongComposer = tkinter.Entry(newSongWindow, font="Helvetica 13")
    newSongComposer.pack()
    space5 = tkinter.Label(newSongWindow, text="")
    space5.pack()
    Instruction6 = tkinter.Label(newSongWindow, text="Enter Milliseconds")
    Instruction6.config(font=("Helvetica",13,"bold"))
    Instruction6.pack()
    newSongMilliseconds = tkinter.Entry(newSongWindow, font="Helvetica 13")
    newSongMilliseconds.pack()
    space6 = tkinter.Label(newSongWindow, text="")
    space6.pack()
    Instruction7 = tkinter.Label(newSongWindow, text="Enter Bytes")
    Instruction7.config(font=("Helvetica",13,"bold"))
    Instruction7.pack()
    newSongBytes = tkinter.Entry(newSongWindow, font="Helvetica 13")
    newSongBytes.pack()
    space7 = tkinter.Label(newSongWindow, text="")
    space7.pack()
    Instruction8 = tkinter.Label(newSongWindow, text="Enter Song Price")
    Instruction8.config(font=("Helvetica",13,"bold"))
    Instruction8.pack()
    newSongPrice = tkinter.Entry(newSongWindow, font="Helvetica 13")
    newSongPrice.pack()
    space8 = tkinter.Label(newSongWindow, text="")
    space8.pack()
    enterArtistBtn = tkinter.Button(newSongWindow,text="Enter Song",bg="#c8c8c8",padx=20,pady=10, command = lambda: insertNewSong(currentUser))
    enterArtistBtn.pack()
    space10 = tkinter.Label(newSongWindow, text="")
    space10.pack()
    backSongBtn = tkinter.Button(newSongWindow,text="Back",bg="#c8c8c8",padx=20,pady=10)
    backSongBtn.pack()
    newSongWindow.mainloop()

def modifyArtistView(currentUser):
    global oldArtistName, upArtistName
    mdArtistWindow = tkinter.Tk()
    for i in range(7):
        mdArtistWindow.columnconfigure(i,weight=1)
    mdArtistWindow.geometry("850x400")
    mdArtistWindow.title("Modify Artist")
    space00 = tkinter.Label(mdArtistWindow, text=" ").grid(row=0,column=5)
    titleReg = tkinter.Label(mdArtistWindow, text="Modify Artist")
    titleReg.grid(row=2,column=3)
    titleReg.config(font=("Steamer",22,"bold"))
    space0 = tkinter.Label(mdArtistWindow, text=" ").grid(row=4,column=3)
    Instructions = tkinter.Label(mdArtistWindow, text="Old Artist Name")
    Instructions.grid(row=6,column=2)
    Instructions.config(font=("Helvetica", 18))
    oldArtistName = tkinter.Entry(mdArtistWindow, font="Helvetica 11")
    oldArtistName.grid(row=7,column=2)
    Instructions1 = tkinter.Label(mdArtistWindow, text="New Artist Name")
    Instructions1.grid(row=6,column=4)
    Instructions1.config(font=("Helvetica", 18))
    upArtistName = tkinter.Entry(mdArtistWindow, font="Helvetica 11")
    upArtistName.grid(row=7,column=4)
    space2 = tkinter.Label(mdArtistWindow, text="").grid(row=8,column=2)
    updateArtistBtn = tkinter.Button(mdArtistWindow, text="Update Artist", padx=15, pady=5, bg="#c8c8c8", command = lambda: modifyArtist(currentUser))
    updateArtistBtn.grid(row=9,column=3)
    space3 = tkinter.Label(mdArtistWindow, text="").grid(row=10,column=3)
    backModifyBtn = tkinter.Button(mdArtistWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: loginView(currentUser))
    backModifyBtn.grid(row=11,column=3)
    mdArtistWindow.mainloop()

def modifyAlbumView(currentUser):
    global oldAlbumName, upAlbumName, upAlbumArtist
    mdAlbumWindow = tkinter.Tk()
    for i in range(7):
        mdAlbumWindow.columnconfigure(i,weight=1)
    mdAlbumWindow.geometry("850x500")
    mdAlbumWindow.title("Modify Album")
    space00 = tkinter.Label(mdAlbumWindow, text=" ").grid(row=0,column=5)
    titleReg = tkinter.Label(mdAlbumWindow, text="Modify Album")
    titleReg.grid(row=2,column=3)
    titleReg.config(font=("Steamer",22,"bold"))
    space0 = tkinter.Label(mdAlbumWindow, text=" ").grid(row=4,column=3)
    Instructions = tkinter.Label(mdAlbumWindow, text="Old Album Name")
    Instructions.grid(row=6,column=2)
    Instructions.config(font=("Helvetica", 18))
    oldAlbumName = tkinter.Entry(mdAlbumWindow, font="Helvetica 11")
    oldAlbumName.grid(row=7,column=2)
    Instructions2 = tkinter.Label(mdAlbumWindow, text="New Album Name")
    Instructions2.grid(row=6,column=4)
    Instructions2.config(font=("Helvetica", 18))
    upAlbumName = tkinter.Entry(mdAlbumWindow, font="Helvetica 11")
    upAlbumName.grid(row=7,column=4)
    space1 = tkinter.Label(mdAlbumWindow, text=" ").grid(row=8,column=4)
    Instructions3 = tkinter.Label(mdAlbumWindow, text="New Artist Name")
    Instructions3.grid(row=9,column=4)
    Instructions3.config(font=("Helvetica", 18))
    upAlbumArtist = tkinter.Entry(mdAlbumWindow, font="Helvetica 11")
    upAlbumArtist.grid(row=10,column=4)
    space2 = tkinter.Label(mdAlbumWindow, text="").grid(row=11,column=2)
    updateAlbumBtn = tkinter.Button(mdAlbumWindow, text="Update Album", padx=15, pady=5, bg="#c8c8c8", command = lambda: modifyAlbum(currentUser))
    updateAlbumBtn.grid(row=12,column=3)
    space3 = tkinter.Label(mdAlbumWindow, text="").grid(row=13,column=3)
    backModifyBtn = tkinter.Button(mdAlbumWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: loginView(con))
    backModifyBtn.grid(row=14,column=3)
    mdAlbumWindow.mainloop()

def modifySongView(currentUser):
    mdSongWindow = tkinter.Tk()
    for i in range(7):
        mdSongWindow.columnconfigure(i,weight=1)
    mdSongWindow.geometry("850x950")
    mdSongWindow.title("Modify Song")
    space00 = tkinter.Label(mdSongWindow, text=" ").grid(row=0,column=5)
    titleReg = tkinter.Label(mdSongWindow, text="Modify Song")
    titleReg.grid(row=2,column=3)
    titleReg.config(font=("Steamer",20,"bold"))
    space0 = tkinter.Label(mdSongWindow, text=" ").grid(row=4,column=3)
    Instructions = tkinter.Label(mdSongWindow, text="Old Song Name")
    Instructions.grid(row=6,column=2)
    Instructions.config(font=("Helvetica", 14))
    oldSongName = tkinter.Entry(mdSongWindow, font="Helvetica 11")
    oldSongName.grid(row=7,column=2)
    Instructions2 = tkinter.Label(mdSongWindow, text="New Song Name")
    Instructions2.grid(row=6,column=4)
    Instructions2.config(font=("Helvetica", 14))
    upSongName = tkinter.Entry(mdSongWindow, font="Helvetica 11")
    upSongName.grid(row=7,column=4)
    space1 = tkinter.Label(mdSongWindow, text=" ").grid(row=8,column=4)
    Instructions3 = tkinter.Label(mdSongWindow, text="New Album Name")
    Instructions3.grid(row=9,column=4)
    Instructions3.config(font=("Helvetica", 14))
    upSongAlbum = tkinter.Entry(mdSongWindow, font="Helvetica 11")
    upSongAlbum.grid(row=10,column=4)
    space2 = tkinter.Label(mdSongWindow, text=" ").grid(row=11,column=4)
    Instructions4 = tkinter.Label(mdSongWindow, text="New Media Type")
    Instructions4.grid(row=12,column=4)
    Instructions4.config(font=("Helvetica", 14))
    upSongMediaType = tkinter.Entry(mdSongWindow, font="Helvetica 11")
    upSongMediaType.grid(row=13,column=4)
    space3 = tkinter.Label(mdSongWindow, text=" ").grid(row=14,column=4)
    Instructions5 = tkinter.Label(mdSongWindow, text="New Genre Name")
    Instructions5.grid(row=15,column=4)
    Instructions5.config(font=("Helvetica", 14))
    upSongGenre = tkinter.Entry(mdSongWindow, font="Helvetica 11")
    upSongGenre.grid(row=16,column=4)
    space4 = tkinter.Label(mdSongWindow, text=" ").grid(row=17,column=4)
    Instructions6 = tkinter.Label(mdSongWindow, text="New Composer")
    Instructions6.grid(row=18,column=4)
    Instructions6.config(font=("Helvetica", 14))
    upSongComposer = tkinter.Entry(mdSongWindow, font="Helvetica 11")
    upSongComposer.grid(row=19,column=4)
    space5 = tkinter.Label(mdSongWindow, text=" ").grid(row=20,column=4)
    Instructions7 = tkinter.Label(mdSongWindow, text="New Milliseconds")
    Instructions7.grid(row=21,column=4)
    Instructions7.config(font=("Helvetica", 14))
    upSongMilliseconds = tkinter.Entry(mdSongWindow, font="Helvetica 11")
    upSongMilliseconds.grid(row=22,column=4)
    space6 = tkinter.Label(mdSongWindow, text=" ").grid(row=23,column=4)
    Instructions8 = tkinter.Label(mdSongWindow, text="New Bytes")
    Instructions8.grid(row=24,column=4)
    Instructions8.config(font=("Helvetica", 14))
    upSongBytes = tkinter.Entry(mdSongWindow, font="Helvetica 11")
    upSongBytes.grid(row=25,column=4)
    space7 = tkinter.Label(mdSongWindow, text=" ").grid(row=26,column=4)
    Instructions9 = tkinter.Label(mdSongWindow, text="New Unit Price")
    Instructions9.grid(row=27,column=4)
    Instructions9.config(font=("Helvetica", 14))
    upSongBytes = tkinter.Entry(mdSongWindow, font="Helvetica 11")
    upSongBytes.grid(row=28,column=4)
    space2 = tkinter.Label(mdSongWindow, text="").grid(row=29,column=2)
    updateAlbumBtn = tkinter.Button(mdSongWindow, text="Update Song", padx=15, pady=5, bg="#c8c8c8")
    updateAlbumBtn.grid(row=30,column=3)
    space3 = tkinter.Label(mdSongWindow, text="").grid(row=31,column=3)
    backModifyBtn = tkinter.Button(mdSongWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: loginView(con))
    backModifyBtn.grid(row=32,column=3)
    mdSongWindow.mainloop()

def removeArtistView(currentUser):
    removeArtistWindow = tkinter.Tk()
    removeArtistWindow.geometry("650x400")
    removeArtistWindow.title("Remove Artist")
    space00 = tkinter.Label(removeArtistWindow, text="")
    space00.pack()
    windowTitle = tkinter.Label(removeArtistWindow, text="Remove Artist")
    windowTitle.config(font=("Helvetica",25,"bold"))
    windowTitle.pack()
    space0 = tkinter.Label(removeArtistWindow, text="")
    space0.pack()
    Instruction1 = tkinter.Label(removeArtistWindow, text="Enter Artist Name")
    Instruction1.config(font=("Helvetica",15,"bold"))
    Instruction1.pack()
    removeArtistName = tkinter.Entry(removeArtistWindow, font="Helvetica 20")
    removeArtistName.pack()
    space1 = tkinter.Label(removeArtistWindow, text="")
    space1.pack()
    enterArtistBtn = tkinter.Button(removeArtistWindow,text="Remove Artist",bg="#c8c8c8",padx=20,pady=10)
    enterArtistBtn.pack()
    space2 = tkinter.Label(removeArtistWindow, text="")
    space2.pack()
    backArtistBtn = tkinter.Button(removeArtistWindow,text="Back",bg="#c8c8c8",padx=20,pady=10)
    backArtistBtn.pack()
    removeArtistWindow.mainloop()
    removeArtistWindow.mainloop()

def removeAlbumView(currentUser):
    removeAlbumWindow = tkinter.Tk()
    removeAlbumWindow.geometry("650x550")
    removeAlbumWindow.title("Remove Album")
    space00 = tkinter.Label(removeAlbumWindow, text="")
    space00.pack()
    windowTitle = tkinter.Label(removeAlbumWindow, text="Remove Album")
    windowTitle.config(font=("Helvetica",25,"bold"))
    windowTitle.pack()
    space0 = tkinter.Label(removeAlbumWindow, text="")
    space0.pack()
    Instruction1 = tkinter.Label(removeAlbumWindow, text="Enter Album name")
    Instruction1.config(font=("Helvetica",15,"bold"))
    Instruction1.pack()
    rmalbumTitle = tkinter.Entry(removeAlbumWindow, font="Helvetica 20")
    rmalbumTitle.pack()
    space1 = tkinter.Label(removeAlbumWindow, text="")
    space1.pack()
    Instruction2 = tkinter.Label(removeAlbumWindow, text="Enter Artist name")
    Instruction2.config(font=("Helvetica",15,"bold"))
    Instruction2.pack()
    rmalbumArtistName = tkinter.Entry(removeAlbumWindow, font="Helvetica 20")
    rmalbumArtistName.pack()
    space2 = tkinter.Label(removeAlbumWindow, text="")
    space2.pack()
    removeAlbumBtn = tkinter.Button(removeAlbumWindow,text="Remove Album",bg="#c8c8c8",padx=20,pady=10)
    removeAlbumBtn.pack()
    space3 = tkinter.Label(removeAlbumWindow, text="")
    space3.pack()
    backAlbumBtn = tkinter.Button(removeAlbumWindow,text="Back",bg="#c8c8c8",padx=20,pady=10)
    backAlbumBtn.pack()
    removeAlbumWindow.mainloop()

def removeSongView(currentUser):
    removeSongWindow = tkinter.Tk()
    removeSongWindow.geometry("650x600")
    removeSongWindow.title("Remove Song")
    space00 = tkinter.Label(removeSongWindow, text="")
    space00.pack()
    windowTitle = tkinter.Label(removeSongWindow, text="Remove Song")
    windowTitle.config(font=("Helvetica",25,"bold"))
    windowTitle.pack()
    space0 = tkinter.Label(removeSongWindow, text="")
    space0.pack()
    Instruction1 = tkinter.Label(removeSongWindow, text="Enter Song Name")
    Instruction1.config(font=("Helvetica",15,"bold"))
    Instruction1.pack()
    rmsgSongTitle = tkinter.Entry(removeSongWindow, font="Helvetica 20")
    rmsgSongTitle.pack()
    space1 = tkinter.Label(removeSongWindow, text="")
    space1.pack()
    Instruction2 = tkinter.Label(removeSongWindow, text="Enter Album Name")
    Instruction2.config(font=("Helvetica",15,"bold"))
    Instruction2.pack()
    rmsgAlbumTitle = tkinter.Entry(removeSongWindow, font="Helvetica 20")
    rmsgAlbumTitle.pack()
    space2 = tkinter.Label(removeSongWindow, text="")
    space2.pack()
    Instruction3 = tkinter.Label(removeSongWindow, text="Enter Composer")
    Instruction3.config(font=("Helvetica",15,"bold"))
    Instruction3.pack()
    rmsgComposer = tkinter.Entry(removeSongWindow, font="Helvetica 20")
    rmsgComposer.pack()
    space3 = tkinter.Label(removeSongWindow, text="")
    space3.pack()
    removeSongBtn = tkinter.Button(removeSongWindow,text="Remove Song",bg="#c8c8c8",padx=20,pady=10)
    removeSongBtn.pack()
    space3 = tkinter.Label(removeSongWindow, text="")
    space3.pack()
    backRemoveSongBtn = tkinter.Button(removeSongWindow,text="Back",bg="#c8c8c8",padx=20,pady=10)
    backRemoveSongBtn.pack()
    removeSongWindow.mainloop()

def deactivateSongView(currentUser):
    global deactivateSongTitle, deactivateSongComposer
    deactivateWindow = tkinter.Tk()
    deactivateWindow.geometry("650x550")
    deactivateWindow.title("Deactivate Song")
    space00 = tkinter.Label(deactivateWindow, text="")
    space00.pack()
    windowTitle = tkinter.Label(deactivateWindow, text="Deactivate Song")
    windowTitle.config(font=("Helvetica",25,"bold"))
    windowTitle.pack()
    space0 = tkinter.Label(deactivateWindow, text="")
    space0.pack()
    Instruction1 = tkinter.Label(deactivateWindow, text="Enter Song Name")
    Instruction1.config(font=("Helvetica",15,"bold"))
    Instruction1.pack()
    deactivateSongTitle = tkinter.Entry(deactivateWindow, font="Helvetica 20")
    deactivateSongTitle.pack()
    space1 = tkinter.Label(deactivateWindow, text="")
    space1.pack()
    Instruction2 = tkinter.Label(deactivateWindow, text="Enter Song Composer")
    Instruction2.config(font=("Helvetica",15,"bold"))
    Instruction2.pack()
    deactivateSongComposer = tkinter.Entry(deactivateWindow, font="Helvetica 20")
    deactivateSongComposer.pack()
    space2 = tkinter.Label(deactivateWindow, text="")
    space2.pack()
    deactivateSongBtn = tkinter.Button(deactivateWindow,text="Deactivate Song",bg="#c8c8c8",padx=20,pady=10, command = lambda: songDeactivation(currentUser))
    deactivateSongBtn.pack()
    space3 = tkinter.Label(deactivateWindow, text="")
    space3.pack()
    backDeactivateBtn = tkinter.Button(deactivateWindow,text="Back",bg="#c8c8c8",padx=20,pady=10)
    backDeactivateBtn.pack()
    deactivateWindow.mainloop()

def activateSongView(currentUser):
    global activateSongTitle, activateSongComposer
    activateWindow = tkinter.Tk()
    activateWindow.geometry("650x550")
    activateWindow.title("Activate Song")
    space00 = tkinter.Label(activateWindow, text="")
    space00.pack()
    windowTitle = tkinter.Label(activateWindow, text="Activate Song")
    windowTitle.config(font=("Helvetica",25,"bold"))
    windowTitle.pack()
    space0 = tkinter.Label(activateWindow, text="")
    space0.pack()
    Instruction1 = tkinter.Label(activateWindow, text="Enter Song Name")
    Instruction1.config(font=("Helvetica",15,"bold"))
    Instruction1.pack()
    activateSongTitle = tkinter.Entry(activateWindow, font="Helvetica 20")
    activateSongTitle.pack()
    space1 = tkinter.Label(activateWindow, text="")
    space1.pack()
    Instruction2 = tkinter.Label(activateWindow, text="Enter Song Composer")
    Instruction2.config(font=("Helvetica",15,"bold"))
    Instruction2.pack()
    activateSongComposer = tkinter.Entry(activateWindow, font="Helvetica 20")
    activateSongComposer.pack()
    space2 = tkinter.Label(activateWindow, text="")
    space2.pack()
    activateSongBtn = tkinter.Button(activateWindow,text="Activate Song",bg="#c8c8c8",padx=20,pady=10, command = lambda: songActivation(currentUser))
    activateSongBtn.pack()
    space3 = tkinter.Label(activateWindow, text="")
    space3.pack()
    backActivateBtn = tkinter.Button(activateWindow,text="Back",bg="#c8c8c8",padx=20,pady=10)
    backActivateBtn.pack()
    activateWindow.mainloop()

def userPermissionView(currentUser):
    global permissionUsername, permissionNewNumber
    permissionWindow = tkinter.Tk()
    permissionWindow.geometry("650x700")
    permissionWindow.title("Permissions Manager")
    space00 = tkinter.Label(permissionWindow, text="")
    space00.pack()
    windowTitle = tkinter.Label(permissionWindow, text="Permission Manager")
    windowTitle.config(font=("Helvetica",25,"bold"))
    windowTitle.pack()
    space0 = tkinter.Label(permissionWindow, text="")
    space0.pack()
    Instruction1 = tkinter.Label(permissionWindow, text="Enter Username")
    Instruction1.config(font=("Helvetica",15,"bold"))
    Instruction1.pack()
    permissionUsername = tkinter.Entry(permissionWindow, font="Helvetica 20")
    permissionUsername.pack()
    space1 = tkinter.Label(permissionWindow, text="")
    space1.pack()
    Instruction2 = tkinter.Label(permissionWindow, text="Enter User First Name")
    Instruction2.config(font=("Helvetica",15,"bold"))
    Instruction2.pack()
    permissionUserFirst = tkinter.Entry(permissionWindow, font="Helvetica 20")
    permissionUserFirst.pack()
    space2 = tkinter.Label(permissionWindow, text="")
    space2.pack()
    Instruction3 = tkinter.Label(permissionWindow, text="Enter User Last Name")
    Instruction3.config(font=("Helvetica",15,"bold"))
    Instruction3.pack()
    permissionUserLast = tkinter.Entry(permissionWindow, font="Helvetica 20")
    permissionUserLast.pack()
    space3 = tkinter.Label(permissionWindow, text="")
    space3.pack()
    Instruction4 = tkinter.Label(permissionWindow, text="Enter New Permission Number")
    Instruction4.config(font=("Helvetica",15,"bold"))
    Instruction4.pack()
    permissionNewNumber = tkinter.Entry(permissionWindow, font="Helvetica 20")
    permissionNewNumber.pack()
    space4 = tkinter.Label(permissionWindow, text="")
    space4.pack()
    changePermissionBtn = tkinter.Button(permissionWindow,text="Activate Song",bg="#c8c8c8",padx=20,pady=10, command = lambda: changeUserPermission(currentUser))
    changePermissionBtn.pack()
    space3 = tkinter.Label(permissionWindow, text="")
    space3.pack()
    backPermissionBtn = tkinter.Button(permissionWindow,text="Back",bg="#c8c8c8",padx=20,pady=10)
    backPermissionBtn.pack()
    permissionWindow.mainloop()
    
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
