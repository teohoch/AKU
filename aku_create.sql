
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

INSERT INTO device (name, value) SELECT 'ColdCart3' AS name, 'ColdCart3' AS value
  UNION SELECT 'ColdCart4', 'ColdCart4'
	UNION SELECT 'ColdCart5', 'ColdCart5'
	UNION SELECT 'ColdCart6', 'ColdCart6'
	UNION SELECT 'ColdCart7', 'ColdCart7'
	UNION SELECT 'ColdCart8', 'ColdCart8'
	UNION SELECT 'ColdCart9', 'ColdCart9'
	UNION SELECT 'ColdCart10', 'ColdCart10'
	UNION SELECT 'WCA3', 'WCA3'
	UNION SELECT 'WCA4', 'WCA4'
	UNION SELECT 'WCA5', 'WCA5'
	UNION SELECT 'WCA6', 'WCA6'
	UNION SELECT 'WCA7', 'WCA7'
	UNION SELECT 'WCA8', 'WCA8'
	UNION SELECT 'WCA9', 'WCA9'
	UNION SELECT 'WCA10', 'WCA10'
	UNION SELECT 'Cryostat', 'Cryostat'
	UNION SELECT 'DTX', 'DTX_new'
	UNION SELECT 'IFProc', 'IFProc'
	UNION SELECT 'LPR', 'LPR'
	UNION SELECT 'Mount', 'Mount'
	UNION SELECT 'PDA', 'PDA';

INSERT INTO ste (name) SELECT 'AOS' AS name
      UNION SELECT 'TFINT'
      UNION SELECT 'TFSD'
      UNION SELECT 'TFOHG'
      UNION SELECT 'TFENG'
      UNION SELECT 'FE-LAB'
      UNION SELECT 'BE-LAB';





-- End of file.

