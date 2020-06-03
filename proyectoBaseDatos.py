import tkinter
from tkinter import font
from tkinter import IntVar, StringVar, Entry, OptionMenu, Button, Label
from pymongo import *
import webbrowser
import psycopg2
import random
from datetime import date
import csv
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle
from reportlab.lib import colors

##################################################################################################################
                                        #Funciones para el sistema
##################################################################################################################
def logOut(View,currentUser):
    View.destroy()
    currentUser = {}
    loginView(con)

def backToLogin(View):
    View.destroy()
    loginView(con)

def backToView(View,currentUser):
    View.destroy()
    userType = currentUser['type']
    if userType == 'admin':
        adminView(currentUser)     
    elif userType == 'Tier 1':
        customer1View(currentUser)
    elif userType == 'Tier 2':
        customer2View(currentUser)
    elif userType == 'Tier 3':
        customer3View(currentUser)

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
        cur.close()
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
                print("\n-> Album Registered Succesfully!")
        cur.close()
    except:
        print("\n-> Album Registration Failed!")
        print("-> Try Checking if there is an ARTIST with that Name!")

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
        url = newSongURL.get()
        cur.execute("""SELECT trackid
                FROM track
                ORDER BY trackid DESC
                LIMIT 1""")
        tracksIDs = cur.fetchall()
        lastTrackID = 0
        for trackID in tracksIDs:
            lastTrackID = trackID[0]
            lastTrackID += 1
            print(str(lastTrackID))
        dictionary = {'Title':songAlbum,'Name':songGenre,'MediaName':mediaType}
        cur.execute("""SELECT albumid
                        FROM album
                        WHERE title = %(Title)s""",dictionary)
        albumsIDs = cur.fetchall()
        rightAlbumID = 0
        for albumID in albumsIDs:
            rightAlbumID = albumID[0]
            print(str(rightAlbumID))
        cur.execute("""SELECT genreid
                    FROM genre
                    WHERE name = %(Name)s""",dictionary)
        genresIDs = cur.fetchall()
        rightGenreID = 0
        for genreID in genresIDs:
            rightGenreID = genreID[0]
            print(str(rightGenreID))
        cur.execute("""SELECT mediatypeid
                FROM mediatype
                WHERE name = %(MediaName)s""",dictionary)
        mediaTypesIDs = cur.fetchall()
        rightMediaType = 0
        activa = 1
        for mediaTypeID in mediaTypesIDs:
            rightMediaType = mediaTypeID[0]
            print(str(rightMediaType))
        lastDictionary = {'TrackId':lastTrackID,
                          'Name':songTitle,
                          'AlbumId':rightAlbumID,
                          'MediaTypeId':rightMediaType,
                          'GenreId':rightGenreID,
                          'Composer':songComposer,
                          'Milliseconds':songMilliseconds,
                          'Bytes':songBytes,
                          'UnitPrice':songPrice,
                          'songURL':url,
                          'Activa':activa}
        cur.execute("""INSERT INTO track (TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice, songURL, activa)
                    VALUES (%(TrackId)s,%(Name)s,%(AlbumId)s,%(MediaTypeId)s,%(GenreId)s,%(Composer)s,%(Milliseconds)s,%(Bytes)s,%(UnitPrice)s,%(songURL)s,%(Activa)s)""",lastDictionary)
        con.commit()
        if currentUser['type'] == 'admin':
            print("\n-> Song Registered Succesfully!")
        else:
            cur.execute("""select invoiceid from invoice order by invoiceid desc limit 1;""")
            lastIDS = cur.fetchall()
            lastID = 0
            for lid in lastIDS:
                lastID = lid[0]
                lastID += 1
            userName = currentUser['name']
            userDictionary = {'Username':userName}
            cur.execute("""select customerid, address, city, state, country, postalcode
                        from customer
                        where username = %(Username)s
                        LIMIT 1;""",userDictionary)
            userCredentials = cur.fetchall()
            customerID = 0
            customerAddress = ""
            customerCity = ""
            customerState = ""
            customerCountry = ""
            customerPostalCode = ""
            price = 0.99
            today = date.today()
            for userCredential in userCredentials:
                customerID = userCredential[0]
                customerAddress = userCredential[1]
                customerCity = userCredential[2]
                customerState = userCredential[3]
                customerCountry = userCredential[4]
                customerPostalCode = userCredential[5]
            invoiceDictionary = {'InvoiceID':lastID,
                               'CustomerID':customerID,
                               'InvoiceDate':today,
                               'BillingAddress':customerAddress,
                               'BillingCity':customerCity,
                               'BillingState':customerState,
                               'BillingCountry':customerCountry,
                               'BillingPostalCode':customerPostalCode,
                               'UnitPrice':price}
            cur.execute("""INSERT INTO invoice (invoiceid,customerid,invoicedate,billingaddress,billingcity,billingstate,billingcountry,billingpostalcode,total)
                        VALUES (%(InvoiceID)s,%(CustomerID)s,%(InvoiceDate)s,%(BillingAddress)s,%(BillingCity)s,%(BillingState)s,%(BillingCountry)s,%(BillingPostalCode)s,%(UnitPrice)s);""",invoiceDictionary)
            con.commit()
            cur.execute("""select invoicelineid from invoiceline order by invoicelineid desc limit 1;""")
            invoiceLIDS = cur.fetchall()
            lastILID = 0
            quantity = 1
            for invoiceLID in invoiceLIDS:
                lastILID = invoiceLID[0]
                lastILID += 1
            invoicelineDictionary = {'InvoiceLineID':lastILID,
                                    'InvoiceID':lastID,
                                    'TrackID':lastTrackID,
                                    'UnitPrice':price,
                                    'Quantity':quantity}
            cur.execute("""INSERT INTO invoiceline (invoicelineid,invoiceid,trackid,unitprice,quantity)
                            VALUES (%(InvoiceLineID)s,%(InvoiceID)s,%(TrackID)s,%(UnitPrice)s,%(Quantity)s);""",invoicelineDictionary)
            con.commit()
            print("\n-> Song Registered Succesfully!")
        cur.close()
    except:
        print("\n-> New Song Registration Failed!")
        print("-> Try Checking if there is an ARTIST or an ALBUM with that Name!")

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
        print("\Artist Update Failed!")

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
        ALBUMID = 0
        for albumID in albumIDS:
            ALBUMID = albumID[0]
        cur.execute("""SELECT artistid FROM artist WHERE name = %(ArtistName)s""",dictionary)
        artistsIDs = cur.fetchall()
        for artistID in artistsIDs:
            rightID = artistID[0]
            finalDictionary = {'OldAlbum':oldAlbum,'albumID':lastAlbumID,'NewAlbum':newAlbum,'ArtistID':rightID}
            cur.execute("""UPDATE album
                            SET title = %(NewAlbum)s
                        WHERE title = %(OldAlbum)s""",finalDictionary)
            con.commit()
        print("\n-> Album Updated Succesfully!")
        cur.close()
    except:
        print("\n Album Update Failed!")

def modifySong(currentUser):
    try:
        cur = con.cursor()
        oldSName = oldSongName.get()
        newSongName = upSongName.get()
        newSongAlbum = upSongAlbum.get()
        newSongAlbum = int(newSongAlbum)
        newSongMedia = upSongMediaType.get()
        newSongMedia = int(newSongMedia)
        newSongGenre = upSongGenre.get()
        newSongGenre = int(newSongGenre)
        newSongComposer = upSongComposer.get()
        newSongMilliseconds = upSongMilliseconds.get()
        newSongMilliseconds = int(newSongMilliseconds)
        newSongBytes = upSongBytes.get()
        newSongBytes = int(newSongBytes)
        newSongPrice = upSongPrice.get()
        newSongPrice = float(newSongPrice)
        newSongURL = upSongURL.get()
        dictionary = {'OldSongName':oldSName,
                      'NewSongName':newSongName,
                      'NewSongAlbum':newSongAlbum,
                      'NewSongMedia':newSongMedia,
                      'NewSongGenre':newSongGenre,
                      'NewSongComposer':newSongComposer,
                      'NewSongMilliseconds':newSongMilliseconds,
                      'NewSongBytes':newSongBytes,
                      'NewSongPrice':newSongPrice,
                      'NewSongURL':newSongURL}
        cur.execute("""UPDATE track
                    SET name = %(NewSongName)s,
                        albumid = %(NewSongAlbum)s,
                        mediatypeid = %(NewSongMedia)s,
                        genreid = %(NewSongGenre)s,
                        composer = %(NewSongComposer)s,
                        milliseconds = %(NewSongMilliseconds)s,
                        bytes = %(NewSongBytes)s,
                        unitprice = %(NewSongPrice)s,
                        songurl = %(NewSongURL)s
                    WHERE name = %(OldSongName)s;""",dictionary)
        con.commit()
        cur.close()
        print("\n-> Song Updated Succesfully!")
    except:
        print("\n-> Song Update Failed! Check:")
        print("     1. Album, MediaType or Album are numbers, not letters")
        print("     2. Album, MediaType or Album exist")
        
def removeArtist(currentUser):
    try:        
        cur = con.cursor()
        artistName = removeArtistName.get()
        dictionary = {'Name':artistName}
        cur.execute("""DELETE FROM artist
                    WHERE name = %(Name)s""",dictionary)
        con.commit()
        cur.close()
        print("\n-> Artist removed Succesfully!")
    except:
        print("\n-> Artist removal Failed!")
        print("-> Try removing all artist albums first...")

def removeAlbum(currentUser):
    try:
        cur = con.cursor()
        albumTitle = rmalbumTitle.get()
        artistName = rmalbumArtistName.get()
        dictionary1 = {'Name':artistName}
        cur.execute("""SELECT artistid
                        FROM artist
                        WHERE name = %(Name)s
                        LIMIT 1;""",dictionary1)
        rows = cur.fetchall()
        for r in rows:
            artistid = r[0]
            if r[0] == None:
                print("-> Artist not found!")
            else:
                
                dictionary2 = {'Title':albumTitle,'ArtistID':artistid}
                cur.execute("""DELETE FROM album
                            WHERE title = %(Title)s AND artistid = %(ArtistID)s""",dictionary2)
                con.commit()
                cur.close()
                print("\n-> Album Removed Succesfully!")
    except:
        print("\n-> Album Removal Failed!")

def removeSong(currentUser):
    try:
        cur = con.cursor()
        songTitle = rmsgSongTitle.get()
        composer = rmsgComposer.get()
        dictionary1 = {'Name':songTitle,'Composer':composer}
        cur.execute("""SELECT trackid
                    FROM track
                    WHERE name = %(Name)s AND composer = %(Composer)s;""",dictionary1)
        rows = cur.fetchall()
        if rows == None:
            print("\n-> No Song found with Those Credentials!")
        else:
            for r in rows:
                songID = r[0]
                dictionary2 = {'TrackID':songID,'Name':songTitle}
                cur.execute("""DELETE FROM playlisttrack
                            WHERE trackid = %(TrackID)s;""",dictionary2)
                con.commit()
                cur.execute("""DELETE FROM track
                            WHERE trackid = %(TrackID)s AND name = %(Name)s;""",dictionary2)
                con.commit()
                cur.close()
                print("\n-> Song Removed Succesfully!")
    except:
        print("\n-> Song Removal Failed!")

def songDeactivation(currentUser):
    try:
        cur = con.cursor()
        songTitle = deactivateSongTitle.get()
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
        cur.close()
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
            elif newPer > 3:
                print("\n-> Please enter a permission between 1 and 3!")
            else:                
                cur.execute("""UPDATE customer
                        SET rol = %(rol)s
                        WHERE username = %(username)s""",dictionary)
                con.commit()
                print("\n-> Customer Permission Updated!")
        cur.close()
    except:
        print("\n-> User Permission Failed!")

def listenAdminSongsFunction(currentUser):
    try:
        cur = con.cursor()
        message = "\n-> Song not found, please try again!"
        songName = listenSongName2.get()
        dictionary = {'Name':songName}
        cur.execute("""SELECT songURL, trackid
                    from track
                    where name = %(Name)s
                    limit 1;""",dictionary)
        rows = cur.fetchall()
        for r in rows:
            rightSongPlayingID = 0
            rightTrackID = r[1]
            amount = 1
            cur.execute("""SELECT songplayingid
                        FROM songplayings
                        ORDER BY songplayingid desc
                        LIMIT 1""")
            songsIDS = cur.fetchall()
            for songID in songsIDS:
                rightSongPlayingID = songID[0]
                rightSongPlayingID += 1
            dictionary2 = {'SongPlayingID':rightSongPlayingID,
                           'TrackID':rightTrackID,
                           'Playing':amount}
            cur.execute("""INSERT INTO songplayings (songplayingid, trackid, playing)
                        VALUES (%(SongPlayingID)s,%(TrackID)s,%(Playing)s);""",dictionary2)
            con.commit()
            new=2
            url=r[0]
            webbrowser.open(url,new=new)
            message = "\n-> Playing song..."
        print(message)
        cur.close()
    except:
        print("-> Song Playback Failed!")

def listenCustomerSongsFunction(currentUser):
    try:
        cur = con.cursor()
        message = "\n-> Song not found on user or is DEACTIVATED!"
        username = currentUser['name']
        userType = currentUser['type']
        songTitle = listenSongName.get()
        dictionary1 = {'username':username}
        cur.execute("""select customerid
                    from customer 
                    where Username = %(username)s 
                    limit 1;""",dictionary1)
        rows1 = cur.fetchall()
        customerID = 0
        for r in rows1:
            customerID = r[0]
        dictionary2 = {'customerID':customerID}
        cur.execute("""SELECT track.name, track.songURL, trackid
                from (select invoiceline.invoiceid as INVOICELINEID, invoiceline.trackid as INVOICELINETRACKID
                from invoiceline) mid
                left join track on track.trackid = mid.INVOICELINETRACKID
                left join invoice on invoice.invoiceid = mid.INVOICELINEID
                where invoice.customerid = %(customerID)s and track.activa = 1;""",dictionary2)
        rows = cur.fetchall()
        for r in rows:
            if songTitle == r[0]:
                rightSongPlayingID = 0
                rightTrackID = r[2]
                amount = 1
                cur.execute("""SELECT songplayingid
                            FROM songplayings
                            ORDER BY songplayingid desc
                            LIMIT 1""")
                songsIDS = cur.fetchall()
                for songID in songsIDS:
                    rightSongPlayingID = songID[0]
                    rightSongPlayingID += 1
                dictionary2 = {'SongPlayingID':rightSongPlayingID,
                               'TrackID':rightTrackID,
                               'Playing':amount}
                cur.execute("""INSERT INTO songplayings (songplayingid, trackid, playing)
                            VALUES (%(SongPlayingID)s,%(TrackID)s,%(Playing)s);""",dictionary2)
                con.commit()
                new=2
                url=r[1]
                webbrowser.open(url,new=new)
                message = "\n-> Playing song..."
        print(message)
        cur.close()
    except:
        print("\n-> Song not found! Problem because:")
        print("    1. Song is typed incorrectly")
        print("    2. Song does not have a URL")

