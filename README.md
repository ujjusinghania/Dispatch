# Dispatch
Dispatch is the messaging application that we made for the Databases (CS-UY 3083) Project. 

### Instructions for using virtual environment
	1) if you havn't yet 
		a) run `sudo pip3 install virtualenv`
		b) navigated to the project folder
		c) run `virtualenv venv`
	2) to activate the virtual environment
		a) `source venv/bin/activate` for OSX/Linux
		b) `venv\Scripts\activate` for Windows
	3) if you havn't already `pip3 install -r requirements.txt`
	4) run `export FLASK_APP=main.py`
	5) run `export DB_PASS="YOUR_PASSWORD"`
	6) run `export DP_PORT=YOUR_PORTNUMBER`
	7) open MAMP/WAMP/LAMP and start the server
	8) run `flask run`
	9) do work
	10) run `deactivate` to leave the virtual environment

```
source venv/bin/activate
export FLASK_APP=main.py
export DB_PASS="root"
export DP_PORT=8889
```


### Importing / resetting the database
	1) run `./form_reset.sh`
	2) from phpMyAdmin select the `Dispatch` database and then import the generated file `reset.sql`

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
