# delete existing values
DELETE FROM person;
DELETE FROM friendgroup;
DELETE FROM member;
DELETE FROM comment;
DELETE FROM content;
DELETE FROM share;
DELETE FROM tag;

#Initial user creation
INSERT INTO person VALUES ('BoatyMcBoatFace',md5('root'),'Boaty','McBoatFace','#ea4c88', NULL);

INSERT INTO Content (id, username, content_name, caption, public) VALUES(0, 'BoatyMcBoatFace', "ImageContent", "default pic", TRUE);
INSERT INTO ImageContent VALUES(LAST_INSERT_ID(), 'http%3A%2F%2Farrkenterprises.com%2Fwp-content%2Fuploads%2F2015%2F02%2Fempty-profile-pic.png');        #thisone

INSERT INTO person (username, password, first_name, last_name) VALUES ('AA', md5('AA'), 'Ann', 'Anderson');
INSERT INTO person (username, password, first_name, last_name) VALUES ('BB', md5('BB'), 'Bob', 'Baker');
INSERT INTO person (username, password, first_name, last_name) VALUES ('CC', md5('CC'), 'Cathy', 'Chang');
INSERT INTO person (username, password, first_name, last_name) VALUES ('DD', md5('DD'), 'David', 'Davidson');
INSERT INTO person (username, password, first_name, last_name) VALUES ('EE', md5('EE'), 'Ellen', 'Ellenberg');
INSERT INTO person (username, password, first_name, last_name) VALUES ('FF', md5('FF'), 'Fred', 'Fox');
INSERT INTO person (username, password, first_name, last_name) VALUES ('GG', md5('GG'), 'Gina', 'Gupta');
INSERT INTO person (username, password, first_name, last_name) VALUES ('HH', md5('HH'), 'Helen', 'Harper');

#inserting ann into family
INSERT INTO friendgroup VALUES ('family', 'AA', NULL);
INSERT INTO member VALUES ('AA', 'family', 'AA');
INSERT INTO member VALUES ('CC', 'family', 'AA');
INSERT INTO member VALUES ('DD', 'family', 'AA');
INSERT INTO member VALUES ('EE', 'family', 'AA');

# inserting bob into family
INSERT INTO friendgroup VALUES 	('family', 'BB', NULL);
INSERT INTO member VALUES 		('BB','family', 'BB');
INSERT INTO member VALUES 		('FF','family', 'BB');
INSERT INTO member VALUES 		('EE','family', 'BB');

# inserting ann into besties
INSERT INTO friendgroup VALUES 	('besties', 'AA', NULL);
INSERT INTO member VALUES 		('AA','besties','AA');
INSERT INTO member VALUES 		('GG','besties','AA');
INSERT INTO member VALUES 		('HH','besties','AA');

# creating friends and friend requests

INSERT INTO friends VALUES ('AA', 'BB', TRUE);
INSERT INTO friends VALUES ('CC', 'AA', FALSE);
INSERT INTO friends VALUES ('EE', 'AA', FALSE);
INSERT INTO friends VALUES ('DD', 'AA', TRUE);
INSERT INTO friends VALUES ('AA', 'FF', TRUE);
INSERT INTO friends VALUES ('GG', 'AA', TRUE);


# message
INSERT INTO Content (username, content_name, caption, public) VALUES('DD', "TextContent", "This is the caption", False);
INSERT INTO TextContent VALUES(LAST_INSERT_ID(), 'hello');
INSERT INTO Share VALUES(LAST_INSERT_ID(), 'Family', 'AA');

# gif
INSERT INTO Content (username, content_name, caption, public) VALUES('AA', "ImageContent", "bear cap", False);
INSERT INTO ImageContent VALUES(LAST_INSERT_ID(), 'https%3A%2F%2Fmedia1.tenor.com%2Fimages%2Ffde24b89a56e6bbf894cb01699a1728c%2Ftenor.gif%3Fitemid%3D5957952');
INSERT INTO Share VALUES(LAST_INSERT_ID(), 'Family', 'AA');

# still image
INSERT INTO Content (username, content_name, caption, public) VALUES('DD', "ImageContent", "grumps...", False);
INSERT INTO ImageContent VALUES(LAST_INSERT_ID(), 'https%3A%2F%2Fnews.nationalgeographic.com%2Fcontent%2Fdam%2Fnews%2Fphotos%2F000%2F755%2F75552.ngsversion.1422285553360.adapt.1900.1.jpg');
INSERT INTO Share VALUES(LAST_INSERT_ID(), 'Family', 'AA');

# video
INSERT INTO Content (username, content_name, caption, public) VALUES('AA', "VideoContent", "Penguin Caption", True);
INSERT INTO VideoContent VALUES(LAST_INSERT_ID(), 'https%3A%2F%2Fmedia.tenor.com%2Fvideos%2Fdcd24af8d7904877548cf632beeca4eb%2Fmp4');
INSERT INTO Share VALUES(LAST_INSERT_ID(), 'Family', 'AA');

# audio
INSERT INTO Content (username, content_name, caption, public) VALUES('AA', "AudioContent", "Audio Caption", True);
INSERT INTO AudioContent VALUES(LAST_INSERT_ID(), 'https://ccrma.stanford.edu/~jos/wav/pno-cs.wav');
INSERT INTO Share VALUES(LAST_INSERT_ID(), 'Family', 'AA');


# comment
INSERT INTO Comment (id, username, comment_text) VALUES(LAST_INSERT_ID(), 'DD', "the comment text :-)");
INSERT INTO Comment (id, username, comment_text) VALUES(LAST_INSERT_ID(), 'AA', "I know right?");


# favorite
INSERT INTO Favorite (id, username) VALUES(LAST_INSERT_ID(), 'DD');
INSERT INTO Favorite (id, username) VALUES(LAST_INSERT_ID(), 'AA');
INSERT INTO Favorite (id, username) VALUES(3, 'AA');

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



