
-- Table: device
CREATE TABLE IF NOT EXISTS device (
    id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    name varchar(25) NOT NULL,
    value varchar(25) NOT NULL,
    regex varchar(50) NOT NULL DEFAULT '.+',
    regex_message varchar(50) NOT NULL DEFAULT 'ERROR',
    scheme_file varchar(50) NOT NULL
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

DELETE FROM device;

INSERT INTO device (name, value, regex, regex_message, scheme_file)
SELECT         'ColdCart3' AS name,   'ColdCart3' AS value ,    '^\d+.xml' AS regex,          '<Number>.xml' AS regex_message,      'ColdCart3.xsd' AS scheme_file
  UNION SELECT 'ColdCart4',           'ColdCart4',              '^\d+.xml',                   '<Number>.xml',                       'ColdCart4.xsd'
	UNION SELECT 'ColdCart5',           'ColdCart5',              '^\d+.xml',                   '<Number>.xml',                       'ColdCart5.xsd'
	UNION SELECT 'ColdCart6',           'ColdCart6',              '^\d+.xml',                   '<Number>.xml',                       'ColdCart6.xsd'
	UNION SELECT 'ColdCart7',           'ColdCart7',              '^\d+.xml',                   '<Number>.xml',                       'ColdCart7.xsd'
	UNION SELECT 'ColdCart8',           'ColdCart8',              '^\d+.xml',                   '<Number>.xml',                       'ColdCart8.xsd'
	UNION SELECT 'ColdCart9',           'ColdCart9',              '^\d+.xml',                   '<Number>.xml',                       'ColdCart9.xsd'
	UNION SELECT 'ColdCart10',          'ColdCart10',             '^\d+.xml',                   '<Number>.xml',                       'ColdCart10.xsd'
	UNION SELECT 'WCA3',                'WCA3',                   '^\d+.xml',                   '<Number>.xml',                       'WCA3.xsd'
	UNION SELECT 'WCA4',                'WCA4',                   '^\d+.xml',                   '<Number>.xml',                       'WCA4.xsd'
	UNION SELECT 'WCA5',                'WCA5',                   '^\d+.xml',                   '<Number>.xml',                       'WCA5.xsd'
	UNION SELECT 'WCA6',                'WCA6',                   '^\d+.xml',                   '<Number>.xml',                       'WCA6.xsd'
	UNION SELECT 'WCA7',                'WCA7',                   '^\d+.xml',                   '<Number>.xml',                       'WCA7.xsd'
	UNION SELECT 'WCA8',                'WCA8',                   '^\d+.xml',                   '<Number>.xml',                       'WCA8.xsd'
	UNION SELECT 'WCA9',                'WCA9',                   '^\d+.xml',                   '<Number>.xml',                       'WCA9.xsd'
	UNION SELECT 'WCA10',               'WCA10',                  '^\d+.xml',                   '<Number>.xml',                       'WCA10.xsd'
	UNION SELECT 'Cryostat',            'Cryostat',               '^\d+.xml',                   '<Number>.xml',                       'Cryostat.xsd'
	UNION SELECT 'IFSwitch',            'IFSwitch',               '^\d+.xml',                   '<Number>.xml',                       'IFSwitch.xsd'
	UNION SELECT 'Mount',               'Mount',                  '^mount_[A-Z]{2}\d{2}.xml',   'mount_<Uppercase Antenna Name>.xml', 'mount'
	UNION SELECT 'IFProc',              'IFProc',                 '^IFP_Cal.xml',               'IFP_Cal.xml',                        ''
	UNION SELECT 'ACD',                 'ACD',                    '^[a-f\d]+.xml',              '<Lowercase Hexadecimal>.xml',        'ACD.xsd'
	UNION SELECT 'DTX',                 'DTX_new',                '^[a-f\d]+.xml',              '<Lowercase Hexadecimal>.xml',        'DTX.xsd'
	UNION SELECT 'WVR',                 'WVR',                    '^[a-f\d]+.xml',              '<Lowercase Hexadecimal>.xml',        'WVR.xsd'
	UNION SELECT 'PRD',                 'PRD',                    '^[a-f\d]+.xml',              '<Lowercase Hexadecimal>.xml',        'PDA.xds'
	UNION SELECT 'MLD',                 'MLD',                    '^[a-f\d]+.xml',              '<Lowercase Hexadecimal>.xml',        'PDA.xsd'
	UNION SELECT 'LFRD',                'LFRD',                   '^[a-f\d]+.xml',              '<Lowercase Hexadecimal>.xml',        'PDA.xsd'
	UNION SELECT 'LS',                  'LS',                     '^ls_[a-f\d]+.xml',           '<Lowercase Hexadecimal>.xml',        'PDA.xsd';

DELETE FROM ste;

INSERT INTO ste (name) SELECT 'AOS' AS name
  UNION SELECT 'TFINT'
  UNION SELECT 'TFSD'
  UNION SELECT 'TFOHG'
  UNION SELECT 'TFENG'
  UNION SELECT 'FE-LAB'
  UNION SELECT 'BE-LAB';





-- End of file.

