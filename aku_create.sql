
-- Table: device
CREATE TABLE IF NOT EXISTS device (
    id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    name varchar(25) NOT NULL,
    value varchar(25) NOT NULL
);

-- Table: ste
CREATE TABLE IF NOT EXISTS ste (
    id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    name varchar(25) NOT NULL
);

-- Table: uploads
CREATE TABLE IF NOT EXISTS uploads (
    id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    ste_id integer NOT NULL,
    device_id integer NOT NULL,
    ticket varchar(25) NOT NULL,
    filename varchar(100) NOT NULL,
    username varchar(50) NOT NULL,
    action boolean NOT NULL,
    serial_number integer DEFAULT NULL,
    date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ste_id) REFERENCES ste (id),
    FOREIGN KEY (device_id) REFERENCES device (id)
);

INSERT INTO device (name, value) VALUES
	('ColdCart3', 'ColdCart3'),
	('ColdCart4', 'ColdCart4'),
	('ColdCart5', 'ColdCart5'),
	('ColdCart6', 'ColdCart6'),
	('ColdCart7', 'ColdCart7'),
	('ColdCart8', 'ColdCart8'),
	('ColdCart9', 'ColdCart9'),
	('ColdCart10', 'ColdCart10'),
	('WCA3', 'WCA3'),
	('WCA4', 'WCA4'),
	('WCA5', 'WCA5'),
	('WCA6', 'WCA6'),
	('WCA7', 'WCA7'),
	('WCA8', 'WCA8'),
	('WCA9', 'WCA9'),
	('WCA10', 'WCA10'),
	('Cryostat', 'Cryostat'),
	('DTX', 'DTX_new'),
	('IFProc', 'IFProc'),
	('LPR', 'LPR'),
	('Mount', 'Mount'),
	('PDA', 'PDA');

INSERT INTO ste (name) VALUES
	('AOS'),
	('TFINT'),
	('TFSD'),
	('TFOHG'),
	('TFENG'),
	('FE-LAB'),
	('BE-LAB');




-- End of file.

