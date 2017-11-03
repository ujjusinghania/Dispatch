SELECT content.contentID, contentName
FROM share NATURAL JOIN content NATURAL JOIN member
WHERE is_pub = TRUE OR (member.name, adminusername) IN
    (SELECT member.name, adminusername
     FROM member
     WHERE username IN (SELECT username
    					FROM person 
    					WHERE firstname = 'David'))