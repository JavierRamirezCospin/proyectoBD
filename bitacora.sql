
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
    _object VARCHAR NULL, -- track / playlist / artist / album
    -- _object_id INT NULL,
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

CREATE OR REPLACE FUNCTION track_update_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;
DECLARE mod_id INT;
    BEGIN
        SELECT NOW() INTO nao;
        SELECT trackid from track where trackid= OLD.TrackId INTO mod_id;
        -- mod_id = OLD.TrackId;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;
        IF (TG_OP = 'DELETE') THEN
            UPDATE bitacora SET verb = 'DELETE', modified = 'TRACK', modified_id = mod_id, modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;

        ELSIF (TG_OP = 'UPDATE') THEN
            UPDATE bitacora SET verb = 'EDIT', modified = 'TRACK', modified_id = mod_id, modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;

        ELSIF (TG_OP = 'INSERT') THEN
            UPDATE bitacora SET verb = 'CREATE', modified = 'TRACK', modified_id = mod_id, modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;
        END IF;
        -- RETURN NEW;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER track_bitacora_trigger 
    BEFORE UPDATE OR INSERT OR DELETE ON track 
    EXECUTE PROCEDURE track_update_bitacora();

UPDATE track SET Composer = 'Johnny' WHERE TrackId = 2;

-- ARTIST

CREATE OR REPLACE FUNCTION artist_update_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;
    BEGIN
        SELECT NOW() INTO nao;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;
        IF (TG_OP = 'DELETE') THEN
            UPDATE bitacora SET verb = 'DELETE', modified = 'ARTIST', modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;

        ELSIF (TG_OP = 'UPDATE') THEN
            UPDATE bitacora SET verb = 'EDIT', modified = 'ARTIST', modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;

        ELSIF (TG_OP = 'INSERT') THEN
            UPDATE bitacora SET verb = 'CREATE', modified = 'ARTIST', modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;
        END IF;
        -- RETURN NEW;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER artist_bitacora_trigger 
    BEFORE UPDATE OR INSERT OR DELETE ON artist 
    EXECUTE PROCEDURE artist_update_bitacora();



-- ALBUM

CREATE OR REPLACE FUNCTION album_update_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;
    BEGIN
        SELECT NOW() INTO nao;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;
        IF (TG_OP = 'DELETE') THEN
            UPDATE bitacora SET verb = 'DELETE', modified = 'ALBUM', modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;

        ELSIF (TG_OP = 'UPDATE') THEN
            UPDATE bitacora SET verb = 'EDIT', modified = 'ALBUM', modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;

        ELSIF (TG_OP = 'INSERT') THEN
            UPDATE bitacora SET verb = 'CREATE', modified = 'ALBUM', modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;
        END IF;
        -- RETURN NEW;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER album_bitacora_trigger 
    BEFORE UPDATE OR INSERT OR DELETE ON album 
    EXECUTE PROCEDURE album_update_bitacora();


-- PLAYLIST

CREATE OR REPLACE FUNCTION playlist_update_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;
    BEGIN
        SELECT NOW() INTO nao;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;
        IF (TG_OP = 'DELETE') THEN
            UPDATE bitacora SET verb = 'DELETE', modified = 'PLAYLIST', modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;

        ELSIF (TG_OP = 'UPDATE') THEN
            UPDATE bitacora SET verb = 'EDIT', modified = 'PLAYLIST', modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;

        ELSIF (TG_OP = 'INSERT') THEN
            UPDATE bitacora SET verb = 'CREATE', modified = 'PLAYLIST', modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;
        END IF;
        -- RETURN NEW;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER playlist_bitacora_trigger 
    BEFORE UPDATE OR INSERT OR DELETE ON playlist 
    EXECUTE PROCEDURE playlist_update_bitacora();