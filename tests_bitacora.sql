-- TRACK

INSERT INTO track (trackid, name, mediatypeID, milliseconds, unitprice) VALUES (3600, 'mysong', 2, 206005, 0.99);
UPDATE track SET Composer = 'Dogs still dont write songs' WHERE TrackId = 3600;


-- ARTIST

INSERT INTO ARTIST (artistid, name) VALUES (3600, 'mi artista favorito');
UPDATE ARTIST SET name = 'mi artist cambio de nombre' WHERE artistid = 3600;


-- ALBUM

INSERT INTO ALBUM (albumid, title, artistid) VALUES (3600, 'mi album', 3600);
UPDATE ALBUM SET title = 'mi albumz' WHERE albumid = 3600;


-- PLAYLIST

INSERT INTO PLAYLIST (playlistid, name) VALUES (3600, 'mis favs');
UPDATE PLAYLIST SET name = 'mis super favs' WHERE playlistid = 3600;


DELETE FROM track WHERE trackId= 3600;
DELETE FROM ARTIST WHERE artistid = 3600;
DELETE FROM ALBUM WHERE trackId = 3600;
DELETE FROM PLAYLIST WHERE playlistid = 3600;