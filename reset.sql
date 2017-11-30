# DROP ALL TABLES
-- SET FOREIGN_KEY_CHECKS = 0;
-- DROP TABLE if exists comment     ;
-- DROP TABLE if exists content     ;
-- DROP TABLE if exists friendgroup ;
-- DROP TABLE if exists member		 ;
-- DROP TABLE if exists person		 ;
-- DROP TABLE if exists share		 ;
-- DROP TABLE if exists tag		 ;
-- SET FOREIGN_KEY_CHECKS = 1;

DROP DATABASE if exists Dispatch;
CREATE DATABASE if not exists Dispatch;

USE Dispatch;

# CREATE TABLES
CREATE TABLE Person
(
    username VARCHAR (50),
    password VARCHAR (50),
    first_name VARCHAR (50),
    last_name VARCHAR (50),
    PRIMARY KEY (username)
) 
ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE Tag
(
    id INT,
    username_tagger VARCHAR (50),
    username_taggee VARCHAR (50),
    timest TIMESTAMP,
    status BOOLEAN,
    PRIMARY KEY (id, username_tagger, username_taggee),
    FOREIGN KEY (id) REFERENCES Content(id),
    FOREIGN KEY (username_tagger) REFERENCES Person(username),
    FOREIGN KEY (username_taggee) REFERENCES Person(username)
)
ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Comment
(
    id INT,
    username VARCHAR (50),
    timest TIMESTAMP,
    comment_text VARCHAR (250),
    PRIMARY KEY (id, username, timest),
    FOREIGN KEY (id) REFERENCES Content(id),
    FOREIGN KEY (username) REFERENCES Person(username)
)
ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE TextContent(
    id INT,                     # content id
    text_content VARCHAR (140), # the content itself
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Content (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Member
(
    username VARCHAR (50),
    group_name VARCHAR (50),
    username_creator VARCHAR (50),
    PRIMARY KEY (username, group_name, username_creator),
    FOREIGN KEY (username) REFERENCES Person(username),
    FOREIGN KEY (group_name, username_creator) REFERENCES FriendGroup(group_name, username)
)
ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Share
(
    id INT,
    group_name VARCHAR (50),
    username VARCHAR (50),
    PRIMARY KEY (id, group_name, username),
    FOREIGN KEY (id) REFERENCES Content(id),
    FOREIGN KEY (group_name, username) REFERENCES FriendGroup(group_name, username)
)
ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Friends
(
    friend_send_username VARCHAR (50),
    friend_receive_username VARCHAR (50),
    accepted_request BOOLEAN,
    FOREIGN KEY (friend_receive_username) REFERENCES Person(username),
    FOREIGN KEY (friend_send_username) REFERENCES Person(username)
)
ENGINE=InnoDB DEFAULT CHARSET=latin1

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
INSERT INTO friendgroup VALUES ('family', 'AA', NULL);
INSERT INTO member VALUES ('CC', 'family', 'AA');
INSERT INTO member VALUES ('DD', 'family', 'AA');
INSERT INTO member VALUES ('EE', 'family', 'AA');

# inserting bob into family
INSERT INTO friendgroup VALUES 	('family', 'BB', NULL);
INSERT INTO member VALUES 		('FF','family', 'BB');
INSERT INTO member VALUES 		('EE','family', 'BB');

# inserting ann into besties
INSERT INTO friendgroup VALUES 	('besties', 'AA', NULL);
INSERT INTO member VALUES 		('GG','besties','AA');
INSERT INTO member VALUES 		('HH','besties','AA');

# creating friends and friend requests

INSERT INTO friends VALUES ('AA', 'BB', TRUE);
INSERT INTO friends VALUES ('CC', 'AA', FALSE);
INSERT INTO friends VALUES ('EE', 'AA', FALSE);
INSERT INTO friends VALUES ('DD', 'AA', TRUE);
INSERT INTO friends VALUES ('AA', 'FF', TRUE);
INSERT INTO friends VALUES ('GG', 'AA', TRUE);
# Saving HH to demonstrate sending a friend request

#Testing for Tag
INSERT INTO content VALUES (1,'BB',NULL,NULL,"ASS",1)
INSERT INTO tag VALUES (1,'BB','AA', NULL,NULL)


-- # Ann​ ​posted​ ​a​ ​content​ ​item​ ​with​ ​ID=1,​ ​caption​ ​=​ ​“Whiskers”,​ ​
-- # is​ ​pub​ ​=​ ​False,​ ​and​ ​shared​ ​it with​ ​her​ ​“family”​ ​FriendGroup.
-- INSERT INTO content VALUES 
-- 	(1, '2017-11-3', NULL, 'Whiskers', FALSE, 'AA');

-- INSERT INTO share VALUES (1, 'family', 'AA');


-- # Ann​ ​posted​ ​a​ ​content​ ​item​ ​with​ ​ID=2,​ ​caption​ ​=​ ​“My​ ​birthday​ ​party”,​ ​
-- # is​ ​pub​ ​=​ ​False,​ ​and shared​ ​it​ ​with​ ​her​ ​“besties”​ ​FriendGroup.
-- INSERT INTO content VALUES 
-- 	(2, '2017-11-3', NULL,'My​ ​birthday​ ​party', FALSE, 'AA');

-- INSERT INTO share VALUES (2, 'besties', 'AA');


-- # Bob​ ​posted​ ​a​ ​content​ ​item​ ​with​ ​ID=3,​ ​caption​ ​=​ ​“Rover”,​ ​
-- # is​ ​pub​ ​=​ ​False,​ ​and​ ​shared​ ​it with​ ​his​ ​“family”​ ​FriendGroup.
-- INSERT INTO content VALUES 
-- 	(3, '2017-11-3', NULL, 'Rover', FALSE, 'BB');

-- INSERT INTO share VALUES (3, 'family', 'BB');



