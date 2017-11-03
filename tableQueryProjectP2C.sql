SELECT contentID, contentName
FROM share JOIN content ON (share.contentID = content.contentID)
WHERE is_pub = TRUE OR name IN
    (SELECT name
     FROM member
     WHERE username = returnUsername('David'))

CREATE FUNCTION returnUsername (nameParameter IN VARCHAR(20))
RETURN VARCHAR(12)
BEGIN
    SELECT username
    FROM person 
    WHERE firstname = nameParameter
END returnUsername; 