def addSongToWishlist(currentUser,wishlist):

    cur = con.cursor()
    songName = purchaseSongName.get()
    dictionary = {'Name':songName}
    cur.execute("""select name from track where name = %(Name)s limit 1;""",dictionary)
    rows = cur.fetchall()
    for r in rows:
        wishlist.append(r[0])
    print("\n-> Song added to Wishlist!")
    print("-> There are now " + str(len(wishlist)) + " items in your wishlist!")
    cur.close()
    #except:
        #print("\n-> No song with that name!")

def songPayment(currentUser,wishlist,totalprice):
    try:
        cur = con.cursor()
        songsList = []
        cur.execute("""select invoiceid from invoice order by invoiceid desc limit 1;""")
        lastIDS = cur.fetchall()
        lastID = 0
        for lid in lastIDS:
            lastID = lid[0]
            lastID += 1
        userName = currentUser['name']
        userDictionary = {'Username':userName}
        cur.execute("""select customerid, address, city, state, country, postalcode
                    from customer
                    where username = %(Username)s
                    LIMIT 1;""",userDictionary)
        userCredential = cur.fetchall()
        customerID = 0
        customerAddress = ""
        customerCity = ""
        customerState = ""
        customerCountry = ""
        customerPostalCode = ""
        price = totalprice
        today = date.today()
        for userCredential in userCredential:
            customerID = userCredential[0]
            customerAddress = userCredential[1]
            customerCity = userCredential[2]
            customerState = userCredential[3]
            customerCountry = userCredential[4]
            customerPostalCode = userCredential[5]
        invoiceDictionary = {'InvoiceID':lastID,
                           'CustomerID':customerID,
                           'InvoiceDate':today,
                           'BillingAddress':customerAddress,
                           'BillingCity':customerCity,
                           'BillingState':customerState,
                           'BillingCountry':customerCountry,
                           'BillingPostalCode':customerPostalCode,
                           'UnitPrice':price}
        cur.execute("""INSERT INTO invoice (invoiceid,customerid,invoicedate,billingaddress,billingcity,billingstate,billingcountry,billingpostalcode,total)
                   VALUES (%(InvoiceID)s,%(CustomerID)s,%(InvoiceDate)s,%(BillingAddress)s,%(BillingCity)s,%(BillingState)s,%(BillingCountry)s,%(BillingPostalCode)s,%(UnitPrice)s);""",invoiceDictionary)
        con.commit()
        for song in wishlist:
            cur.execute("""select invoicelineid from invoiceline order by invoicelineid desc limit 1;""")
            invoiceLIDS = cur.fetchall()
            lastILID = 0
            quantity = 1
            for invoiceLID in invoiceLIDS:
                lastILID = invoiceLID[0]
                lastILID += 1
            rightTrackID = 0
            songName = song
            songDictionary = {'SongName':songName}
            cur.execute("""SELECT trackid
                    FROM track
                    where name = %(SongName)s
                    LIMIT 1""",songDictionary)
            tracksIDs = cur.fetchall()
            price = 0.99
            quantity = 1
            for trackID in tracksIDs:
                rightTrackID = trackID[0]
            invoicelineDictionary = {'InvoiceLineID':lastILID,
                                    'InvoiceID':lastID,
                                    'TrackID':rightTrackID,
                                    'UnitPrice':price,
                                    'Quantity':quantity}
            cur.execute("""INSERT INTO invoiceline (invoicelineid,invoiceid,trackid,unitprice,quantity)
                            VALUES (%(InvoiceLineID)s,%(InvoiceID)s,%(TrackID)s,%(UnitPrice)s,%(Quantity)s);""",invoicelineDictionary)
            con.commit()
            songsList.append(invoicelineDictionary)
        print("\n-> Songs Purchase Succesfully!")
        csvGenerator(currentUser,songsList,totalprice)
        print("\n-> CSV File Generated Succesfully!")
        pdfGenerator(currentUser,songsList,totalprice)
        print("\n-> PDF File Generated Succesfully!")
        cur.close()
    except:
        print("\n-> Song purchase Failed!")

def csvGenerator(currentUser,songsList,totalprice):
    try:
        cur = con.cursor()
        client = currentUser['name']
        with open(client+'.csv', 'w', newline='') as f:
            fieldnames = ['invoiceLineID','invoiceID','TrackID','UnitPrice','Quantity']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for song in songsList:
                songILID = song['InvoiceLineID']
                songIID = song['InvoiceID']
                songID = song['TrackID']
                songPrice = song['UnitPrice']
                songQuantity = song['Quantity']
                writer.writerow({'invoiceLineID':songILID,
                                 'invoiceID':songIID,
                                 'TrackID':songID,
                                 'UnitPrice':songPrice,
                                 'Quantity':songQuantity})
        cur.close()
    except:
        print("\n-> CSV File Generation Failed!")

def pdfGenerator(currentUser,songsList,totalprice):
    try:
        cur = con.cursor()
        client = currentUser['name']
        length = len(songsList) + 1
        pdf = SimpleDocTemplate("PurchaseCertification-"+client+".pdf")
        flow_obj = []
        with open(client+'.csv') as f1:
            csvdata = csv.reader(f1,delimiter=",")
            tdata = []
            for row in csvdata:
                data = []
                songInvoiceLineID = row[0]
                songInvoiceID = row[1]
                songID = row[2]
                songPrice = row[3]
                songQuantity = row[4]
                data.append(songInvoiceLineID)
                data.append(songInvoiceID)
                data.append(songID)
                data.append(songPrice)
                data.append(songQuantity)
                tdata.append(data)
        t = Table(tdata)
        tstyle = TableStyle([("GRID",(0,0),(-1,-1),1,colors.black),
                             ("BOX",(0,0),(-1,-5),1,colors.black),
                             ("BACKGROUND",(0,0),(-1,-length),colors.grey)])
        t.setStyle(tstyle)
        flow_obj.append(t)
        pdf.build(flow_obj)
        cur.close()
    except:
        print("\n-> PDF File Generation Failed!")

def searchClients(currentUser):
    try:
        cur = con.cursor()
        date = searchByDate.get()
        dictionary = {'Date':date}
        cur.execute("""select invoice.customerid, invoice.invoicedate, invoiceline.trackid
            from invoiceline
            left join invoice on invoice.invoiceid = invoiceline.invoiceid
            where invoice.invoicedate = %(Date)s;""",dictionary)
        clients = cur.fetchall()
        collectionName = 'clients-'+date[:4]
        collection = db[collectionName]
        for client in clients:
            clien = db.collection.insert_one({"ClientID":client[0],"InvoiceDate":client[1],"TrackID":client[2]})
        cur.close()
        print("\n-> MongoDB Updated Succesfully!")
    except:
        print("\n-> MongoDB Update Unsuccessful!")

def exportArtistSellingsCSV(rows,currentUser):
    try:
        cur = con.cursor()
        with open('ArtistSellings.csv', 'w', newline='') as f:
                fieldnames = ['Artist','Sum']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for r in rows:
                    artist = r[0]
                    sumatory = r[1]
                    writer.writerow({'Artist':artist,
                                     'Sum':sumatory})
        cur.close()
        print("\n-> CSV Generation Successfully!")
    except:
        print("\n-> CSV Generation Failed!")

def exportGenreSellingsCSV(rows,currentUser):
    try:
        cur = con.cursor()
        with open('GenreSellings.csv', 'w', newline='') as f:
                fieldnames = ['Genre','Sum']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for r in rows:
                    artist = r[0]
                    sumatory = r[1]
                    writer.writerow({'Genre':artist,
                                     'Sum':sumatory})
        cur.close()
        print("\n-> CSV Generation Successfully!")
    except:
        print("\n-> CSV Generation Failed!")

def exportSongPlayingsCSV(rows,currentUser):
    try:
        cur = con.cursor()
        with open('SongPlayings.csv', 'w', newline='') as f:
                fieldnames = ['Song','Playbacks']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for r in rows:
                    artist = r[0]
                    sumatory = r[1]
                    writer.writerow({'Song':artist,
                                     'Playbacks':sumatory})
        cur.close()
        print("\n-> CSV Generation Successfully!")
    except:
        print("\n-> CSV Generation Failed!")

def exportSellingsCSV(rows,currentUser):
    try:
        cur = con.cursor()
        with open('TotalSellings.csv', 'w', newline='') as f:
                fieldnames = ['Sum']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for r in rows:
                    sumatory = r[0]
                    writer.writerow({'Sum':sumatory})
        cur.close()
        print("\n-> CSV Generation Successfully!")
    except:
        print("\n-> CSV Generation Failed!")
    
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
        cur.close()
    except:
        print("\n->Registration failed!")

def loginUser(window,con):
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
                window.destroy()
                
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
                        window.destroy()
                    elif userType == 2:
                        currentUser['type'] = 'Tier 2'
                        customer2View(currentUser)
                        window.destroy()
                    elif userType == 3:
                        currentUser['type'] = 'Tier 3'
                        customer3View(currentUser)
                        window.destroy()
        cur.close()
    except:
        print("Login Failed")

##################################################################################################################
                                        #Vistas del sistema
##################################################################################################################

def registerView(View):
    global newuserEntry, newpasswordEntry, newFaxEntry, newFirstNameEntry, newLastNameEntry, newAddressEntry, newStateEntry, newCityEntry, newCountryEntry, newPostalEntry, newPhoneEntry, newEmailEntry, newCompanyEntry
    registerWindow = tkinter.Tk()
    View.destroy()
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
    backBtn = tkinter.Button(registerWindow, text="BACK", padx=15, pady=5, command = lambda: backToLogin(registerWindow))
    backBtn.grid(row=29,column=3)
    registerWindow.mainloop()

