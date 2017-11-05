# DROP ALL TABLES
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE if exists comment     ;
DROP TABLE if exists content     ;
DROP TABLE if exists friendgroup ;
DROP TABLE if exists member		 ;
DROP TABLE if exists person		 ;
DROP TABLE if exists share		 ;
DROP TABLE if exists tag		 ;
SET FOREIGN_KEY_CHECKS = 1;

# CREATE TABLES
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
    FOREIGN KEY (name, adminusername) REFERENCES friendgroup(name, username) ON DELETE CASCADE
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
    username    VARCHAR(12),    # Username of Group Admin
    PRIMARY KEY (name, contentID),
    FOREIGN KEY (name, username) REFERENCES friendgroup(name, username) ON DELETE CASCADE,
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


# POPULATE TABLES
# delete existing values
DELETE FROM person;
DELETE FROM friendgroup;
DELETE FROM member;
DELETE FROM comment;
DELETE FROM content;
DELETE FROM share;
DELETE FROM tag;

#Initial user creation
INSERT INTO person VALUES ('AA', md5('AA'), 'Ann', 'Anderson');
INSERT INTO person VALUES ('BB', md5('BB'), 'Bob', 'Baker');
INSERT INTO person VALUES ('CC', md5('CC'), 'Cathy', 'Chang');
INSERT INTO person VALUES ('DD', md5('DD'), 'David', 'Davidson');
INSERT INTO person VALUES ('EE', md5('EE'), 'Ellen', 'Ellenberg');
INSERT INTO person VALUES ('FF', md5('FF'), 'Fred', 'Fox');
INSERT INTO person VALUES ('GG', md5('GG'), 'Gina', 'Gupta');
INSERT INTO person VALUES ('HH', md5('HH'), 'Helen', 'Harper');

#inserting ann into family
INSERT INTO friendgroup VALUES ('family','AA', NULL);
INSERT INTO member VALUES ('family','CC', 'AA');
INSERT INTO member VALUES ('family','DD', 'AA');
INSERT INTO member VALUES ('family','EE', 'AA');

# inserting bob into family
INSERT INTO friendgroup VALUES ('family', 'BB', NULL);
INSERT INTO member VALUES ('family','FF', 'BB');
INSERT INTO member VALUES ('family','EE', 'BB');

# inserting ann into besties
INSERT INTO friendgroup VALUES ('besties','AA', NULL);
INSERT INTO member VALUES ('besties','GG','AA');
INSERT INTO member VALUES ('besties','HH','AA');


# Ann​ ​posted​ ​a​ ​content​ ​item​ ​with​ ​ID=1,​ ​caption​ ​=​ ​“Whiskers”,​ ​
# is​ ​pub​ ​=​ ​False,​ ​and​ ​shared​ ​it with​ ​her​ ​“family”​ ​FriendGroup.
INSERT INTO content VALUES 
	(1, '2017-11-3', NULL, 'Whiskers', FALSE, 'AA');

INSERT INTO share VALUES (1, 'family', 'AA');


# Ann​ ​posted​ ​a​ ​content​ ​item​ ​with​ ​ID=2,​ ​caption​ ​=​ ​“My​ ​birthday​ ​party”,​ ​
# is​ ​pub​ ​=​ ​False,​ ​and shared​ ​it​ ​with​ ​her​ ​“besties”​ ​FriendGroup.
INSERT INTO content VALUES 
	(2, '2017-11-3', NULL, 'My​ ​birthday​ ​party', FALSE, 'AA');

INSERT INTO share VALUES (2, 'besties', 'AA');


# Bob​ ​posted​ ​a​ ​content​ ​item​ ​with​ ​ID=3,​ ​caption​ ​=​ ​“Rover”,​ ​
# is​ ​pub​ ​=​ ​False,​ ​and​ ​shared​ ​it with​ ​his​ ​“family”​ ​FriendGroup.
INSERT INTO content VALUES 
	(3, '2017-11-3', NULL, 'Rover', FALSE, 'BB');

INSERT INTO share VALUES (3, 'family', 'BB');



