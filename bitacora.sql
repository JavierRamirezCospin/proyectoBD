
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
    modified_id INT NULL,
    old_values VARCHAR(810),
    new_values VARCHAR(810),
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

CREATE OR REPLACE FUNCTION track_update_insert_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;
-- DECLARE old_values VARCHAR(810);

    BEGIN
        SELECT NOW() INTO nao;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;

        IF (TG_OP = 'UPDATE') THEN
        -- old y new
            -- OLD into old_values;
            UPDATE bitacora SET verb = 'EDIT', modified = 'TRACK', modified_id = OLD.trackId, modify_date = nao, old_values = OLD, new_values = NEW WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;

        ELSIF (TG_OP = 'INSERT') THEN
        -- no old
            RAISE NOTICE 'NEW in INSERT: %', NEW.trackId;
            
            UPDATE bitacora SET verb = 'CREATE', modified = 'TRACK', modified_id = NEW.trackId, modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;
        END IF;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER track_bitacora_trigger_up_ins
    BEFORE UPDATE OR INSERT ON track 
    FOR EACH ROW EXECUTE PROCEDURE track_update_insert_bitacora();

CREATE OR REPLACE FUNCTION track_delete_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;
    BEGIN
        SELECT NOW() INTO nao;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;
		UPDATE bitacora SET verb = 'DELETE', modified = 'TRACK', modified_id = OLD.trackid, modify_date = nao WHERE _id = pos;
		EXECUTE add_user_to_bitacora(usn);
		RETURN OLD;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER track_bitacora_trigger_del 
    BEFORE DELETE ON track 
    FOR EACH ROW EXECUTE PROCEDURE track_delete_bitacora();

-- UPDATE track SET Composer = 'Johnny' WHERE TrackId = 2;

-- ARTIST

CREATE OR REPLACE FUNCTION artist_update_insert_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;

    BEGIN
        SELECT NOW() INTO nao;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;

        IF (TG_OP = 'UPDATE') THEN
        -- old y new
            
            UPDATE bitacora SET verb = 'EDIT', modified = 'ARTIST', modified_id = OLD.artistId, modify_date = nao, old_values = OLD, new_values = NEW WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;

        ELSIF (TG_OP = 'INSERT') THEN
        -- no old
            
            UPDATE bitacora SET verb = 'CREATE', modified = 'ARTIST', modified_id = NEW.artistId, modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;
        END IF;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER artist_bitacora_trigger_up_ins
    BEFORE UPDATE OR INSERT ON artist 
    FOR EACH ROW EXECUTE PROCEDURE artist_update_insert_bitacora();

CREATE OR REPLACE FUNCTION artist_delete_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;
    BEGIN
        SELECT NOW() INTO nao;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;
		UPDATE bitacora SET verb = 'DELETE', modified = 'ARTIST', modified_id = OLD.artistId, modify_date = nao WHERE _id = pos;
		EXECUTE add_user_to_bitacora(usn);
		RETURN OLD;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER artist_bitacora_trigger_del 
    BEFORE DELETE ON artist 
    FOR EACH ROW EXECUTE PROCEDURE artist_delete_bitacora();

-- ALBUM

CREATE OR REPLACE FUNCTION album_update_insert_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;

    BEGIN
        SELECT NOW() INTO nao;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;

        IF (TG_OP = 'UPDATE') THEN
        -- old y new
            
            UPDATE bitacora SET verb = 'EDIT', modified = 'ALBUM', modified_id = OLD.albumId, modify_date = nao, old_values = OLD, new_values = NEW WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;

        ELSIF (TG_OP = 'INSERT') THEN
        -- no old
            
            UPDATE bitacora SET verb = 'CREATE', modified = 'ALBUM', modified_id = NEW.albumId, modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;
        END IF;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER album_bitacora_trigger_up_ins
    BEFORE UPDATE OR INSERT ON album 
    FOR EACH ROW EXECUTE PROCEDURE album_update_insert_bitacora();

CREATE OR REPLACE FUNCTION album_delete_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;
    BEGIN
        SELECT NOW() INTO nao;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;
		UPDATE bitacora SET verb = 'DELETE', modified = 'ALBUM', modified_id = OLD.albumId, modify_date = nao WHERE _id = pos;
		EXECUTE add_user_to_bitacora(usn);
		RETURN OLD;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER album_bitacora_trigger_del 
    BEFORE DELETE ON album 
    FOR EACH ROW EXECUTE PROCEDURE album_delete_bitacora();


-- PLAYLIST

CREATE OR REPLACE FUNCTION playlist_update_insert_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;

    BEGIN
        SELECT NOW() INTO nao;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;

        IF (TG_OP = 'UPDATE') THEN
        -- old y new
            
            UPDATE bitacora SET verb = 'EDIT', modified = 'PLAYLIST', modified_id = OLD.playlistId, modify_date = nao, old_values = OLD, new_values = NEW = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;

        ELSIF (TG_OP = 'INSERT') THEN
        -- no old
            
            UPDATE bitacora SET verb = 'CREATE', modified = 'PLAYLIST', modified_id = NEW.playlistId, modify_date = nao WHERE _id = pos;
            EXECUTE add_user_to_bitacora(usn);
            RETURN NEW;
        END IF;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER playlist_bitacora_trigger_up_ins
    BEFORE UPDATE OR INSERT ON playlist 
    FOR EACH ROW EXECUTE PROCEDURE playlist_update_insert_bitacora();

CREATE OR REPLACE FUNCTION playlist_delete_bitacora()
  RETURNS TRIGGER AS
$$
DECLARE nao TIMESTAMP;
DECLARE usn VARCHAR(30);
DECLARE pos INT;
    BEGIN
        SELECT NOW() INTO nao;
        SELECT _id, username  FROM bitacora WHERE verb is null INTO pos, usn;
		UPDATE bitacora SET verb = 'DELETE', modified = 'PLAYLIST', modified_id = OLD.playlistId, modify_date = nao WHERE _id = pos;
		EXECUTE add_user_to_bitacora(usn);
		RETURN OLD;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER playlist_bitacora_trigger_del 
    BEFORE DELETE ON playlist 
    FOR EACH ROW EXECUTE PROCEDURE playlist_delete_bitacora();