def loginView(con):
    global userEntry, passwordEntry
    window = tkinter.Tk()
    window.geometry("650x700")
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
    loginBtn = tkinter.Button(window, text="LOGIN", bg="#c8c8c8",padx=30, pady=10, command = lambda: loginUser(window,con))
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
    loginBtn = tkinter.Button(window, text="REGISTER", bg="#c8c8c8", padx=30, pady=10, command = lambda: registerView(window))
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
    showUser.config(font=("Helvetica", 23, "bold"))
    showUserType = tkinter.Label(customer1View, text="User type: Costumer " + currentUser['type'])
    showUserType.grid(row=2,column=1)
    showUserType.config(font=("Helvetica", 20, "bold"))
    space0 = tkinter.Label(customer1View, text="").grid(row=3,column=1)
    registerArtist = tkinter.Button(customer1View, text="Register New Artist", width=20, height=1, command = lambda: newArtistView(customer1View,currentUser))
    registerArtist.grid(row=4,column=1)
    registerAlbum = tkinter.Button(customer1View, text="Register New Album", width=20, height=1, command = lambda: newAlbumView(customer1View,currentUser))
    registerAlbum.grid(row=5,column=1)
    registerSong = tkinter.Button(customer1View, text="Register New Song", width=20, height=1, command = lambda: newSongView(customer1View,currentUser))
    registerSong.grid(row=6,column=1)
    mostAlbums = tkinter.Button(customer1View, text="Artist with most Albums",width=20,height=1, command = lambda: mostAlbumsView(customer1View,currentUser))
    mostAlbums.grid(row=4,column=2)
    mostGenres = tkinter.Button(customer1View, text="Genres with most Songs",width=20,height=1, command = lambda: mostGenresView(customer1View,currentUser))
    mostGenres.grid(row=5,column=2)
    playlistDuration = tkinter.Button(customer1View, text="Playlist Duration",width=20,height=1, command = lambda: playlistDurationView(customer1View,currentUser))
    playlistDuration.grid(row=6,column=2)
    longestSongs = tkinter.Button(customer1View, text="Longest Songs",width=20,height=1, command = lambda: longestSongsView(customer1View,currentUser))
    longestSongs.grid(row=7,column=2)
    usersSongs = tkinter.Button(customer1View, text="Users Songs",width=20,height=1, command = lambda: mostUsersUploadsView(customer1View,currentUser))
    usersSongs.grid(row=8,column=2)
    averageGenre = tkinter.Button(customer1View, text="Average Genre Length",width=20,height=1, command = lambda: averageGDView(customer1View,currentUser))
    averageGenre.grid(row=9,column=2)
    playlistArtists = tkinter.Button(customer1View, text="Playlist Artists",width=20,height=1, command = lambda: playlistArtistsView(customer1View,currentUser))
    playlistArtists.grid(row=10,column=2)
    diverseArtists = tkinter.Button(customer1View, text="Diverse Artists",width=20,height=1, command = lambda: diverseArtistsView(customer1View,currentUser))
    diverseArtists.grid(row=11,column=2)
    listenSongs = tkinter.Button(customer1View, text="Listen Songs",width=20,height=1, command = lambda: listenSongsCustomerView(customer1View,currentUser))
    listenSongs.grid(row=4,column=3)
    space4 = tkinter.Label(customer1View, text="").grid(row=5,column=3)
    purchaseSongs = tkinter.Button(customer1View, text="Purchase Songs",width=20,height=1, command = lambda: purchaseSongsView(customer1View,currentUser))
    purchaseSongs.grid(row=6,column=3)
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
    registerArtist = tkinter.Button(customer2View, text="Register New Artist", width=20, height=1, command = lambda: newArtistView(customer2View,currentUser))
    registerArtist.grid(row=4,column=1)
    registerAlbum = tkinter.Button(customer2View, text="Register New Album", width=20, height=1, command = lambda: newAlbumView(customer2View,currentUser))
    registerAlbum.grid(row=5,column=1)
    registerSong = tkinter.Button(customer2View, text="Register New Song", width=20, height=1, command = lambda: newSongView(customer2View,currentUser))
    registerSong.grid(row=6,column=1)
    modifyArtist = tkinter.Button(customer2View, text="Modify Artist", width=20, height=1, command = lambda: modifyArtistView(customer2View,currentUser))
    modifyArtist.grid(row=7,column=1)
    modifyAlbum = tkinter.Button(customer2View, text="Modify Album", width=20, height=1, command = lambda: modifyAlbumView(customer2View,currentUser))
    modifyAlbum.grid(row=8,column=1)
    modifySong = tkinter.Button(customer2View, text="Modify Song", width=20, height=1, command = lambda: modifySongView(customer2View,currentUser))
    modifySong.grid(row=9,column=1)
    mostAlbums = tkinter.Button(customer2View, text="Artist with most Albums",width=20,height=1, command = lambda: mostAlbumsView(customer2View,currentUser))
    mostAlbums.grid(row=4,column=2)
    mostGenres = tkinter.Button(customer2View, text="Genres with most Songs",width=20,height=1, command = lambda: mostGenresView(customer2View,currentUser))
    mostGenres.grid(row=5,column=2)
    playlistDuration = tkinter.Button(customer2View, text="Playlist Duration",width=20,height=1, command = lambda: playlistDurationView(customer2View,currentUser))
    playlistDuration.grid(row=6,column=2)
    longestSongs = tkinter.Button(customer2View, text="Longest Songs",width=20,height=1, command = lambda: longestSongsView(customer2View,currentUser))
    longestSongs.grid(row=7,column=2)
    usersSongs = tkinter.Button(customer2View, text="Users Songs",width=20,height=1, command = lambda: mostUsersUploadsView(customer2View,currentUser))
    usersSongs.grid(row=8,column=2)
    averageGenre = tkinter.Button(customer2View, text="Average Genre Length",width=20,height=1, command = lambda: averageGDView(customer2View,currentUser))
    averageGenre.grid(row=9,column=2)
    playlistArtists = tkinter.Button(customer2View, text="Playlist Artists",width=20,height=1, command = lambda: playlistArtistsView(customer2View,currentUser))
    playlistArtists.grid(row=10,column=2)
    diverseArtists = tkinter.Button(customer2View, text="Diverse Artists",width=20,height=1, command = lambda: diverseArtistsView(customer2View,currentUser))
    diverseArtists.grid(row=11,column=2)
    listenSongs = tkinter.Button(customer2View, text="Listen Songs",width=20,height=1, command = lambda: listenSongsCustomerView(customer2View,currentUser))
    listenSongs.grid(row=4,column=3)
    space4 = tkinter.Label(customer2View, text="").grid(row=5,column=3)
    purchaseSongs = tkinter.Button(customer2View, text="Purchase Songs",width=20,height=1, command = lambda: purchaseSongsView(customer2View,currentUser))
    purchaseSongs.grid(row=6,column=3)
    salesPerWeekBtn = tkinter.Button(customer2View, text="Sales per Week",width=20,height=1, command = lambda: rangeSellingsView(customer2View,currentUser))
    salesPerWeekBtn.grid(row=4,column=4)
    salesPerArtist = tkinter.Button(customer2View, text="Sales per Artist",width=20,height=1, command = lambda: artistSellingsView(customer2View,currentUser))
    salesPerArtist.grid(row=6,column=4)
    salesPerGenre = tkinter.Button(customer2View, text="Sales per Genre",width=20,height=1, command = lambda: genreSellingsView(customer2View,currentUser))
    salesPerGenre.grid(row=8,column=4)
    artistPlaybackBtn = tkinter.Button(customer2View, text="Artist Playback",width=20,height=1, command = lambda: artistPlayedSongsView(customer2View,currentUser))
    artistPlaybackBtn.grid(row=10,column=4)
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
    registerArtist = tkinter.Button(customer3View, text="Register New Artist", width=20, height=1, command = lambda: newArtistView(customer3View,currentUser))
    registerArtist.grid(row=4,column=1)
    registerAlbum = tkinter.Button(customer3View, text="Register New Album", width=20, height=1, command = lambda: newAlbumView(customer3View,currentUser))
    registerAlbum.grid(row=5,column=1)
    registerSong = tkinter.Button(customer3View, text="Register New Song", width=20, height=1, command = lambda: newSongView(customer3View,currentUser))
    registerSong.grid(row=6,column=1)
    modifyArtist = tkinter.Button(customer3View, text="Modify Artist", width=20, height=1, command = lambda: modifyArtistView(customer3View,currentUser))
    modifyArtist.grid(row=7,column=1)
    modifyAlbum = tkinter.Button(customer3View, text="Modify Album", width=20, height=1, command = lambda: modifyAlbumView(customer3View,currentUser))
    modifyAlbum.grid(row=8,column=1)
    modifySong = tkinter.Button(customer3View, text="Modify Song", width=20, height=1, command = lambda: modifySongView(customer3View,currentUser))
    modifySong.grid(row=9,column=1)
    deactivateSong = tkinter.Button(customer3View, text="Deactivate Song", width=20, height=1, command = lambda: deactivateSongView(customer3View,currentUser))
    deactivateSong.grid(row=13,column=1)
    activateSong = tkinter.Button(customer3View, text="Activate Song", width=20, height=1, command = lambda: activateSongView(customer3View,currentUser))
    activateSong.grid(row=14,column=1)
    mostAlbums = tkinter.Button(customer3View, text="Artist with most Albums",width=20,height=1, command = lambda: mostAlbumsView(customer3View,currentUser))
    mostAlbums.grid(row=4,column=2)
    mostGenres = tkinter.Button(customer3View, text="Genres with most Songs",width=20,height=1, command = lambda: mostGenresView(customer3View,currentUser))
    mostGenres.grid(row=5,column=2)
    playlistDuration = tkinter.Button(customer3View, text="Playlist Duration",width=20,height=1, command = lambda: playlistDurationView(customer3View,currentUser))
    playlistDuration.grid(row=6,column=2)
    longestSongs = tkinter.Button(customer3View, text="Longest Songs",width=20,height=1, command = lambda: longestSongsView(customer3View,currentUser))
    longestSongs.grid(row=7,column=2)
    usersSongs = tkinter.Button(customer3View, text="Users Songs",width=20,height=1, command = lambda: mostUsersUploadsView(customer3View,currentUser))
    usersSongs.grid(row=8,column=2)
    averageGenre = tkinter.Button(customer3View, text="Average Genre Length",width=20,height=1, command = lambda: averageGDView(customer3View,currentUser))
    averageGenre.grid(row=9,column=2)
    playlistArtists = tkinter.Button(customer3View, text="Playlist Artists",width=20,height=1, command = lambda: playlistArtistsView(customer3View,currentUser))
    playlistArtists.grid(row=10,column=2)
    diverseArtists = tkinter.Button(customer3View, text="Diverse Artists",width=20,height=1, command = lambda: diverseArtistsView(customer3View,currentUser))
    diverseArtists.grid(row=11,column=2)
    listenSongs = tkinter.Button(customer3View, text="Listen Songs",width=20,height=1, command = lambda: listenSongsCustomerView(customer3View,currentUser))
    listenSongs.grid(row=4,column=3)
    space4 = tkinter.Label(customer3View, text="").grid(row=5,column=3)
    purchaseSongs = tkinter.Button(customer3View, text="Purchase Songs",width=20,height=1, command = lambda: purchaseSongsView(customer3View,currentUser))
    purchaseSongs.grid(row=6,column=3)
    salesPerWeekBtn = tkinter.Button(customer3View, text="Sales per Week",width=20,height=1, command = lambda: rangeSellingsView(customer3View,currentUser))
    salesPerWeekBtn.grid(row=4,column=4)
    salesPerArtist = tkinter.Button(customer3View, text="Sales per Artist",width=20,height=1, command = lambda: artistSellingsView(customer3View,currentUser))
    salesPerArtist.grid(row=6,column=4)
    salesPerGenre = tkinter.Button(customer3View, text="Sales per Genre",width=20,height=1, command = lambda: genreSellingsView(customer3View,currentUser))
    salesPerGenre.grid(row=8,column=4)
    artistPlaybackBtn = tkinter.Button(customer3View, text="Artist Playback",width=20,height=1, command = lambda: artistPlayedSongsView(customer3View,currentUser))
    artistPlaybackBtn.grid(row=10,column=4)
    space0 = tkinter.Label(customer3View, text="").grid(row=15,column=1)
    space0 = tkinter.Label(customer3View, text="").grid(row=16,column=1)
    space0 = tkinter.Label(customer3View, text="").grid(row=17,column=1)
    logoutBtn = tkinter.Button(customer3View, text="LOGOUT", width=20, height=1, bg="#ff9999", command = lambda: logOut(customer3View,currentUser))
    logoutBtn.grid(row=18,column=1)
    customer3View.mainloop()
    
def adminView(currentUser):
    adminWindow = tkinter.Tk()
    adminWindow.geometry("1250x700")
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
    registerArtist = tkinter.Button(adminWindow, text="Register New Artist", width=20, height=1, command = lambda: newArtistView(adminWindow,currentUser))
    registerArtist.grid(row=4,column=1)
    registerAlbum = tkinter.Button(adminWindow, text="Register New Album", width=20, height=1, command = lambda: newAlbumView(adminWindow,currentUser))
    registerAlbum.grid(row=5,column=1)
    registerSong = tkinter.Button(adminWindow, text="Register New Song", width=20, height=1, command = lambda: newSongView(adminWindow,currentUser))
    registerSong.grid(row=6,column=1)
    modifyArtist = tkinter.Button(adminWindow, text="Modify Artist", width=20, height=1, command = lambda: modifyArtistView(adminWindow,currentUser))
    modifyArtist.grid(row=7,column=1)
    modifyAlbum = tkinter.Button(adminWindow, text="Modify Album", width=20, height=1, command = lambda: modifyAlbumView(adminWindow,currentUser))
    modifyAlbum.grid(row=8,column=1)
    modifySong = tkinter.Button(adminWindow, text="Modify Song", width=20, height=1, command = lambda: modifySongView(adminWindow,currentUser))
    modifySong.grid(row=9,column=1)
    removeArtist = tkinter.Button(adminWindow, text="Remove Artist", width=20, height=1, command = lambda: removeArtistView(adminWindow,currentUser))
    removeArtist.grid(row=10,column=1)
    removeAlbum = tkinter.Button(adminWindow, text="Remove Album", width=20, height=1, command = lambda: removeAlbumView(adminWindow,currentUser))
    removeAlbum.grid(row=11,column=1)
    removeSong = tkinter.Button(adminWindow, text="Remove Song", width=20, height=1, command = lambda: removeSongView(adminWindow,currentUser))
    removeSong.grid(row=12,column=1)
    deactivateSong = tkinter.Button(adminWindow, text="Deactivate Song", width=20, height=1, command = lambda: deactivateSongView(adminWindow,currentUser))
    deactivateSong.grid(row=13,column=1)
    activateSong = tkinter.Button(adminWindow, text="Activate Song", width=20, height=1, command = lambda: activateSongView(adminWindow,currentUser))
    activateSong.grid(row=14,column=1)
    manageUsers = tkinter.Button(adminWindow, text="Change User permission", width=20, height=1, command = lambda: userPermissionView(adminWindow,currentUser))
    manageUsers.grid(row=15,column=1)
    space2 = tkinter.Label(adminWindow, text="").grid(row=16,column=1)
    space3 = tkinter.Label(adminWindow, text="").grid(row=17,column=1)
    mostAlbums = tkinter.Button(adminWindow, text="Artist with most Albums",width=20,height=1, command = lambda: mostAlbumsView(adminWindow,currentUser))
    mostAlbums.grid(row=4,column=2)
    mostGenres = tkinter.Button(adminWindow, text="Genres with most Songs",width=20,height=1, command = lambda: mostGenresView(adminWindow,currentUser))
    mostGenres.grid(row=5,column=2)
    playlistDuration = tkinter.Button(adminWindow, text="Playlist Duration",width=20,height=1, command = lambda: playlistDurationView(adminWindow,currentUser))
    playlistDuration.grid(row=6,column=2)
    longestSongs = tkinter.Button(adminWindow, text="Longest Songs",width=20,height=1, command = lambda: longestSongsView(adminWindow,currentUser))
    longestSongs.grid(row=7,column=2)
    usersSongs = tkinter.Button(adminWindow, text="Users Songs",width=20,height=1, command = lambda: mostUsersUploadsView(adminWindow,currentUser))
    usersSongs.grid(row=8,column=2)
    averageGenre = tkinter.Button(adminWindow, text="Average Genre Length",width=20,height=1, command = lambda: averageGDView(adminWindow,currentUser))
    averageGenre.grid(row=9,column=2)
    playlistArtists = tkinter.Button(adminWindow, text="Playlist Artists",width=20,height=1, command = lambda: playlistArtistsView(adminWindow,currentUser))
    playlistArtists.grid(row=10,column=2)
    diverseArtists = tkinter.Button(adminWindow, text="Diverse Artists",width=20,height=1, command = lambda: diverseArtistsView(adminWindow,currentUser))
    diverseArtists.grid(row=11,column=2)
    listenSongs = tkinter.Button(adminWindow, text="Listen Songs",width=20,height=1, command = lambda: listenSongsAdminView(adminWindow,currentUser))
    listenSongs.grid(row=4,column=3)
    space4 = tkinter.Label(adminWindow, text="").grid(row=5,column=3)
    purchaseSongs = tkinter.Button(adminWindow, text="Purchase Songs",width=20,height=1, command = lambda: listenSongsAdminView(adminWindow,currentUser))
    purchaseSongs.grid(row=6,column=3)
    space5 = tkinter.Label(adminWindow, text="").grid(row=7,column=3)
    trackLogs = tkinter.Button(adminWindow, text="Song Logs",width=20,height=1, command = lambda: listenSongsView(adminWindow,currentUser))
    trackLogs.grid(row=8,column=3)
    space6 = tkinter.Label(adminWindow, text="").grid(row=9,column=3)
    purchaseSimulator = tkinter.Button(adminWindow, text="Simulator",width=20,height=1, command = lambda: randomizerView())
    purchaseSimulator.grid(row=10,column=3)
    promotion = tkinter.Button(adminWindow, text="Promotion",width=20,height=1, command = lambda: promotionView(adminWindow,currentUser))
    promotion.grid(row=12,column=3)
    intelligence = tkinter.Button(adminWindow, text="Intelligence",width=20,height=1, command = lambda: listenSongsAdminView(adminWindow,currentUser))
    intelligence.grid(row=14,column=3)
    salesPerWeekBtn = tkinter.Button(adminWindow, text="Sales per Week",width=20,height=1, command = lambda: rangeSellingsView(adminWindow,currentUser))
    salesPerWeekBtn.grid(row=4,column=4)
    salesPerArtist = tkinter.Button(adminWindow, text="Sales per Artist",width=20,height=1, command = lambda: artistSellingsView(adminWindow,currentUser))
    salesPerArtist.grid(row=6,column=4)
    salesPerGenre = tkinter.Button(adminWindow, text="Sales per Genre",width=20,height=1, command = lambda: genreSellingsView(adminWindow,currentUser))
    salesPerGenre.grid(row=8,column=4)
    artistPlaybackBtn = tkinter.Button(adminWindow, text="Artist Playback",width=20,height=1, command = lambda: artistPlayedSongsView(adminWindow,currentUser))
    artistPlaybackBtn.grid(row=10,column=4)
    space8 = tkinter.Label(adminWindow, text="").grid(row=18,column=1)
    space9 = tkinter.Label(adminWindow, text="").grid(row=19,column=1)
    logoutBtn = tkinter.Button(adminWindow, text="LOGOUT", width=20, height=1, bg="#ff9999", command = lambda: logOut(adminWindow,currentUser))
    logoutBtn.grid(row=20,column=1)
    adminWindow.mainloop()

