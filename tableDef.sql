CREATE TABLE Person(
    username VARCHAR (50),
    password VARCHAR (50),
    first_name VARCHAR (50),
    last_name VARCHAR (50),
	color VARCHAR (7) DEFAULT '#ea4c88',
    profilePic INT DEFAULT 0,
    PRIMARY KEY (username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
ALTER TABLE person ADD INDEX(username);


CREATE TABLE Content(
    id INT AUTO_INCREMENT,
    username VARCHAR (50),      # the owner of this content
    timest TIMESTAMP DEFAULT CURRENT_TIMESTAMP,           # when this content was created
    content_name VARCHAR (50),  # ContentType?
    public BOOLEAN,             #
    caption TEXT,               # textual description of content
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES Person (username) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE TextContent (
    id INT,                     # content id
    text_content VARCHAR (140), # the content itself
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Content (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE ImageContent (
    id INT,
    url TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Content (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE FileContent (
    id INT,                     # content id
    file_path TEXT,             # path to content
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Content (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE VideoContent (
    id INT,                     # content id
    url TEXT,             # path to content
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Content (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE AudioContent (
    id INT,                     # content id
    url TEXT,             # path to content
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Content (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE FriendGroup
(
    group_name VARCHAR (50),
    username VARCHAR (50),
    description VARCHAR (50),
    PRIMARY KEY (group_name, username),
    FOREIGN KEY (username) REFERENCES Person(username) ON DELETE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=latin1;
ALTER TABLE friendgroup ADD INDEX(username);


CREATE TABLE Comment
(
    id INT,                         # content_id
    username VARCHAR (50),
    timest TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comment_text VARCHAR (250),
    PRIMARY KEY (id, username, timest),
    FOREIGN KEY (id) REFERENCES Content(id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Person(username) ON DELETE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE Share (
    id INT,
    group_name VARCHAR (50),
    username VARCHAR (50),
    PRIMARY KEY (id, group_name, username),
    FOREIGN KEY (id) REFERENCES Content(id) ON DELETE CASCADE,
    FOREIGN KEY (group_name, username) REFERENCES FriendGroup(group_name, username) ON DELETE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE Member (
    username VARCHAR (50),
    group_name VARCHAR (50),
    username_creator VARCHAR (50),
    PRIMARY KEY (username, group_name, username_creator),
    FOREIGN KEY (username) REFERENCES Person(username) ON DELETE CASCADE,
    FOREIGN KEY (group_name, username_creator) REFERENCES FriendGroup(group_name, username) ON DELETE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Tag (
    id INT,
    username_tagger VARCHAR (50),
    username_taggee VARCHAR (50),
    timest TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id, username_tagger, username_taggee),
    FOREIGN KEY (id) REFERENCES Content(id) ON DELETE CASCADE,
    FOREIGN KEY (username_tagger) REFERENCES Person(username) ON DELETE CASCADE, 
    FOREIGN KEY (username_taggee) REFERENCES Person(username) ON DELETE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Friends (
    friend_send_username VARCHAR (50),
    friend_receive_username VARCHAR (50),
    accepted_request BOOLEAN,
    FOREIGN KEY (friend_receive_username) REFERENCES Person(username) ON DELETE CASCADE,
    FOREIGN KEY (friend_send_username) REFERENCES Person(username) ON DELETE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE Favorite (
    id INT,
    username VARCHAR (50),
    PRIMARY KEY (id, username),
    FOREIGN KEY (id) REFERENCES Content(id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Person(username) ON DELETE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=latin1;