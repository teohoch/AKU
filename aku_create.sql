
-- Table: device
CREATE TABLE device (
    id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    name varchar(25) NOT NULL
);

-- Table: ste
CREATE TABLE ste (
    id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    name varchar(25) NOT NULL
);

-- Table: uploads
CREATE TABLE uploads (
    id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    ste_id integer NOT NULL,
    device_id integer NOT NULL,
    ticket varchar(25) NOT NULL,
    filename varchar(100) NOT NULL,
    serial_number integer,
    date datetime NOT NULL,
    FOREIGN KEY (ste_id) REFERENCES ste (id),
    FOREIGN KEY (device_id) REFERENCES device (id)
);

INSERT INTO device (name) VALUES 
	('Coldcart3'),
	('Coldcart4'),
	('Coldcart5'),
	('Coldcart6'),
	('Coldcart7'),
	('Coldcart8'),
	('Coldcart9'),
	('Coldcart10'),
	('WCA3'),
	('WCA4'),
	('WCA5'),
	('WCA6'),
	('WCA7'),
	('WCA8'),
	('WCA9'),
	('WCA10'),
	('Cryostat'),
	('DTX'),
	('IFProc'),
	('LPR'),
	('Mount'),
	('PDA');

INSERT INTO ste (name) VALUES
	('AOS'),
	('TFINT'),
	('TFSD'),
	('TFOHG'),
	('TFENG'),
	('FE-LAB'),
	('BE-LAB');




-- End of file.