def newArtistView(View,currentUser):
    global newArtistName
    newArtistWindow = tkinter.Tk()
    View.destroy()
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
    backArtistBtn = tkinter.Button(newArtistWindow,text="Back",bg="#c8c8c8",padx=20,pady=10, command = lambda: backToView(newArtistWindow,currentUser))
    backArtistBtn.pack()
    newArtistWindow.mainloop()

def newAlbumView(View,currentUser):
    global albumTitle, albumArtistName
    newAlbumWindow = tkinter.Tk()
    View.destroy()
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
    backAlbumBtn = tkinter.Button(newAlbumWindow,text="Back",bg="#c8c8c8",padx=20,pady=10, command = lambda: backToView(newAlbumWindow,currentUser))
    backAlbumBtn.pack()
    newAlbumWindow.mainloop()

def newSongView(View,currentUser):
    global newSongTitle, newSongAlbumName, newSongMediaType, newSongGenre, newSongComposer, newSongMilliseconds, newSongBytes, newSongPrice, newSongURL
    newSongWindow = tkinter.Tk()
    View.destroy()
    newSongWindow.geometry("650x950")
    newSongWindow.title("Enter New Song")
    space00 = tkinter.Label(newSongWindow, text="")
    space00.pack()
    windowTitle = tkinter.Label(newSongWindow, text="Enter new Song")
    windowTitle.config(font=("Helvetica",16,"bold"))
    windowTitle.pack()
    space0 = tkinter.Label(newSongWindow, text="")
    space0.pack()
    Instruction1 = tkinter.Label(newSongWindow, text="Enter Song Name")
    Instruction1.config(font=("Helvetica",11,"bold"))
    Instruction1.pack()
    newSongTitle = tkinter.Entry(newSongWindow, font="Helvetica 12")
    newSongTitle.pack()
    space1 = tkinter.Label(newSongWindow, text="")
    space1.pack()
    Instruction2 = tkinter.Label(newSongWindow, text="Enter Album Name")
    Instruction2.config(font=("Helvetica",11,"bold"))
    Instruction2.pack()
    newSongAlbumName = tkinter.Entry(newSongWindow, font="Helvetica 12")
    newSongAlbumName.pack()
    space2 = tkinter.Label(newSongWindow, text="")
    space2.pack()
    Instruction3 = tkinter.Label(newSongWindow, text="Enter Media Type")
    Instruction3.config(font=("Helvetica",11,"bold"))
    Instruction3.pack()
    newSongMediaType = tkinter.Entry(newSongWindow, font="Helvetica 12")
    newSongMediaType.pack()
    space3 = tkinter.Label(newSongWindow, text="")
    space3.pack()
    Instruction4 = tkinter.Label(newSongWindow, text="Enter Genre")
    Instruction4.config(font=("Helvetica",11,"bold"))
    Instruction4.pack()
    newSongGenre = tkinter.Entry(newSongWindow, font="Helvetica 12")
    newSongGenre.pack()
    space4 = tkinter.Label(newSongWindow, text="")
    space4.pack()
    Instruction5 = tkinter.Label(newSongWindow, text="Enter Composer")
    Instruction5.config(font=("Helvetica",11,"bold"))
    Instruction5.pack()
    newSongComposer = tkinter.Entry(newSongWindow, font="Helvetica 12")
    newSongComposer.pack()
    space5 = tkinter.Label(newSongWindow, text="")
    space5.pack()
    Instruction6 = tkinter.Label(newSongWindow, text="Enter Milliseconds")
    Instruction6.config(font=("Helvetica",11,"bold"))
    Instruction6.pack()
    newSongMilliseconds = tkinter.Entry(newSongWindow, font="Helvetica 12")
    newSongMilliseconds.pack()
    space6 = tkinter.Label(newSongWindow, text="")
    space6.pack()
    Instruction7 = tkinter.Label(newSongWindow, text="Enter Bytes")
    Instruction7.config(font=("Helvetica",11,"bold"))
    Instruction7.pack()
    newSongBytes = tkinter.Entry(newSongWindow, font="Helvetica 12")
    newSongBytes.pack()
    space7 = tkinter.Label(newSongWindow, text="")
    space7.pack()
    Instruction8 = tkinter.Label(newSongWindow, text="Enter Song Price")
    Instruction8.config(font=("Helvetica",11,"bold"))
    Instruction8.pack()
    newSongPrice = tkinter.Entry(newSongWindow, font="Helvetica 12")
    newSongPrice.pack()
    space8 = tkinter.Label(newSongWindow, text="")
    space8.pack()
    Instruction9 = tkinter.Label(newSongWindow, text="Enter Song URL")
    Instruction9.config(font=("Helvetica",11,"bold"))
    Instruction9.pack()
    newSongURL = tkinter.Entry(newSongWindow, font="Helvetica 12")
    newSongURL.pack()
    space9 = tkinter.Label(newSongWindow, text="")
    space9.pack()
    enterArtistBtn = tkinter.Button(newSongWindow,text="Enter Song",bg="#c8c8c8",padx=20,pady=6, command = lambda: insertNewSong(currentUser))
    enterArtistBtn.pack()
    space10 = tkinter.Label(newSongWindow, text="")
    space10.pack()
    backSongBtn = tkinter.Button(newSongWindow,text="Back",bg="#c8c8c8",padx=20,pady=6, command = lambda: backToView(newSongWindow,currentUser))
    backSongBtn.pack()
    newSongWindow.mainloop()

def modifyArtistView(View,currentUser):
    global oldArtistName, upArtistName
    mdArtistWindow = tkinter.Tk()
    View.destroy()
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
    backModifyBtn = tkinter.Button(mdArtistWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(mdArtistWindow,currentUser))
    backModifyBtn.grid(row=11,column=3)
    mdArtistWindow.mainloop()

def modifyAlbumView(View,currentUser):
    global oldAlbumName, upAlbumName, upAlbumArtist
    mdAlbumWindow = tkinter.Tk()
    View.destroy()
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
    backModifyBtn = tkinter.Button(mdAlbumWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(mdAlbumWindow,currentUser))
    backModifyBtn.grid(row=14,column=3)
    mdAlbumWindow.mainloop()

def modifySongView(View,currentUser):
    global oldSongName, upSongName, upSongAlbum, upSongMediaType, upSongGenre, upSongComposer, upSongMilliseconds, upSongBytes, upSongURL, upSongPrice
    mdSongWindow = tkinter.Tk()
    View.destroy()
    for i in range(7):
        mdSongWindow.columnconfigure(i,weight=1)
    mdSongWindow.geometry("850x950")
    mdSongWindow.title("Modify Song")
    space00 = tkinter.Label(mdSongWindow, text=" ").grid(row=0,column=5)
    titleReg = tkinter.Label(mdSongWindow, text="Modify Song")
    titleReg.grid(row=2,column=3)
    titleReg.config(font=("Steamer",17,"bold"))
    space0 = tkinter.Label(mdSongWindow, text=" ").grid(row=4,column=3)
    Instructions = tkinter.Label(mdSongWindow, text="Old Song Name")
    Instructions.grid(row=6,column=2)
    Instructions.config(font=("Helvetica", 12,"bold"))
    oldSongName = tkinter.Entry(mdSongWindow, font="Helvetica 10")
    oldSongName.grid(row=7,column=2)
    Instructions2 = tkinter.Label(mdSongWindow, text="New Song Name")
    Instructions2.grid(row=6,column=4)
    Instructions2.config(font=("Helvetica", 12,"bold"))
    upSongName = tkinter.Entry(mdSongWindow, font="Helvetica 10")
    upSongName.grid(row=7,column=4)
    space1 = tkinter.Label(mdSongWindow, text=" ").grid(row=8,column=4)
    Instructions3 = tkinter.Label(mdSongWindow, text="New Album Name")
    Instructions3.grid(row=9,column=4)
    Instructions3.config(font=("Helvetica", 12,"bold"))
    upSongAlbum = tkinter.Entry(mdSongWindow, font="Helvetica 10")
    upSongAlbum.grid(row=10,column=4)
    space2 = tkinter.Label(mdSongWindow, text=" ").grid(row=11,column=4)
    Instructions4 = tkinter.Label(mdSongWindow, text="New Media Type")
    Instructions4.grid(row=12,column=4)
    Instructions4.config(font=("Helvetica", 12,"bold"))
    upSongMediaType = tkinter.Entry(mdSongWindow, font="Helvetica 10")
    upSongMediaType.grid(row=13,column=4)
    space3 = tkinter.Label(mdSongWindow, text=" ").grid(row=14,column=4)
    Instructions5 = tkinter.Label(mdSongWindow, text="New Genre Name")
    Instructions5.grid(row=15,column=4)
    Instructions5.config(font=("Helvetica", 12,"bold"))
    upSongGenre = tkinter.Entry(mdSongWindow, font="Helvetica 10")
    upSongGenre.grid(row=16,column=4)
    space4 = tkinter.Label(mdSongWindow, text=" ").grid(row=17,column=4)
    Instructions6 = tkinter.Label(mdSongWindow, text="New Composer")
    Instructions6.grid(row=18,column=4)
    Instructions6.config(font=("Helvetica", 12,"bold"))
    upSongComposer = tkinter.Entry(mdSongWindow, font="Helvetica 10")
    upSongComposer.grid(row=19,column=4)
    space5 = tkinter.Label(mdSongWindow, text=" ").grid(row=20,column=4)
    Instructions7 = tkinter.Label(mdSongWindow, text="New Milliseconds")
    Instructions7.grid(row=21,column=4)
    Instructions7.config(font=("Helvetica", 12,"bold"))
    upSongMilliseconds = tkinter.Entry(mdSongWindow, font="Helvetica 10")
    upSongMilliseconds.grid(row=22,column=4)
    space6 = tkinter.Label(mdSongWindow, text=" ").grid(row=23,column=4)
    Instructions8 = tkinter.Label(mdSongWindow, text="New Bytes")
    Instructions8.grid(row=24,column=4)
    Instructions8.config(font=("Helvetica", 12,"bold"))
    upSongBytes = tkinter.Entry(mdSongWindow, font="Helvetica 10")
    upSongBytes.grid(row=25,column=4)
    space7 = tkinter.Label(mdSongWindow, text=" ").grid(row=26,column=4)
    Instructions9 = tkinter.Label(mdSongWindow, text="New Unit Price")
    Instructions9.grid(row=27,column=4)
    Instructions9.config(font=("Helvetica", 12,"bold"))
    upSongPrice = tkinter.Entry(mdSongWindow, font="Helvetica 10")
    upSongPrice.grid(row=28,column=4)
    space2 = tkinter.Label(mdSongWindow, text="").grid(row=29,column=2)
    Instructions10 = tkinter.Label(mdSongWindow, text="New URL")
    Instructions10.grid(row=30,column=4)
    Instructions10.config(font=("Helvetica", 12,"bold"))
    upSongURL = tkinter.Entry(mdSongWindow, font="Helvetica 10")
    upSongURL.grid(row=31,column=4)
    space2 = tkinter.Label(mdSongWindow, text="").grid(row=32,column=2)
    updateSongBtn = tkinter.Button(mdSongWindow, text="Update Song", padx=15, pady=5, bg="#c8c8c8", command = lambda: modifySong(currentUser))
    updateSongBtn.grid(row=33,column=3)
    space3 = tkinter.Label(mdSongWindow, text="").grid(row=34,column=3)
    backModifyBtn = tkinter.Button(mdSongWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(mdSongWindow,currentUser))
    backModifyBtn.grid(row=35,column=3)
    mdSongWindow.mainloop()

def removeArtistView(View,currentUser):
    global removeArtistName
    removeArtistWindow = tkinter.Tk()
    View.destroy()
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
    removeArtistBtn = tkinter.Button(removeArtistWindow,text="Remove Artist",bg="#c8c8c8",padx=20,pady=10, command = lambda: removeArtist(currentUser))
    removeArtistBtn.pack()
    space2 = tkinter.Label(removeArtistWindow, text="")
    space2.pack()
    backArtistBtn = tkinter.Button(removeArtistWindow,text="Back",bg="#c8c8c8",padx=20,pady=10, command = lambda: backToView(removeArtistWindow,currentUser))
    backArtistBtn.pack()
    removeArtistWindow.mainloop()
    removeArtistWindow.mainloop()

