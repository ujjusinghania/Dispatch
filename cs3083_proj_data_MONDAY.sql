-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 11, 2017 at 03:36 AM
-- Server version: 5.7.14
-- PHP Version: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs3083f17_final`
--

--
-- Dumping data for table `person`
--

INSERT INTO `person` (`username`, `password`, `first_name`, `last_name`) VALUES
('UserA', '5f4dcc3b5aa765d61d8327deb882cf99', 'Ann', 'Anderson'),
('UserB', '5f4dcc3b5aa765d61d8327deb882cf99', 'Bob', 'Baker'),
('UserC', '5f4dcc3b5aa765d61d8327deb882cf99', 'Cathy', 'Chang'),
('UserD', '5f4dcc3b5aa765d61d8327deb882cf99', 'David', 'Davidson'),
('UserE', '5f4dcc3b5aa765d61d8327deb882cf99', 'Ellen', 'Ellenberg'),
('UserF', '5f4dcc3b5aa765d61d8327deb882cf99', 'Fred', 'Fox'),
('UserFF', '5f4dcc3b5aa765d61d8327deb882cf99', 'Fred', 'Fox');

--
-- Dumping data for table `friendgroup`
--

INSERT INTO `friendgroup` (`group_name`, `username`, `description`) VALUES
('Family', 'UserC', 'My entire family'),
('Friends', 'UserC', 'All of my friends'),
('Friends', 'UserF', 'My friends'),
('Work', 'UserF', 'Some of my coworkers');

--
-- Dumping data for table `member`
--

INSERT INTO `member` (`username`, `group_name`, `username_creator`) VALUES
('UserD', 'Family', 'UserC'),
('UserE', 'Family', 'UserC'),
('UserA', 'Friends', 'UserC'),
('UserB', 'Friends', 'UserC'),
('UserF', 'Friends', 'UserC'),
('UserA', 'Friends', 'UserF'),
('UserC', 'Friends', 'UserF'),
('UserD', 'Work', 'UserF');


--
-- Dumping data for table 'friends'
--

INSERT INTO friends VALUES
('UserC', 'UserD', 1),
('UserC', 'UserE', 1),
('UserC', 'UserA', 1),
('UserC', 'UserB', 1),
('UserC', 'UserC', 1),
('UserF', 'UserA', 1),
('UserF', 'UserC', 1),
('UserF', 'UserD', 1);


--
-- Dumping data for table `content`
--
			
# REMOVE FILE_PATH, CHANGE content_name to caption, add content_name = TextContent
INSERT INTO `content` (`id`, `username`, `timest`, `caption`, `public`, `content_name`) VALUES
(1, 'UserC', '2017-12-09 18:23:37', 'Graduation', 1, 'TextContent'),
(2, 'UserC', '2017-12-09 19:12:28', 'Birthday with Friends', 0, 'TextContent'),
(3, 'UserC', '2017-12-09 20:10:29', 'Holidays with Family', 0, 'TextContent'),
(4, 'UserF', '2017-12-09 21:10:41', 'Thanksgiving', 1, 'TextContent'),
(5, 'UserF', '2017-12-09 22:52:15', 'Central Park', 0, 'TextContent'),
(6, 'UserF', '2017-12-09 23:45:14', 'Office Party', 0, 'TextContent');

# ADD TEXT_CONTENT
INSERT INTO `TextContent` (`id`, `text_content`) VALUES
(1, 'file_graduation'),
(2, 'file_birthday'),
(3, 'file_holidays'),
(4, 'path_to_thanksgiving'),
(5, 'file_path_centralpark'),
(6, 'path_work_office_party');


--
-- Dumping data for table `comment`
--

INSERT INTO `comment` (`id`, `username`, `timest`, `comment_text`) VALUES
(1, 'UserD', '2017-12-09 17:22:38', 'So proud of you!!'),
(1, 'UserE', '2017-12-09 17:22:38', 'I knew you could do it!'),
(2, 'UserC', '2017-12-09 17:25:39', 'Thank you everyone for coming!'),
(2, 'UserF', '2017-12-09 17:25:39', 'Glad I was able to come!'),
(4, 'UserC', '2017-12-09 17:30:52', 'What a wonderful Turkey!'),
(5, 'UserC', '2017-12-09 17:32:51', 'It was a great day!'),
(5, 'UserF', '2017-12-09 17:32:51', 'Had a blast!');



--
-- Dumping data for table `share`
--

INSERT INTO `share` (`id`, `group_name`, `username`) VALUES
(3, 'Family', 'UserC'),
(2, 'Friends', 'UserC'),
(5, 'Friends', 'UserF'),
(6, 'Work', 'UserF');

--
-- Dumping data for table `tag`
--

INSERT INTO `tag` (`id`, `username_tagger`, `username_taggee`, `timest`, `status`) VALUES
(1, 'UserC', 'UserD', '2017-12-10 17:00:00', 1),
(1, 'UserC', 'UserE', '2017-12-10 17:06:00', 1),
(1, 'UserC', 'UserF', '2017-12-10 18:00:00', 0),
(2, 'UserC', 'UserF', '2017-12-10 10:00:00', 1),
(3, 'UserC', 'UserD', '2017-12-10 12:00:00', 1),
(3, 'UserC', 'UserE', '2017-12-10 16:00:00', 1),
(4, 'UserF', 'UserA', '2017-12-10 14:09:00', 1),
(4, 'UserF', 'UserC', '2017-12-10 22:33:00', 1),
(5, 'UserF', 'UserC', '2017-12-10 11:00:00', 1);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
