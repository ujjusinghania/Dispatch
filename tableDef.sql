CREATE TABLE person (
    username    VARCHAR(12),    # Username of the person
    password    VARCHAR(100),    # MD5-hashed password
    firstname   VARCHAR(20),    # First name of person
    lastname    VARCHAR(20),    # Last name of person
    PRIMARY KEY (username)
);
ALTER TABLE person ADD INDEX(username);


CREATE TABLE friendgroup (
    name        VARCHAR(40),    # Name of the friend group
    username    VARCHAR(12),    # UserName of the admin
    description VARCHAR(100),   # Description of the friend group
    PRIMARY KEY (username, name),
    FOREIGN KEY (username) REFERENCES person(username) ON DELETE CASCADE
);
ALTER TABLE friendgroup ADD INDEX(name);

CREATE TABLE member (
    name        VARCHAR(40),    # name of the friend group
    username    VARCHAR(12),    # username of the member
    adminusername VARCHAR(12),  # username of the group admin
    PRIMARY KEY (username, name, adminusername),
    FOREIGN KEY (username) REFERENCES person(username) ON DELETE CASCADE,
    FOREIGN KEY (adminusername) REFERENCES person(username) ON DELETE CASCADE,
    FOREIGN KEY (name) REFERENCES friendgroup(name) ON DELETE CASCADE
);

CREATE TABLE content (
    contentID       INTEGER,        # ID of the content
    contentDate     DATE,           # Date content posted
    file_path       VARCHAR(50),    # Path of the content
    contentName     VARCHAR(50),    # Name of the content
    is_pub          BOOLEAN,        # Determines whether the content is public or not
    username        VARCHAR(12),    # Username of the poster
    PRIMARY KEY (contentID),
    FOREIGN KEY (username) REFERENCES person(username) ON DELETE SET NULL 
);
ALTER TABLE content ADD INDEX(contentID);


CREATE TABLE comment (
    time_stamp   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  # Timestamp
    text_comment VARCHAR(500),                                  # Content of comment
    username     VARCHAR(12),                                   # Username of commentor
    contentID    INTEGER,                                        # Content commented on
    PRIMARY KEY  (username, contentID, time_stamp),
    FOREIGN KEY  (username) REFERENCES person(username) ON DELETE CASCADE,
    FOREIGN KEY  (contentID)  REFERENCES content(contentID) ON DELETE CASCADE
);


CREATE TABLE share (
    contentID   INTEGER,        # ID of content that is being shared
    name        VARCHAR(40),    # Group that the content is being shared to
    PRIMARY KEY (name, contentID),
    FOREIGN KEY (name) REFERENCES friendgroup(name) ON DELETE CASCADE,
    FOREIGN KEY (contentID) REFERENCES content(contentID) ON DELETE CASCADE
);

CREATE TABLE tag (
    status          Boolean,        # Determines if the tag is accepted
    contentID       INTEGER,        # ID of the content
    taggedusername  VARCHAR(12),    # Username of the tagged person
    taggerusername  VARCHAR(12),    # Username of the person tagging another
    time_stamp      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, # Timestamp of the tag
    PRIMARY KEY (taggedusername, taggerusername, contentID),
    FOREIGN KEY (taggedusername) REFERENCES person(username) ON DELETE CASCADE,
    FOREIGN KEY (taggerusername) REFERENCES person(username) ON DELETE CASCADE,
    FOREIGN KEY (contentID) REFERENCES content(contentID) ON DELETE CASCADE
);