def removeAlbumView(View,currentUser):
    global rmalbumTitle, rmalbumArtistName
    removeAlbumWindow = tkinter.Tk()
    View.destroy()
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
    removeAlbumBtn = tkinter.Button(removeAlbumWindow,text="Remove Album",bg="#c8c8c8",padx=20,pady=10, command = lambda: removeAlbum(currentUser))
    removeAlbumBtn.pack()
    space3 = tkinter.Label(removeAlbumWindow, text="")
    space3.pack()
    backAlbumBtn = tkinter.Button(removeAlbumWindow,text="Back",bg="#c8c8c8",padx=20,pady=10, command = lambda: backToView(removeAlbumWindow,currentUser))
    backAlbumBtn.pack()
    removeAlbumWindow.mainloop()

def removeSongView(View,currentUser):
    global rmsgSongTitle, rmsgComposer
    removeSongWindow = tkinter.Tk()
    View.destroy()
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
    removeSongBtn = tkinter.Button(removeSongWindow,text="Remove Song",bg="#c8c8c8",padx=20,pady=10, command = lambda: removeSong(currentUser))
    removeSongBtn.pack()
    space3 = tkinter.Label(removeSongWindow, text="")
    space3.pack()
    backRemoveSongBtn = tkinter.Button(removeSongWindow,text="Back",bg="#c8c8c8",padx=20,pady=10, command = lambda: backToView(removeSongWindow,currentUser))
    backRemoveSongBtn.pack()
    removeSongWindow.mainloop()

def deactivateSongView(View,currentUser):
    global deactivateSongTitle, deactivateSongComposer
    deactivateWindow = tkinter.Tk()
    View.destroy()
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
    space2 = tkinter.Label(deactivateWindow, text="")
    space2.pack()
    deactivateSongBtn = tkinter.Button(deactivateWindow,text="Deactivate Song",bg="#c8c8c8",padx=20,pady=10, command = lambda: songDeactivation(currentUser))
    deactivateSongBtn.pack()
    space3 = tkinter.Label(deactivateWindow, text="")
    space3.pack()
    backDeactivateBtn = tkinter.Button(deactivateWindow,text="Back",bg="#c8c8c8",padx=20,pady=10, command = lambda: backToView(deactivateWindow,currentUser))
    backDeactivateBtn.pack()
    deactivateWindow.mainloop()

def activateSongView(View,currentUser):
    global activateSongTitle, activateSongComposer
    activateWindow = tkinter.Tk()
    View.destroy()
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
    space2 = tkinter.Label(activateWindow, text="")
    space2.pack()
    activateSongBtn = tkinter.Button(activateWindow,text="Activate Song",bg="#c8c8c8",padx=20,pady=10, command = lambda: songActivation(currentUser))
    activateSongBtn.pack()
    space3 = tkinter.Label(activateWindow, text="")
    space3.pack()
    backActivateBtn = tkinter.Button(activateWindow,text="Back",bg="#c8c8c8",padx=20,pady=10, command = lambda: backToView(activateWindow,currentUser))
    backActivateBtn.pack()
    activateWindow.mainloop()

def userPermissionView(View,currentUser):
    global permissionUsername, permissionNewNumber
    permissionWindow = tkinter.Tk()
    View.destroy()
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
    changePermissionBtn = tkinter.Button(permissionWindow,text="Change Permission",bg="#c8c8c8",padx=20,pady=10, command = lambda: changeUserPermission(currentUser))
    changePermissionBtn.pack()
    space3 = tkinter.Label(permissionWindow, text="")
    space3.pack()
    backPermissionBtn = tkinter.Button(permissionWindow,text="Back",bg="#c8c8c8",padx=20,pady=10, command = lambda: backToView(permissionWindow,currentUser))
    backPermissionBtn.pack()
    permissionWindow.mainloop()

