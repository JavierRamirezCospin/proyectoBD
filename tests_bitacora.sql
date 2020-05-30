-- TRACK

INSERT INTO track (trackid, name, mediatypeID, milliseconds, unitprice) VALUES (3602, 'mysong', 2, 206005, 0.99);
UPDATE track SET Composer = 'Dogs still dont write songs' WHERE TrackId = 3602;


-- ARTIST

INSERT INTO ARTIST (artistid, name) VALUES (290, 'mi artista favorito');
UPDATE ARTIST SET name = 'mi artist cambio de nombre' WHERE artistid = 290;


-- ALBUM

INSERT INTO ALBUM (albumid, title, artistid) VALUES (3680, 'mi album', 290);
UPDATE ALBUM SET title = 'mi albumz' WHERE albumid = 3680;


-- PLAYLIST

INSERT INTO PLAYLIST (playlistid, name) VALUES (3690, 'mis favs');
UPDATE PLAYLIST SET name = 'mis super favs' WHERE playlistid = 3690;


DELETE FROM track WHERE trackId= 3602;
DELETE FROM ALBUM WHERE albumId = 3680;
DELETE FROM ARTIST WHERE artistid = 290;
DELETE FROM PLAYLIST WHERE playlistid = 3690;