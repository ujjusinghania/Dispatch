CREATE TABLE person (
    username    VARCHAR(12),
    password    VARCHAR(14),
    firstname   VARCHAR(20),
    lastname    VARCHAR(20),
    PRIMARY KEY (username)
);

CREATE TABLE friendgroup (
    name        VARCHAR(40),
    username    VARCHAR(12),
    description VARCHAR(100),
    PRIMARY KEY (username, name),
    FOREIGN KEY (username) REFERENCES person(username) ON DELETE CASCADE
);

CREATE TABLE member (
    username    VARCHAR(12),
    name        VARCHAR(40),
    PRIMARY KEY (username, name)
    FOREIGN KEY (username) REFERENCES person(username) ON DELETE CASCADE,
    FOREIGN KEY (name) REFERENCES friendgroup(name) ON DELETE CASCADE
);

CREATE TABLE comment (
    time_stamp   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    text_comment VARCHAR(500),
    username     VARCHAR(12),
    contentID    INTEGER       
    PRIMARY KEY  (username, contentID, time_stamp)
    FOREIGN KEY  (username) REFERENCES person(username) ON DELETE CASCADE,
    FOREIGN KEY  (contentID)  REFERENCES content(contentID) ON DELETE CASCADE,
);

CREATE TABLE content(
    contentID       INTEGER,
    contentDate     DATE,
    file_path       VARCHAR(50),
    contentName     VARCHAR(50),
    is_pub          BOOLEAN,
    username        VARCHAR(12),
<<<<<<< HEAD
    PRIMARY KEY (contentID),
    FOREIGN KEY (username) REFERENCES person(username) ON DELETE SET NULL 
);
=======
    PRIMARY KEY (contentID)
    FOREIGN KEY (username) REFERENCES person(username)
);

CREATE TABLE tag(
    status          Boolean,
    contentID       INTEGER,
    taggedusername        VARCHAR(12),
    taggerusername        VARCHAR(12),
    time_stamp   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (taggedusername, taggerusername, contentID)
    FOREIGN KEY (taggedusername) REFERENCES person(username)
    FOREIGN KEY (taggerusername) REFERENCES person(username)
    FOREIGN KEY (contentID) REFERENCES content(contentID)
);
>>>>>>> 24b9a32a69ee1a50b7bd8cc248075fd64ab17f43
