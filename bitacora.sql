
/*
    Agregar a tabla permisos nuevos
    Crear nueva tabla bitacora
    insertar Funciones para agregar / eliminar 
    agregar triggers de artist/album/playlist
    
    Agregar ejecución add_to/remove al login y logout
*/

INSERT INTO permisos VALUES (11, 'Revisar Bitacora');
INSERT INTO rolesandpermisos VALUES ('Administrador', 11);

CREATE TABLE bitacora (
    _id SERIAL PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    verb VARCHAR(7) NULL,
    modified VARCHAR NULL, -- track / playlist / artist / album
    modify_date TIMESTAMP NULL,
    
);

CREATE OR REPLACE FUNCTION add_user_to_bitacora(username VARCHAR(30)) RETURNS void AS
$$
    BEGIN
        INSERT into bitacora (username) VALUES (username);
    END
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION remove_user_from_bitacora(username VARCHAR(30)) RETURNS void AS
$$
    BEGIN
        DELETE FROM bitacora WHERE username = username AND verb = null AND modified = null AND modify_date = NULL;
    END
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION track_write_to_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;
    BEGIN
        SELECT NOW() INTO nao;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;
        UPDATE bitacora SET verb = 'EDIT', modified = 'TRACK', modify_date = nao WHERE _id = pos;
        EXECUTE add_user_to_bitacora(usn);
        RETURN NEW;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER track_edit_trigger 
    BEFORE UPDATE ON track 
    EXECUTE PROCEDURE track_write_to_bitacora();

CREATE TRIGGER track_edit_trigger 
    BEFORE INSERT ON track 
    EXECUTE PROCEDURE track_write_to_bitacora();




UPDATE track SET Composer = 'Johnny' WHERE TrackId = 2;