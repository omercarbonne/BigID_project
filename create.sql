create table Users (
	username VARCHAR(50) PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	password VARCHAR(100) NOT NULL
)

create table Articles (
	articleID INT PRIMARY KEY,
	title VARCHAR(200) NOT NULL,
	author VARCHAR(50) NOT NULL, 
	body TEXT NOT NULL,
	FOREIGN KEY (author) REFERENCES Users(username)
)

create table Comments (
	commentID INT PRIMARY KEY,
	title VARCHAR(200) NOT NULL,
	author VARCHAR(50) NOT NULL,
	articleID INT NOT NULL
	body TEXT NOT NULL,
	FOREIGN KEY (author) REFERENCES Users(username),
	FOREIGN KEY (articleID) REFERENCES Articles(articleID)
)
