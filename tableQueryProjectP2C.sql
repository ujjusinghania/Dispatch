SELECT content.contentID, contentName
FROM share NATURAL JOIN content
WHERE is_pub = TRUE OR (name, username) IN
    (SELECT name, adminusername
     FROM member
     WHERE username IN (SELECT username
    					FROM person 
    					WHERE firstname = 'David'))