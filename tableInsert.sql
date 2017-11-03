CREATE TABLE person (
    username    VARCHAR(12),
    password    VARCHAR(14),
    firstname   VARCHAR(20),
    lastname    VARCHAR(20),
    PRIMARY KEY (username)
);

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