def mostAlbumsView(View,currentUser):
    cur = con.cursor()
    mostAlbumsView = tkinter.Tk()
    View.destroy()
    mostAlbumsView.geometry("1000x500")
    for i in range(5):
        mostAlbumsView.columnconfigure(i,weight=1)
    mostAlbumsView.title("Most Albums View")
    space00 = tkinter.Label(mostAlbumsView, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(mostAlbumsView, text="Artists with most Albums")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(mostAlbumsView, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(mostAlbumsView, text="Number")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=1)
    subTitle = tkinter.Label(mostAlbumsView, text="Artist")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=3,column=2)
    subTitle2 = tkinter.Label(mostAlbumsView, text="Number of albums")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=3,column=3)
    cur.execute("""select a.name as "Nombre", t.count as "Numero de Albumes"
                from (select artistid, count(artistid) as count
                from album
                group by artistid) t
                join artist a on a.artistid = t.artistid
                order by t.count desc
                limit 5""")
    rows = cur.fetchall()
    i = 4
    x = 1
    for r in rows:
        number = tkinter.Label(mostAlbumsView, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        artist = tkinter.Label(mostAlbumsView,text=r[0])
        artist.config(font=("Helvetica",15))
        artist.grid(row=i,column=2)
        albums = tkinter.Label(mostAlbumsView,text=str(r[1]))
        albums.config(font=("Helvetica",15))
        albums.grid(row=i,column=3)
        i += 1
        x += 1
    space1 = tkinter.Label(mostAlbumsView, text="").grid(row=9,column=3)
    space2 = tkinter.Label(mostAlbumsView, text="").grid(row=10,column=3)
    backModifyBtn = tkinter.Button(mostAlbumsView, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(mostAlbumsView,currentUser))
    backModifyBtn.grid(row=11,column=2)
    mostAlbumsView.mainloop()

def mostGenresView(View,currentUser):
    cur = con.cursor()
    mostGenresView = tkinter.Tk()
    View.destroy()
    mostGenresView.geometry("1000x500")
    for i in range(5):
        mostGenresView.columnconfigure(i,weight=1)
    mostGenresView.title("Most Genres View")
    space00 = tkinter.Label(mostGenresView, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(mostGenresView, text="Genres with most Songs")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(mostGenresView, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(mostGenresView, text="Number")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=1)
    subTitle = tkinter.Label(mostGenresView, text="Genre")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=3,column=2)
    subTitle2 = tkinter.Label(mostGenresView, text="Number of Songs")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=3,column=3)
    cur.execute("""select g.name as "Genero", t.counter as "Numero de Canciones"
                from (select genreid, count(genreid) as counter
                from track
                group by genreid) t
                left join genre g on g.genreid = t.genreid
                order by t.counter desc
                LIMIT 5;""")
    rows = cur.fetchall()
    i = 4
    x = 1
    for r in rows:
        number = tkinter.Label(mostGenresView, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        artist = tkinter.Label(mostGenresView,text=r[0])
        artist.config(font=("Helvetica",15))
        artist.grid(row=i,column=2)
        albums = tkinter.Label(mostGenresView,text=str(r[1]))
        albums.config(font=("Helvetica",15))
        albums.grid(row=i,column=3)
        i += 1
        x += 1
    space1 = tkinter.Label(mostGenresView, text="").grid(row=9,column=3)
    space2 = tkinter.Label(mostGenresView, text="").grid(row=10,column=3)
    backModifyBtn = tkinter.Button(mostGenresView, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(mostGenresView,currentUser))
    backModifyBtn.grid(row=11,column=2)
    mostGenresView.mainloop()

def playlistDurationView(View,currentUser):
    cur = con.cursor()
    playlistDuration = tkinter.Tk()
    View.destroy()
    playlistDuration.geometry("1000x500")
    for i in range(5):
        playlistDuration.columnconfigure(i,weight=1)
    playlistDuration.title("Playlist Duration")
    space00 = tkinter.Label(playlistDuration, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(playlistDuration, text="Playlist Duration")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(playlistDuration, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(playlistDuration, text="Number")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=1)
    subTitle = tkinter.Label(playlistDuration, text="Playlist Name")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=3,column=2)
    subTitle2 = tkinter.Label(playlistDuration, text="Duration (minutes)")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=3,column=3)
    cur.execute("""select p.playlistid as "ID", p.name as "Nombre del Album", sum(t.milliseconds*0.000016666666) as "Tiempo de Duracion (Segundos)"
                from (select playlistid, trackid
                from playlisttrack) pt
                join track t on t.trackid = pt.trackid
                join playlist p on pt.playlistid = p.playlistid
                group by p.playlistid
                limit 7;""")
    rows = cur.fetchall()
    i = 4
    x = 1
    for r in rows:
        number = tkinter.Label(playlistDuration, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        artist = tkinter.Label(playlistDuration,text=r[1])
        artist.config(font=("Helvetica",15))
        artist.grid(row=i,column=2)
        albums = tkinter.Label(playlistDuration,text=str(r[2]))
        albums.config(font=("Helvetica",15))
        albums.grid(row=i,column=3)
        i += 1
        x += 1
    space1 = tkinter.Label(playlistDuration, text="").grid(row=11,column=3)
    space2 = tkinter.Label(playlistDuration, text="").grid(row=12,column=3)
    backModifyBtn = tkinter.Button(playlistDuration, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(playlistDuration,currentUser))
    backModifyBtn.grid(row=13,column=2)
    playlistDuration.mainloop()

def longestSongsView(View,currentUser):
    cur = con.cursor()
    longestSongs = tkinter.Tk()
    View.destroy()
    longestSongs.geometry("1400x500")
    for i in range(5):
        longestSongs.columnconfigure(i,weight=1)
    longestSongs.title("Playlist Duration")
    space00 = tkinter.Label(longestSongs, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(longestSongs, text="Longest Songs")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(longestSongs, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(longestSongs, text="Number")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=1)
    subTitle = tkinter.Label(longestSongs, text="Song Name")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=3,column=2)
    subTitle2 = tkinter.Label(longestSongs, text="Duration (minutes)")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=3,column=3)
    subTitle3 = tkinter.Label(longestSongs, text="Artist Name")
    subTitle3.config(font=("Helvetica",15,"bold"))
    subTitle3.grid(row=3,column=4)
    cur.execute("""select t.name as "Nombre", t.milliseconds*0.000016666666 as "Tiempo de Duracion (Minutos)", ar.name as "Artista/s"
                from album a
                join track t on a.albumid = t.albumid
                join artist ar on a.artistid = ar.artistid
                order by t.milliseconds desc
                limit 5;""")
    rows = cur.fetchall()
    i = 4
    x = 1
    for r in rows:
        number = tkinter.Label(longestSongs, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        song = tkinter.Label(longestSongs,text=r[0])
        song.config(font=("Helvetica",15))
        song.grid(row=i,column=2)
        duration = tkinter.Label(longestSongs,text=str(r[1]))
        duration.config(font=("Helvetica",15))
        duration.grid(row=i,column=3)
        artist = tkinter.Label(longestSongs,text=str(r[2]))
        artist.config(font=("Helvetica",15))
        artist.grid(row=i,column=4)
        i += 1
        x += 1
    space1 = tkinter.Label(longestSongs, text="").grid(row=9,column=3)
    space2 = tkinter.Label(longestSongs, text="").grid(row=10,column=3)
    backModifyBtn = tkinter.Button(longestSongs, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(longestSongs,currentUser))
    backModifyBtn.grid(row=11,column=2)
    longestSongs.mainloop()

def mostUsersUploadsView(View,currentUser):
    cur = con.cursor()
    userUploads = tkinter.Tk()
    View.destroy()
    userUploads.geometry("1400x500")
    for i in range(5):
        userUploads.columnconfigure(i,weight=1)
    userUploads.title("User Uploads")
    space00 = tkinter.Label(userUploads, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(userUploads, text="Users Uploads")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(userUploads, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(userUploads, text="Number")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=1)
    subTitle = tkinter.Label(userUploads, text="User Name")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=3,column=2)
    subTitle2 = tkinter.Label(userUploads, text="Number of Uploads)")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=3,column=3)
    cur.execute("""select customer.username, mid.counting
            from (select customerid, count(customerid) as counting
            from invoice
            group by customerid) mid
            left join customer on customer.customerid = mid.customerid
            limit 5;""")
    rows = cur.fetchall()
    i = 4
    x = 1
    for r in rows:
        number = tkinter.Label(userUploads, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        us = tkinter.Label(userUploads,text=r[0])
        us.config(font=("Helvetica",15))
        us.grid(row=i,column=2)
        number2 = tkinter.Label(userUploads,text=str(r[1]))
        number2.config(font=("Helvetica",15))
        number2.grid(row=i,column=3)
        i += 1
        x += 1
    space1 = tkinter.Label(userUploads, text="").grid(row=9,column=3)
    space2 = tkinter.Label(userUploads, text="").grid(row=10,column=3)
    backModifyBtn = tkinter.Button(userUploads, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(userUploads,currentUser))
    backModifyBtn.grid(row=11,column=2)
    userUploads.mainloop()

def averageGDView(View,currentUser):
    cur = con.cursor()
    averageGD = tkinter.Tk()
    View.destroy()
    averageGD.geometry("1000x500")
    for i in range(5):
        averageGD.columnconfigure(i,weight=1)
    averageGD.title("Average Genre Duration")
    space00 = tkinter.Label(averageGD, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(averageGD, text="Average Genre Duration")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(averageGD, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(averageGD, text="Number")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=1)
    subTitle = tkinter.Label(averageGD, text="Genre")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=3,column=2)
    subTitle2 = tkinter.Label(averageGD, text="Average Length (minutes)")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=3,column=3)
    cur.execute("""select g.name as "Nombre", t.average as "Promedio de Duracion (Minutos)"
                from (select genreid, avg(milliseconds)*0.000016666666 average
                from track
                group by genreid) t
                join genre g on g.genreid = t.genreid
                order by t.average desc
                limit 7;""")
    rows = cur.fetchall()
    i = 4
    x = 1
    for r in rows:
        number = tkinter.Label(averageGD, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        genre = tkinter.Label(averageGD,text=r[0])
        genre.config(font=("Helvetica",15))
        genre.grid(row=i,column=2)
        duration = tkinter.Label(averageGD,text=str(r[1]))
        duration.config(font=("Helvetica",15))
        duration.grid(row=i,column=3)
        i += 1
        x += 1
    space1 = tkinter.Label(averageGD, text="").grid(row=11,column=3)
    space2 = tkinter.Label(averageGD, text="").grid(row=12,column=3)
    backModifyBtn = tkinter.Button(averageGD, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(averageGD,currentUser))
    backModifyBtn.grid(row=13,column=2)
    averageGD.mainloop()

def playlistArtistsView(View,currentUser):
    cur = con.cursor()
    playlistArtists = tkinter.Tk()
    View.destroy()
    playlistArtists.geometry("1000x500")
    for i in range(5):
        playlistArtists.columnconfigure(i,weight=1)
    playlistArtists.title("Artists Per Playlist")
    space00 = tkinter.Label(playlistArtists, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(playlistArtists, text="Number of Artists for Playlist")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(playlistArtists, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(playlistArtists, text="Number")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=1)
    subTitle = tkinter.Label(playlistArtists, text="Playlist")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=3,column=2)
    subTitle2 = tkinter.Label(playlistArtists, text="Number of Artists")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=3,column=3)
    cur.execute("""select p.name as "Nombre del Album", count(al.artistid) as "Numero de Artistas"
                from (select playlisttrack.playlistid as PLAYLISTID, track.albumid as ALBUMID
                from track
                join playlisttrack on track.trackid = playlisttrack.trackid) mid
                join playlist p on mid.PLAYLISTID = p.playlistid
                join album al on al.albumid = mid.ALBUMID
                group by p.playlistid
                order by count(al.artistid) desc
                limit 7;""")
    rows = cur.fetchall()
    i = 4
    x = 1
    for r in rows:
        number = tkinter.Label(playlistArtists, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        playlist = tkinter.Label(playlistArtists,text=r[0])
        playlist.config(font=("Helvetica",15))
        playlist.grid(row=i,column=2)
        artists = tkinter.Label(playlistArtists,text=str(r[1]))
        artists.config(font=("Helvetica",15))
        artists.grid(row=i,column=3)
        i += 1
        x += 1
    space1 = tkinter.Label(playlistArtists, text="").grid(row=11,column=3)
    space2 = tkinter.Label(playlistArtists, text="").grid(row=12,column=3)
    backModifyBtn = tkinter.Button(playlistArtists, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(playlistArtists,currentUser))
    backModifyBtn.grid(row=13,column=2)
    playlistArtists.mainloop()

def diverseArtistsView(View,currentUser):
    cur = con.cursor()
    diverseArtists = tkinter.Tk()
    View.destroy()
    diverseArtists.geometry("1000x500")
    for i in range(5):
        diverseArtists.columnconfigure(i,weight=1)
    diverseArtists.title("Diverse Artists")
    space00 = tkinter.Label(diverseArtists, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(diverseArtists, text="Number of Artists for Playlist")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(diverseArtists, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(diverseArtists, text="Number")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=1)
    subTitle = tkinter.Label(diverseArtists, text="Artists")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=3,column=2)
    subTitle2 = tkinter.Label(diverseArtists, text="Number of Genres")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=3,column=3)
    cur.execute("""select ar.name, count(mid.GENRE)
                from (select album.artistid as ARTISTID, track.genreid as GENRE
                from track
                join album on album.albumid = track.albumid) mid
                join artist ar on ar.artistid = mid.ARTISTID
                group by ar.name
                order by count(mid.GENRE) desc
                limit 5;""")
    rows = cur.fetchall()
    i = 4
    x = 1
    for r in rows:
        number = tkinter.Label(diverseArtists, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        playlist = tkinter.Label(diverseArtists,text=r[0])
        playlist.config(font=("Helvetica",15))
        playlist.grid(row=i,column=2)
        artists = tkinter.Label(diverseArtists,text=str(r[1]))
        artists.config(font=("Helvetica",15))
        artists.grid(row=i,column=3)
        i += 1
        x += 1
    space1 = tkinter.Label(diverseArtists, text="").grid(row=9,column=3)
    space2 = tkinter.Label(diverseArtists, text="").grid(row=10,column=3)
    backModifyBtn = tkinter.Button(diverseArtists, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(diverseArtists,currentUser))
    backModifyBtn.grid(row=11,column=2)
    diverseArtists.mainloop()

def listenSongsAdminView(View,currentUser):
    global listenSongName2
    cur = con.cursor()
    listenSongsAdmin = tkinter.Tk()
    View.destroy()
    listenSongsAdmin.geometry("1000x250")
    for i in range(5):
        listenSongsAdmin.columnconfigure(i,weight=1)
    listenSongsAdmin.title("Diverse Artists")
    space00 = tkinter.Label(listenSongsAdmin, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(listenSongsAdmin, text="LISTEN")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=1)
    windowTitle2 = tkinter.Label(listenSongsAdmin, text="SONGS")
    windowTitle2.config(font=("Helvetica",15,"bold"))
    windowTitle2.grid(row=2,column=1)
    Instruction1 = tkinter.Label(listenSongsAdmin,text="Song Name")
    Instruction1.config(font=("Helvetica",13,"bold"))
    Instruction1.grid(row=1,column=3)
    listenSongName2 = tkinter.Entry(listenSongsAdmin, font="Helvetica 10")
    listenSongName2.grid(row=2,column=3)
    listenCustomerSong = tkinter.Button(listenSongsAdmin, text="Listen Song", padx=15, pady=5, bg="#c8c8c8", command = lambda: listenAdminSongsFunction(currentUser))
    listenCustomerSong.grid(row=2,column=4)
    space1 = tkinter.Label(listenSongsAdmin, text="").grid(row=3,column=3)
    space2 = tkinter.Label(listenSongsAdmin, text="").grid(row=4,column=3)
    backModifyBtn = tkinter.Button(listenSongsAdmin, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(listenSongsAdmin,currentUser))
    backModifyBtn.grid(row=5,column=2)
    listenSongsAdmin.mainloop()

def listenSongsCustomerView(View,currentUser):
    global listenSongName
    cur = con.cursor()
    listenSongsCustomer = tkinter.Tk()
    View.destroy()
    listenSongsCustomer.geometry("1000x700")
    songs = []
    username = currentUser['name']
    dictionary = {'Username':username}
    dictionary2 = {}
    cur.execute("""select customerid 
                from customer
                where Username = %(Username)s;""",dictionary)
    customerIDS = cur.fetchall()
    for customerID in customerIDS:
        customerid = customerID[0]
        dictionary2 = {'CustomerId':customerid}
    for i in range(5):
        listenSongsCustomer.columnconfigure(i,weight=1)
    listenSongsCustomer.title("Listen Songs")
    space00 = tkinter.Label(listenSongsCustomer, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(listenSongsCustomer, text="LISTEN")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=1)
    windowTitle2 = tkinter.Label(listenSongsCustomer, text="SONGS")
    windowTitle2.config(font=("Helvetica",15,"bold"))
    windowTitle2.grid(row=2,column=1)
    Instruction1 = tkinter.Label(listenSongsCustomer,text="Song Name")
    Instruction1.config(font=("Helvetica",13,"bold"))
    Instruction1.grid(row=1,column=3)
    listenSongName = tkinter.Entry(listenSongsCustomer, font="Helvetica 10")
    listenSongName.grid(row=2,column=3)
    listenCustomerSong = tkinter.Button(listenSongsCustomer, text="Listen Song", padx=15, pady=5, bg="#c8c8c8", command = lambda: listenCustomerSongsFunction(currentUser))
    listenCustomerSong.grid(row=2,column=4)
    space0 = tkinter.Label(listenSongsCustomer, text="").grid(row=3,column=3)
    subTitle0 = tkinter.Label(listenSongsCustomer, text="Number")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=4,column=1)
    subTitle = tkinter.Label(listenSongsCustomer, text="Purchase ID")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=4,column=2)
    subTitle2 = tkinter.Label(listenSongsCustomer, text="Song Name")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=4,column=3)
    subTitle2 = tkinter.Label(listenSongsCustomer, text="Active")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=4,column=4)
    cur.execute("""select mid.INVOICELINEID, track.name, track.activa
                from (select invoiceline.invoiceid as INVOICELINEID, invoiceline.trackid as INVOICELINETRACKID
                from invoiceline) mid
                left join track on track.trackid = mid.INVOICELINETRACKID
                left join invoice on invoice.invoiceid = mid.INVOICELINEID
                where invoice.customerid = %(CustomerId)s
                limit 10;""",dictionary2)
    rows = cur.fetchall()
    i = 5
    x = 1
    for r in rows:
        number = tkinter.Label(listenSongsCustomer, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        purchaseid = tkinter.Label(listenSongsCustomer,text=str(r[0]))
        purchaseid.config(font=("Helvetica",15))
        purchaseid.grid(row=i,column=2)
        songname = tkinter.Label(listenSongsCustomer,text=r[1])
        songname.config(font=("Helvetica",15))
        songname.grid(row=i,column=3)
        if r[2] == 1:
            songactive = tkinter.Label(listenSongsCustomer,text="YES")
            songactive.config(font=("Helvetica",15))
            songactive.grid(row=i,column=4)
        elif r[2] == 2:
            songactive = tkinter.Label(listenSongsCustomer,text="NO")
            songactive.config(font=("Helvetica",15))
            songactive.grid(row=i,column=4)
        songs.append(r[1])
        i += 1
        x += 1
    space1 = tkinter.Label(listenSongsCustomer, text="").grid(row=15,column=3)
    space2 = tkinter.Label(listenSongsCustomer, text="").grid(row=16,column=3)
    backModifyBtn = tkinter.Button(listenSongsCustomer, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(listenSongsCustomer,currentUser))
    backModifyBtn.grid(row=17,column=3)
    listenSongsCustomer.mainloop()

def purchaseSongsView(View,currentUser):
    global purchaseSongName
    purchaseSongs = tkinter.Tk()
    View.destroy()
    purchaseSongs.geometry("1000x350")
    purchaseSongs.title("Purchase Songs")
    wishlist = []
    for i in range(5):
        purchaseSongs.columnconfigure(i,weight=1)
    space00 = tkinter.Label(purchaseSongs, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(purchaseSongs, text="PURCHASE")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=1)
    windowTitle2 = tkinter.Label(purchaseSongs, text="SONGS")
    windowTitle2.config(font=("Helvetica",15,"bold"))
    windowTitle2.grid(row=2,column=1)
    Instruction1 = tkinter.Label(purchaseSongs,text="Song Name")
    Instruction1.config(font=("Helvetica",13,"bold"))
    Instruction1.grid(row=1,column=3)
    purchaseSongName = tkinter.Entry(purchaseSongs, font="Helvetica 10")
    purchaseSongName.grid(row=2,column=3)
    space0 = tkinter.Label(purchaseSongs, text="").grid(row=3,column=3)
    purchaseSongsBtn = tkinter.Button(purchaseSongs, text="Add Song to Shopping Cart", padx=15, pady=5, bg="#c8c8c8", command = lambda: addSongToWishlist(currentUser,wishlist))
    purchaseSongsBtn.grid(row=4,column=2)
    space1 = tkinter.Label(purchaseSongs, text="").grid(row=5,column=3)
    purchaseSongsBtn = tkinter.Button(purchaseSongs, text="Proceed to Checkout", padx=15, pady=5, bg="#c8c8c8", command = lambda: checkoutView(purchaseSongs,currentUser,wishlist))
    purchaseSongsBtn.grid(row=6,column=2)
    space2 = tkinter.Label(purchaseSongs, text="").grid(row=7,column=3)
    backModifyBtn = tkinter.Button(purchaseSongs, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(purchaseSongs,currentUser))
    backModifyBtn.grid(row=8,column=2)
    purchaseSongs.mainloop()

def checkoutView(View,currentUser,wishlist):
    cur = con.cursor()
    checkoutView = tkinter.Tk()
    View.destroy()
    checkoutView.geometry("1000x550")
    checkoutView.title("Checkout")
    for i in range(5):
        checkoutView.columnconfigure(i,weight=1)
    space00 = tkinter.Label(checkoutView, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(checkoutView, text="CHECKOUT")
    windowTitle.config(font=("Helvetica",20,"bold"))
    windowTitle.grid(row=1,column=1)
    space0 = tkinter.Label(checkoutView, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(checkoutView, text="Number")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=1)
    subTitle = tkinter.Label(checkoutView, text="Song Name")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=3,column=2)
    subTitle2 = tkinter.Label(checkoutView, text="Price")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=3,column=3)
    x = 1
    i = 4
    totalprice = 0.00
    for song in wishlist:
        dictionary = {'Name':song}
        cur.execute("""select name, unitprice from track where name = %(Name)s limit 1;""",dictionary)
        rows = cur.fetchall()
        for r in rows:
            number = tkinter.Label(checkoutView, text=x)
            number.config(font=("Helvetica",15))
            number.grid(row=i,column=1)
            songName = tkinter.Label(checkoutView, text=r[0])
            songName.config(font=("Helvetica",15))
            songName.grid(row=i,column=2)
            price = tkinter.Label(checkoutView, text=r[1])
            price.config(font=("Helvetica",15))
            price.grid(row=i,column=3)
            i += 1
            x += 1
            songprice = r[1]
            songprice = float(songprice)
            totalprice += songprice
    space1 = tkinter.Label(checkoutView, text="").grid(row=i+1,column=2)
    totalLabel = tkinter.Label(checkoutView, text="Total: ")
    totalLabel.config(font=("Helvetica",15,"bold"))
    totalLabel.grid(row=i+2,column=2)
    totalPriceLabel = tkinter.Label(checkoutView, text=str(totalprice))
    totalPriceLabel.config(font=("Helvetica",15,"bold"))
    totalPriceLabel.grid(row=i+2,column=3)
    space2 = tkinter.Label(checkoutView, text="").grid(row=i+3,column=2)
    buySongsBtn = tkinter.Button(checkoutView, text="Buy Songs", padx=15, pady=5, bg="#c8c8c8", command = lambda: songPayment(currentUser,wishlist,totalprice))
    buySongsBtn.grid(row=i+4,column=2)
    space3 = tkinter.Label(checkoutView, text="").grid(row=i+5,column=2)
    buySongsBtn = tkinter.Button(checkoutView, text="Continue", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(checkoutView,currentUser))
    buySongsBtn.grid(row=i+6,column=2)
    checkoutView.mainloop()

