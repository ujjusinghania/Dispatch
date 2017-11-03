DELETE FROM person;
DELETE FROM friendgroup;
DELETE FROM member;
DELETE FROM comment;
DELETE FROM content;
DELETE FROM share;
DELETE FROM tag;

INSERT INTO person VALUES ('AA', md5('AA'), 'Ann', 'Anderson');
INSERT INTO person VALUES ('BB', md5('BB'), 'Bob', 'Baker');
INSERT INTO person VALUES ('CC', md5('CC'), 'Cathy', 'Chang');
INSERT INTO person VALUES ('DD', md5('DD'), 'David', 'Davidson');
INSERT INTO person VALUES ('EE', md5('EE'), 'Ellen', 'Ellenberg');
INSERT INTO person VALUES ('FF', md5('FF'), 'Fred', 'Fox');
INSERT INTO person VALUES ('GG', md5('GG'), 'Gina', 'Gupta');
INSERT INTO person VALUES ('HH', md5('HH'), 'Helen', 'Harper');

#inserting both ann and bob into groups
INSERT INTO friendgroup VALUES ('family','AA')
INSERT INTO member VALUES ('family','CC')
INSERT INTO member VALUES ('family','DD')
INSERT INTO member VALUES ('family','EE')
INSERT INTO friendgroup VALUES ('family','BB')
INSERT INTO member VALUES ('family','FF')
INSERT INTO member VALUES ('family','EE')
INSERT INTO friendgroup VALUES ('besties','AA')
INSERT INTO member VALUES ('besties','GG')
INSERT INTO member VALUES ('besties','HH')


# Ann​ ​posted​ ​a​ ​content​ ​item​ ​with​ ​ID=1,​ ​caption​ ​=​ ​“Whiskers”,​ ​
# is​ ​pub​ ​=​ ​False,​ ​and​ ​shared​ ​it with​ ​her​ ​“family”​ ​FriendGroup.
INSERT INTO content VALUES 
	(1, TO_DATE('11/3/17', 'MM/DD/YY'), NULL, 'Whiskers', FALSE, 'AA');

INSERT INTO share VALUES (1, 'family');



