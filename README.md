# Dispatch
Dispatch is the messaging application that we made for the Databases (CS-UY 3083) Project. 

### Instructions for running the app
	0) navagate to Dispatch folder
	1) run `export FLASK_APP=main.py`
	2) run `export DB_PASS="YOUR_PASSWORD"`
	3) run `export DP_PORT=YOUR_PORTNUMBER`
	4) open MAMP/WAMP/LAMP and start the server
	5) run `flask run`
	6) do work

##### example:
```
export FLASK_APP=main.py
export DB_PASS="root"
export DB_PORT=8889
flask run
```
### port numbers: 3306 for Windows, 8889 for MacOS

### Importing / resetting the database
	run `./reset_db.sh`


### To Do List for Part 3
	1) Basic Framework
	2) Create Database
	3) Login For Everyone Should Work

### List of Features
	- Changing Admin (Only one at a time)
	- Generalized Content (actually displaying is a plus)
		-> JPG
		-> Music
		-> Stickers
		-> Gifs
		-> Videos
	- Reactions to post
	- Color picker for an individual
	- Background
	- Statistics Page (Amount of texts sent)
	- Self Deleting Messages
	- Delete Message that hasn't been seen
	- Blocking People
	- Removing people from group
	- Starring Messages

### Part 1 ER Diagram
![Part 1 ER](/docs/Part1_ER.png)
