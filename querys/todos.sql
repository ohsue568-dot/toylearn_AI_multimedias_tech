CREATE TABLE IF NOT EXISTS todo (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            item VARCHAR(255) NOT NULL
        ) ;

INSERT INTO todo (item)
VALUES ('Learn SQL');

