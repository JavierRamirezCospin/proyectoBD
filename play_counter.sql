CREATE OR REPLACE FUNCTION songplaying_insert_update()
  RETURNS TRIGGER AS
$$
DECLARE play_count INT;
DECLARE play_id INT;

    BEGIN
    
        IF (TG_OP = 'INSERT') THEN
        -- no old
            
            SELECT songplayingid, playing FROM songplayings WHERE trackId = NEW.trackId INTO play_id, play_count;
            IF play_count > 0 THEN
                SELECT play_count + 1 INTO play_count;
                UPDATE songplayings SET playing = play_count WHERE trackid = NEW.trackId AND songplayingid = play_id;
                RETURN NULL;
            END IF;
            RETURN NEW;
        END IF;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER songplaying_trigger_up_ins
    BEFORE INSERT ON songplayings 
    FOR EACH ROW EXECUTE PROCEDURE songplaying_insert_update();