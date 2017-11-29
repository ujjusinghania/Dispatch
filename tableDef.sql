CREATE TABLE Person(
    username VARCHAR (50),
    password VARCHAR (50),
    first_name VARCHAR (50),
    last_name VARCHAR (50),
    PRIMARY KEY (username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




CREATE TABLE Content(
    id INT AUTO_INCREMENT,
    username VARCHAR (50),      # the owner of this content
    timest TIMESTAMP,           # when this content was created
    content_name VARCHAR (50),  # ContentType?
    public BOOLEAN,             #
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES Person (username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE TextContent(
    id INT,                     # content id
    text_content VARCHAR (140), # the content itself
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Content (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE FileContent(
    id INT,                     # content id
    file_path VARCHAR (100),    # path to content
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Content (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




CREATE TABLE Tag(
    id INT,
    username_tagger VARCHAR (50),
    username_taggee VARCHAR (50),
    timest TIMESTAMP,
    status BOOLEAN,
    PRIMARY KEY (id, username_tagger, username_taggee),
    FOREIGN KEY (id) REFERENCES Content(id),
    FOREIGN KEY (username_tagger) REFERENCES Person(username),
    FOREIGN KEY (username_taggee) REFERENCES Person(username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Comment(
    id INT,
    username VARCHAR (50),
    timest TIMESTAMP,
    comment_text VARCHAR (250),
    PRIMARY KEY (id, username, timest),
    FOREIGN KEY (id) REFERENCES Content(id),
    FOREIGN KEY (username) REFERENCES Person(username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE FriendGroup(
    group_name VARCHAR (50),
    username VARCHAR (50),
    description VARCHAR (50),
    PRIMARY KEY (group_name, username),
    FOREIGN KEY (username) REFERENCES Person(username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Member(
    username VARCHAR (50),
    group_name VARCHAR (50),
    username_creator VARCHAR (50),
    PRIMARY KEY (username, group_name, username_creator),
    FOREIGN KEY (username) REFERENCES Person(username),
    FOREIGN KEY (group_name, username_creator) REFERENCES FriendGroup(group_name, username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Share(
    id INT,                     # content id
    group_name VARCHAR (50),    # group name  
    username VARCHAR (50),      # group admin
    PRIMARY KEY (id, group_name, username),
    FOREIGN KEY (id) REFERENCES Content(id),
    FOREIGN KEY (group_name, username) REFERENCES FriendGroup(group_name, username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
