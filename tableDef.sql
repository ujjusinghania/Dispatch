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
    FOREIGN KEY (username) REFERENCES person(username)
);

CREATE TABLE member (
    username VARCHAR(12),
    name VARCHAR(40),
    PRIMARY KEY (username, name)
    FOREIGN KEY (username) REFERENCES person(username),
    FOREIGN KEY (name) REFERENCES friendgroup(name)
);

CREATE TABLE table_name (
    `time_stamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `text`       VARCHAR(500),
    FOREIGN KEY (username) REFERENCES person(username)
    FOREIGN KEY (content)  REFERENCES content(ID)
    PRIMARY KEY (username, content)
);

