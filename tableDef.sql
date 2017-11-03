CREATE TABLE person (
    username    VARCHAR(12),    # Username of the person
    password    VARCHAR(14),    # MD5-hashed password
    firstname   VARCHAR(20),    # First name of person
    lastname    VARCHAR(20),    # Last name of person
    PRIMARY KEY (username)
);

CREATE TABLE friendgroup (
    name        VARCHAR(40),    # Name of the friend group
    username    VARCHAR(12),    # UserName of the admin
    description VARCHAR(100),   # Description of the friend group
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
    time_stamp   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  # Timestamp
    text_comment VARCHAR(500),                                  # Content of comment
    username     VARCHAR(12),                                   # Username of commentor
    contentID    INTEGER                                        # Content commented on
    PRIMARY KEY  (username, contentID, time_stamp)
    FOREIGN KEY  (username) REFERENCES person(username) ON DELETE CASCADE,
    FOREIGN KEY  (contentID)  REFERENCES content(contentID) ON DELETE CASCADE,
);

CREATE TABLE content (
    contentID       INTEGER,
    contentDate     DATE,
    file_path       VARCHAR(50),
    contentName     VARCHAR(50),
    is_pub          BOOLEAN,
    username        VARCHAR(12),
    PRIMARY KEY (contentID),
    FOREIGN KEY (username) REFERENCES person(username) ON DELETE SET NULL 
);

CREATE TABLE share (
    contentID   INTEGER,
    name        VARCHAR(40),
    PRIMARY KEY (name, contentID),
    FOREIGN KEY (name) REFERENCES friendgroup(name) ON DELETE CASCADE,
    FOREIGN KEY (contentID) REFERENCES content(contentID) ON DELETE CASCADE
);

CREATE TABLE tag (
    status          Boolean,
    contentID       INTEGER,
    taggedusername  VARCHAR(12),
    taggerusername  VARCHAR(12),
    time_stamp      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (taggedusername, taggerusername, contentID)
    FOREIGN KEY (taggedusername) REFERENCES person(username) ON DELETE NULL,
    FOREIGN KEY (taggerusername) REFERENCES person(username) ON DELETE NULL,
    FOREIGN KEY (contentID) REFERENCES content(contentID) ON DELETE CASCADE
);