def promotionView(View,currentUser):
    global searchByDate
    promotionWindow = tkinter.Tk()
    View.destroy()
    promotionWindow.geometry("650x350")
    promotionWindow.title("Promotion")
    space0 = tkinter.Label(promotionWindow, text="").pack()
    windowTitle = tkinter.Label(promotionWindow, text="PROMOTION")
    windowTitle.config(font=("Helvetica",23,"bold"))
    windowTitle.pack()
    space1 = tkinter.Label(promotionWindow, text="").pack()
    Instruction1 = tkinter.Label(promotionWindow,text="Date")
    Instruction1.config(font=("Helvetica",13,"bold"))
    Instruction1.pack()
    Instruction2 = tkinter.Label(promotionWindow,text="YYYY-MM-DD")
    Instruction2.config(font=("Helvetica",13))
    Instruction2.pack()
    searchByDate = tkinter.Entry(promotionWindow, font="Helvetica 10")
    searchByDate.pack()
    space3 = tkinter.Label(promotionWindow, text="").pack()
    searchBtn = tkinter.Button(promotionWindow, text="Search", padx=15, pady=5, bg="#c8c8c8", command = lambda: searchClients(currentUser)).pack()
    space2 = tkinter.Label(promotionWindow, text="").pack()
    backModifyBtn = tkinter.Button(promotionWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(promotionWindow,currentUser)).pack()
    promotionWindow.mainloop()

