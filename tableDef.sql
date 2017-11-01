CREATE TABLE person (
    username VARCHAR(12),
    password VARCHAR(14),
    firstname VARCHAR(20),
    lastname VARCHAR(20),
    PRIMARY KEY (username)
);

CREATE TABLE friendgroup (
    name VARCHAR(40),
    username VARCHAR(12),
    description VARCHAR(100),
    PRIMARY KEY (username, name),
    FOREIGN KEY (username) REFERENCES person(username) ON DELETE CASCADE
);

CREATE TABLE member (
    username VARCHAR(12),
    name VARCHAR(40),
    PRIMARY KEY (username, name)
    FOREIGN KEY (username) REFERENCES person(username) ON DELETE CASCADE,
    FOREIGN KEY (name) REFERENCES friendgroup(name) ON DELETE CASCADE
);

CREATE TABLE table_name (
    time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    text       VARCHAR(500),
    FOREIGN KEY (username) REFERENCES person(username) 
    FOREIGN KEY (content)  REFERENCES content(ID)
    PRIMARY KEY (username, content)
);

CREATE TABLE content(
    ContentID int,
    ContentDate date,
    file_path VARCHAR(50),
    ContentName VARCHAR(50),
    is_pub BOOLEAN,
    username VARCHAR(12),
    PRIMARY KEY (ContentID)
    FOREIGN KEY (username) REFERENCES person(username)
);