def artistSellingsView(View,currentUser):
    global artistSellingsBegDate, artistSellingsFinDate, artistSellingsLimit
    cur = con.cursor()
    artistSellingsWindow = tkinter.Tk()
    View.destroy()
    artistSellingsWindow.geometry("900x400")
    artistSellingsWindow.title("Artist Sellings")
    for i in range(5):
        artistSellingsWindow.columnconfigure(i,weight=1)
    space00 = tkinter.Label(artistSellingsWindow, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(artistSellingsWindow, text="ARTIST SELLINGS")
    windowTitle.config(font=("Helvetica",20,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(artistSellingsWindow, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(artistSellingsWindow, text="Initial Date")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=1)
    subTitle4 = tkinter.Label(artistSellingsWindow, text="YYYY-MM-DD")
    subTitle4.config(font=("Helvetica",15))
    subTitle4.grid(row=4,column=1)
    subTitle = tkinter.Label(artistSellingsWindow, text="Final Date")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=3,column=3)
    subTitle3 = tkinter.Label(artistSellingsWindow, text="YYYY-MM-DD")
    subTitle3.config(font=("Helvetica",15))
    subTitle3.grid(row=4,column=3)
    artistSellingsBegDate = tkinter.Entry(artistSellingsWindow, font="Helvetica 10")
    artistSellingsBegDate.grid(row=5,column=1)
    artistSellingsFinDate = tkinter.Entry(artistSellingsWindow, font="Helvetica 10")
    artistSellingsFinDate.grid(row=5,column=3)
    space1 = tkinter.Label(artistSellingsWindow, text="").grid(row=5,column=3)
    subTitle2 = tkinter.Label(artistSellingsWindow, text="Limit")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=6,column=2)
    artistSellingsLimit = tkinter.Entry(artistSellingsWindow, font="Helvetica 10")
    artistSellingsLimit.grid(row=7,column=2)
    space2 = tkinter.Label(artistSellingsWindow, text="").grid(row=8,column=3)
    searchBtn = tkinter.Button(artistSellingsWindow, text="Search", padx=15, pady=5, bg="#c8c8c8", command = lambda: showArtistSellingsView(artistSellingsWindow,currentUser))
    searchBtn.grid(row=9,column=2)
    space1 = tkinter.Label(artistSellingsWindow, text="").grid(row=10,column=2)
    backModifyBtn = tkinter.Button(artistSellingsWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(artistSellingsWindow,currentUser))
    backModifyBtn.grid(row=11,column=2)
    artistSellingsWindow.mainloop()

def showArtistSellingsView(View,currentUser):
    cur = con.cursor()
    showArtistSellingsWindow = tkinter.Tk()
    showArtistSellingsWindow.geometry("900x400")
    showArtistSellingsWindow.title("Artist Sellings")
    for i in range(5):
        showArtistSellingsWindow.columnconfigure(i,weight=1)
    space00 = tkinter.Label(showArtistSellingsWindow, text="").grid(row=0,column=2)
    windowTitle = tkinter.Label(showArtistSellingsWindow, text="ARTIST SELLINGS")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(showArtistSellingsWindow, text="").grid(row=2,column=2)
    Instruction1 = tkinter.Label(showArtistSellingsWindow,text="Number")
    Instruction1.config(font=("Helvetica",13,"bold"))
    Instruction1.grid(row=3,column=1)
    Instruction2 = tkinter.Label(showArtistSellingsWindow,text="Artist")
    Instruction2.config(font=("Helvetica",13,"bold"))
    Instruction2.grid(row=3,column=2)
    Instruction3 = tkinter.Label(showArtistSellingsWindow,text="Amount (Dollars)")
    Instruction3.config(font=("Helvetica",13,"bold"))
    Instruction3.grid(row=3,column=3)
    initDate = artistSellingsBegDate.get()
    finDate = artistSellingsFinDate.get()
    limit = artistSellingsLimit.get()
    limit = int(limit)
    dictionary = {'InitDate':initDate,
                  'FinDate':finDate,
                  'Limit':limit}
    cur.execute("""select track.composer, sum(invoice.total)
                from invoiceline
                left join invoice on invoice.invoiceid = invoiceline.invoiceid
                left join track on track.trackid = invoiceline.trackid
                where invoice.invoicedate > %(InitDate)s and invoice.invoicedate < %(FinDate)s
                group by track.composer
                order by sum(invoice.total) desc
                limit %(Limit)s offset 1;""",dictionary)
    rows = cur.fetchall()
    i = 4
    x = 1
    for r in rows:
        number = tkinter.Label(showArtistSellingsWindow, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        artist = tkinter.Label(showArtistSellingsWindow,text=r[0])
        artist.config(font=("Helvetica",15))
        artist.grid(row=i,column=2)
        sumatory = tkinter.Label(showArtistSellingsWindow,text=str(r[1]))
        sumatory.config(font=("Helvetica",15))
        sumatory.grid(row=i,column=3)
        i += 1
        x += 1
    space1 = tkinter.Label(showArtistSellingsWindow, text="").grid(row=i+1,column=2)
    csvBtn = tkinter.Button(showArtistSellingsWindow, text="Export To CSV", padx=15, pady=5, bg="#c8c8c8", command = lambda: exportArtistSellingsCSV(rows,currentUser))
    csvBtn.grid(row=i+2,column=2)
    space2 = tkinter.Label(showArtistSellingsWindow, text="").grid(row=i+3,column=2)
    backModifyBtn = tkinter.Button(showArtistSellingsWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(showArtistSellingsWindow,currentUser))
    backModifyBtn.grid(row=i+4,column=2)
    View.destroy()
    showArtistSellingsWindow.mainloop()

def genreSellingsView(View,currentUser):
    global genreSellingsBegDate, genreSellingsFinDate, genreSellingsLimit
    cur = con.cursor()
    genreSellingsWindow = tkinter.Tk()
    View.destroy()
    genreSellingsWindow.geometry("900x400")
    genreSellingsWindow.title("Genre Sellings")
    for i in range(5):
        genreSellingsWindow.columnconfigure(i,weight=1)
    space00 = tkinter.Label(genreSellingsWindow, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(genreSellingsWindow, text="GENRE SELLINGS")
    windowTitle.config(font=("Helvetica",20,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(genreSellingsWindow, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(genreSellingsWindow, text="Initial Date")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=1)
    subTitle4 = tkinter.Label(genreSellingsWindow, text="YYYY-MM-DD")
    subTitle4.config(font=("Helvetica",15))
    subTitle4.grid(row=4,column=1)
    subTitle = tkinter.Label(genreSellingsWindow, text="Final Date")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=3,column=3)
    subTitle3 = tkinter.Label(genreSellingsWindow, text="YYYY-MM-DD")
    subTitle3.config(font=("Helvetica",15))
    subTitle3.grid(row=4,column=3)
    genreSellingsBegDate = tkinter.Entry(genreSellingsWindow, font="Helvetica 10")
    genreSellingsBegDate.grid(row=5,column=1)
    genreSellingsFinDate = tkinter.Entry(genreSellingsWindow, font="Helvetica 10")
    genreSellingsFinDate.grid(row=5,column=3)
    space1 = tkinter.Label(genreSellingsWindow, text="").grid(row=5,column=3)
    subTitle2 = tkinter.Label(genreSellingsWindow, text="Limit")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=6,column=2)
    genreSellingsLimit = tkinter.Entry(genreSellingsWindow, font="Helvetica 10")
    genreSellingsLimit.grid(row=7,column=2)
    space2 = tkinter.Label(genreSellingsWindow, text="").grid(row=8,column=3)
    searchBtn = tkinter.Button(genreSellingsWindow, text="Search", padx=15, pady=5, bg="#c8c8c8", command = lambda: showGenreSellingsView(genreSellingsWindow,currentUser))
    searchBtn.grid(row=9,column=2)
    space1 = tkinter.Label(genreSellingsWindow, text="").grid(row=10,column=2)
    backModifyBtn = tkinter.Button(genreSellingsWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(genreSellingsWindow,currentUser))
    backModifyBtn.grid(row=11,column=2)
    genreSellingsWindow.mainloop()

def showGenreSellingsView(View,currentUser):
    cur = con.cursor()
    showGenreSellingsWindow = tkinter.Tk()
    showGenreSellingsWindow.geometry("900x400")
    showGenreSellingsWindow.title("Genre Sellings")
    for i in range(5):
        showGenreSellingsWindow.columnconfigure(i,weight=1)
    space00 = tkinter.Label(showGenreSellingsWindow, text="").grid(row=0,column=2)
    windowTitle = tkinter.Label(showGenreSellingsWindow, text="GENRE SELLINGS")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(showGenreSellingsWindow, text="").grid(row=2,column=2)
    Instruction1 = tkinter.Label(showGenreSellingsWindow,text="Number")
    Instruction1.config(font=("Helvetica",13,"bold"))
    Instruction1.grid(row=3,column=1)
    Instruction2 = tkinter.Label(showGenreSellingsWindow,text="Genre")
    Instruction2.config(font=("Helvetica",13,"bold"))
    Instruction2.grid(row=3,column=2)
    Instruction3 = tkinter.Label(showGenreSellingsWindow,text="Amount (Dollars)")
    Instruction3.config(font=("Helvetica",13,"bold"))
    Instruction3.grid(row=3,column=3)
    initDate = genreSellingsBegDate.get()
    finDate = genreSellingsFinDate.get()
    limit = genreSellingsLimit.get()
    limit = int(limit)
    dictionary = {'InitDate':initDate,
                  'FinDate':finDate,
                  'Limit':limit}
    cur.execute("""select mid.GENRENAME, sum(invoice.total)
            from invoiceline
            left join invoice on invoice.invoiceid = invoiceline.invoiceid
            left join (select track.trackid as TRACKID, genre.name AS GENRENAME
            from track
            left join genre on track.genreid = genre.genreid) mid ON mid.TRACKID = invoiceline.trackid
            where invoice.invoicedate > %(InitDate)s and invoice.invoicedate < %(FinDate)s
            group by mid.GENRENAME
            order by sum(invoice.total) desc
            limit %(Limit)s;""",dictionary)
    rows = cur.fetchall()
    i = 4
    x = 1
    for r in rows:
        number = tkinter.Label(showGenreSellingsWindow, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        genre = tkinter.Label(showGenreSellingsWindow,text=r[0])
        genre.config(font=("Helvetica",15))
        genre.grid(row=i,column=2)
        sumatory = tkinter.Label(showGenreSellingsWindow,text=str(r[1]))
        sumatory.config(font=("Helvetica",15))
        sumatory.grid(row=i,column=3)
        i += 1
        x += 1
    space1 = tkinter.Label(showGenreSellingsWindow, text="").grid(row=i+1,column=2)
    csvBtn = tkinter.Button(showGenreSellingsWindow, text="Export To CSV", padx=15, pady=5, bg="#c8c8c8", command = lambda: exportGenreSellingsCSV(rows,currentUser))
    csvBtn.grid(row=i+2,column=2)
    space2 = tkinter.Label(showGenreSellingsWindow, text="").grid(row=i+3,column=2)
    backModifyBtn = tkinter.Button(showGenreSellingsWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(showGenreSellingsWindow,currentUser))
    backModifyBtn.grid(row=i+4,column=2)
    View.destroy()
    showGenreSellingsWindow.mainloop()

def artistPlayedSongsView(View,currentUser):
    global artistPlayedSongsName, artistPlayedSongsLimit
    cur = con.cursor()
    artistPlayedSongsWindow = tkinter.Tk()
    View.destroy()
    artistPlayedSongsWindow.geometry("700x350")
    artistPlayedSongsWindow.title("Artist Playback")
    for i in range(5):
        artistPlayedSongsWindow.columnconfigure(i,weight=1)
    space00 = tkinter.Label(artistPlayedSongsWindow, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(artistPlayedSongsWindow, text="ARTIST SONG PLAYBACK")
    windowTitle.config(font=("Helvetica",20,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(artistPlayedSongsWindow, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(artistPlayedSongsWindow, text="Artist Name")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=2)
    artistPlayedSongsName = tkinter.Entry(artistPlayedSongsWindow, font="Helvetica 10")
    artistPlayedSongsName.grid(row=5,column=2)
    space2 = tkinter.Label(artistPlayedSongsWindow, text="").grid(row=6,column=3)
    subTitle2 = tkinter.Label(artistPlayedSongsWindow, text="Limit")
    subTitle2.config(font=("Helvetica",15,"bold"))
    subTitle2.grid(row=7,column=2)
    artistPlayedSongsLimit = tkinter.Entry(artistPlayedSongsWindow, font="Helvetica 10")
    artistPlayedSongsLimit.grid(row=8,column=2)
    space3 = tkinter.Label(artistPlayedSongsWindow, text="").grid(row=9,column=3)
    searchBtn = tkinter.Button(artistPlayedSongsWindow, text="Search", padx=15, pady=5, bg="#c8c8c8", command = lambda: showArtistPlayingSongsView(artistPlayedSongsWindow,currentUser))
    searchBtn.grid(row=10,column=2)
    space1 = tkinter.Label(artistPlayedSongsWindow, text="").grid(row=11,column=2)
    backModifyBtn = tkinter.Button(artistPlayedSongsWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(artistPlayedSongsWindow,currentUser))
    backModifyBtn.grid(row=12,column=2)
    artistPlayedSongsWindow.mainloop()

def showArtistPlayingSongsView(View,currentUser):
    cur = con.cursor()
    showArtistPlayingSongsWindow = tkinter.Tk()
    showArtistPlayingSongsWindow.geometry("900x400")
    showArtistPlayingSongsWindow.title("Artist Playback")
    for i in range(5):
        showArtistPlayingSongsWindow.columnconfigure(i,weight=1)
    space00 = tkinter.Label(showArtistPlayingSongsWindow, text="").grid(row=0,column=2)
    windowTitle = tkinter.Label(showArtistPlayingSongsWindow, text="ARTIST SONG PLAYBACK")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(showArtistPlayingSongsWindow, text="").grid(row=2,column=2)
    Instruction1 = tkinter.Label(showArtistPlayingSongsWindow,text="Number")
    Instruction1.config(font=("Helvetica",13,"bold"))
    Instruction1.grid(row=3,column=1)
    Instruction2 = tkinter.Label(showArtistPlayingSongsWindow,text="Song")
    Instruction2.config(font=("Helvetica",13,"bold"))
    Instruction2.grid(row=3,column=2)
    Instruction3 = tkinter.Label(showArtistPlayingSongsWindow,text="Playbacks")
    Instruction3.config(font=("Helvetica",13,"bold"))
    Instruction3.grid(row=3,column=3)
    artistName = artistPlayedSongsName.get()
    limit = artistPlayedSongsLimit.get()
    limit = int(limit)
    dictionary = {'SongsArtist':artistName,
                  'Limit':limit}
    cur.execute("""select track.name, count(songplayings.playing)
                from track
                left join songplayings on songplayings.trackid = track.trackid
                left join (select album.albumid as ALBUMID, artist.name AS ARTISTNAME
                from album
                left join artist on album.artistid = artist.artistid) mid on track.albumid = mid.ALBUMID
                where mid.ARTISTNAME = %(SongsArtist)s
                group by track.name
                order by count(songplayings.playing) desc
                LIMIT %(Limit)s;""",dictionary)
    rows = cur.fetchall()
    i = 4
    x = 1
    for r in rows:
        number = tkinter.Label(showArtistPlayingSongsWindow, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        songname = tkinter.Label(showArtistPlayingSongsWindow,text=r[0])
        songname.config(font=("Helvetica",15))
        songname.grid(row=i,column=2)
        sumatory = tkinter.Label(showArtistPlayingSongsWindow,text=str(r[1]))
        sumatory.config(font=("Helvetica",15))
        sumatory.grid(row=i,column=3)
        i += 1
        x += 1
    space1 = tkinter.Label(showArtistPlayingSongsWindow, text="").grid(row=i+1,column=2)
    csvBtn = tkinter.Button(showArtistPlayingSongsWindow, text="Export To CSV", padx=15, pady=5, bg="#c8c8c8", command = lambda: exportSongPlayingsCSV(rows,currentUser))
    csvBtn.grid(row=i+2,column=2)
    space2 = tkinter.Label(showArtistPlayingSongsWindow, text="").grid(row=i+3,column=2)
    backModifyBtn = tkinter.Button(showArtistPlayingSongsWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(showArtistPlayingSongsWindow,currentUser))
    backModifyBtn.grid(row=i+4,column=2)
    View.destroy()
    showArtistPlayingSongsWindow.mainloop()

def rangeSellingsView(View,currentUser):
    global rangeSellingsBegDate, rangeSellingsFinDate
    cur = con.cursor()
    rangeSellingsWindow = tkinter.Tk()
    View.destroy()
    rangeSellingsWindow.geometry("900x400")
    rangeSellingsWindow.title("Range Sellings")
    for i in range(5):
        rangeSellingsWindow.columnconfigure(i,weight=1)
    space00 = tkinter.Label(rangeSellingsWindow, text="").grid(row=0,column=3)
    windowTitle = tkinter.Label(rangeSellingsWindow, text="RANGE SELLINGS")
    windowTitle.config(font=("Helvetica",20,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(rangeSellingsWindow, text="").grid(row=2,column=3)
    subTitle0 = tkinter.Label(rangeSellingsWindow, text="Initial Date")
    subTitle0.config(font=("Helvetica",15,"bold"))
    subTitle0.grid(row=3,column=1)
    subTitle4 = tkinter.Label(rangeSellingsWindow, text="YYYY-MM-DD")
    subTitle4.config(font=("Helvetica",15))
    subTitle4.grid(row=4,column=1)
    subTitle = tkinter.Label(rangeSellingsWindow, text="Final Date")
    subTitle.config(font=("Helvetica",15,"bold"))
    subTitle.grid(row=3,column=3)
    subTitle3 = tkinter.Label(rangeSellingsWindow, text="YYYY-MM-DD")
    subTitle3.config(font=("Helvetica",15))
    subTitle3.grid(row=4,column=3)
    rangeSellingsBegDate = tkinter.Entry(rangeSellingsWindow, font="Helvetica 10")
    rangeSellingsBegDate.grid(row=5,column=1)
    rangeSellingsFinDate = tkinter.Entry(rangeSellingsWindow, font="Helvetica 10")
    rangeSellingsFinDate.grid(row=5,column=3)
    space1 = tkinter.Label(rangeSellingsWindow, text="").grid(row=6,column=3)
    searchBtn = tkinter.Button(rangeSellingsWindow, text="Search", padx=15, pady=5, bg="#c8c8c8", command = lambda: showRangeSellingsView(rangeSellingsWindow,currentUser))
    searchBtn.grid(row=7,column=2)
    space1 = tkinter.Label(rangeSellingsWindow, text="").grid(row=8,column=2)
    backModifyBtn = tkinter.Button(rangeSellingsWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(rangeSellingsWindow,currentUser))
    backModifyBtn.grid(row=9,column=2)
    rangeSellingsWindow.mainloop()

def showRangeSellingsView(View,currentUser):
    cur = con.cursor()
    showRangeSellingsWindow = tkinter.Tk()
    showRangeSellingsWindow.geometry("900x400")
    showRangeSellingsWindow.title("Artist Playback")
    for i in range(5):
        showRangeSellingsWindow.columnconfigure(i,weight=1)
    space00 = tkinter.Label(showRangeSellingsWindow, text="").grid(row=0,column=2)
    windowTitle = tkinter.Label(showRangeSellingsWindow, text="RANGE SELLINGS")
    windowTitle.config(font=("Helvetica",15,"bold"))
    windowTitle.grid(row=1,column=2)
    space0 = tkinter.Label(showRangeSellingsWindow, text="").grid(row=2,column=2)
    Instruction1 = tkinter.Label(showRangeSellingsWindow,text="Number")
    Instruction1.config(font=("Helvetica",13,"bold"))
    Instruction1.grid(row=3,column=1)
    Instruction2 = tkinter.Label(showRangeSellingsWindow,text="Sum")
    Instruction2.config(font=("Helvetica",13,"bold"))
    Instruction2.grid(row=3,column=2)
    beginDate = rangeSellingsBegDate.get()
    endDate = rangeSellingsFinDate.get()
    dictionary = {'BeginDate':beginDate,
                  'EndDate':endDate}
    cur.execute("""select sum(total)
            from invoice
            where invoicedate > %(BeginDate)s and invoicedate < %(EndDate)s
            limit 1;""",dictionary)
    rows = cur.fetchall()
    i = 4
    x = 1
    for r in rows:
        number = tkinter.Label(showRangeSellingsWindow, text=x)
        number.config(font=("Helvetica",15))
        number.grid(row=i,column=1)
        songname = tkinter.Label(showRangeSellingsWindow,text=r[0])
        songname.config(font=("Helvetica",15))
        songname.grid(row=i,column=2)
        i += 1
        x += 1
    space1 = tkinter.Label(showRangeSellingsWindow, text="").grid(row=i+1,column=2)
    csvBtn = tkinter.Button(showRangeSellingsWindow, text="Export To CSV", padx=15, pady=5, bg="#c8c8c8", command = lambda: exportSellingsCSV(rows,currentUser))
    csvBtn.grid(row=i+2,column=2)
    space2 = tkinter.Label(showRangeSellingsWindow, text="").grid(row=i+3,column=2)
    backModifyBtn = tkinter.Button(showRangeSellingsWindow, text="Back", padx=15, pady=5, bg="#c8c8c8", command = lambda: backToView(showRangeSellingsWindow,currentUser))
    backModifyBtn.grid(row=i+4,column=2)
    View.destroy()
    showRangeSellingsWindow.mainloop()

def randomizerView():
    randomizer = tkinter.Tk()
    randomizer.geometry("400x200")
    number = IntVar()
    optionsvar = StringVar()
    
    numberEntry = Entry(randomizer, width=8, textvariable=number)
    datevar = StringVar()
    datevar.set('2020-06-01')
    dateEntry = Entry(randomizer, width=20, textvariable=datevar)
    #   yyyy-mm-dd
    opLabel = Label(randomizer, text='Opciones')
    fechaLabel  = Label(randomizer, text='Fecha YYYY-MM-DD')
    cantidad = Label(randomizer, text='Cantidad a simular')
    randoptions = OptionMenu(randomizer, optionsvar, 'Compras', 'Reproducciones')
    randoptions.config(width=14)
    # randoptions.set('Compras')

    def decider():
        if optionsvar.get() == 'Compras':
            n = int(numberEntry.get())
            d = dateEntry.get()
            print('Deciding', n, d)
            makeRandomPurchases(n, d)
        elif optionsvar.get() == 'Reproducciones':
            n = int(numberEntry.get())
            print('Deciding', n)
            makeRandomPlays(n)

    randomButton = Button(randomizer, text='Ejecutar', width=8, command=decider)
    
    randoptions.grid(row=1, column=1)
    opLabel.grid(row=1, column=0)
    fechaLabel.grid(row=2, column=0)
    dateEntry.grid(row=2, column=1)
    cantidad.grid(row=3, column=0)
    numberEntry.grid(row=3, column=1)
    randomButton.grid(row=4, column=0)
    # backToView(adminView, currentUser)

def getRandomTracktIds(n):
    try:
        cur = con.cursor()
        cur.execute("""SELECT trackid FROM track;""")
        IDS = cur.fetchall()
        size = len(IDS) - 1
        randomIds = []
        for x in range(n):
            randomIds.append(IDS[random.randint(0, size)])
        return randomIds
    except Exception as ex:
        print(f'getRandomTracktIds exception: \n{ex}')

def getRandomCustIds(n):
    try:
        cur = con.cursor()
        cur.execute("""SELECT customerid, address, city, state, country, postalcode FROM customer;""")
        IDS = cur.fetchall()
        size = len(IDS) - 1
        randomIds = []
        # address, city, state, country, pscode
        for x in range(n):
            randomIds.append(IDS[random.randint(0, size)])
        return randomIds
    except Exception as ex:
        print(f'getRandomCustIds exception: \n{ex}')

def makeRandomPurchases(n, date):
    #   n === int
    #   date === string
    try:
        
        cur = con.cursor()
        cur.execute("""SELECT invoiceid FROM invoice order by invoiceid desc limit 1;""")
        IDS = cur.fetchall()
        last_invoice = IDS[0][0]
        cur.execute("""SELECT invoicelineid FROM invoiceline order by invoicelineid desc limit 1;""")
        IDS = cur.fetchall()
        last_invoice_line = IDS[0][0]
        track_ids = getRandomTracktIds(n)
        customer_ids = getRandomCustIds(n)
        
        #   invoice -> invoiceline
        for purchase in range(n):
            last_invoice += 1
            last_invoice_line += 1
            customer = customer_ids[purchase]
            track_id = track_ids[purchase][0]
            print('Customer ID:', customer[0], 'Bougth:', track_id)
            #   insert invoice
            cur.execute(f"""INSERT INTO invoice(invoiceid, customerid, invoicedate, billingaddress, 
                            billingcity, billingstate, billingcountry, billingpostalcode, total) 
                            VALUES({last_invoice}, {customer[0]}, '{date}', '{customer[1]}', '{customer[2]}', '{customer[3]}', 
                            '{customer[4]}', '{customer[5]}', 0.99);""")
            #   insert invoiceline
            cur.execute(f'''INSERT INTO invoiceline(invoicelineid, invoiceid, trackid, unitprice, quantity) 
                VALUES ({last_invoice_line}, {last_invoice}, {track_id}, 0.99, 1);''')

        con.commit()
        print(f'Made {n} random purchases for date: {date}')
    except Exception as ex:
        print(f'makeRandomPurchases exception: \n{ex}')

def makeRandomPlays(n):
    try:
        randomIds = []
        cur = con.cursor()
        cur.execute("""SELECT trackid FROM InvoiceLine;""")
        #   get all trackids that have been purchased
        IDS = cur.fetchall()
        size = len(IDS) - 1
        #   get random trackids to play from purchased track list
        #   insert said ids into array
        for x in range(n):
            randomIds.append(IDS[random.randint(0, size)])
        
        #   insert into songplayings table
        for _id in randomIds:
            cur.execute(f"""INSERT INTO songplayings(trackid, playing) VALUES({_id[0]}, 1);""")
            print(f'Song: {_id[0]} just played')
        
        con.commit()
        print(f'Played {n} random songs.')
    except Exception as ex:
        print(f'makeRandomPlays exception: \n{ex}')





##################################################################################################################
                                                #Programa
##################################################################################################################
    
try:
    global con
    print("\n->Connecting to DB...")
    con = psycopg2.connect(
        host = "127.0.0.1",
        database = "proyecto1",
        # database = "basesdb",
        user = "postgres",
        password = "uvg123",
        # password = "7654321.",
        port = 5432
    )
    print("->Connected Succesfully to DB!")
    print("\n->Connecting to Mongo DB...")
    MONGO_URI = 'mongodb://localhost'
    client = MongoClient(MONGO_URI)
    db = client['ProyectoBD']
    print("->Connected Succesfully to Mongo DB!")
    loginView(con)
except:
    print("->Connection to Database failed!")
    print("->Check connection settings...")
