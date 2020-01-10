DROP DATABASE IF EXISTS bgg_inforbgg_informationmation;

Create database bgg_information;

use bgg_information;

DROP TABLE IF EXISTS  bgg_information;

CREATE TABLE IF NOT EXISTS bgg_information (
 bgg_information_key MEDIUMINT NOT NULL AUTO_INCREMENT,
 subtypename VARCHAR(15),
 itemid VARCHAR(15), #INT NOT NULL,
 objecttype VARCHAR(10),
 objectid VARCHAR(15), #INT NOT NULL,
 label VARCHAR(10),
 name VARCHAR(200) NOT NULL,
 yearpublished VARCHAR(15), #INT,
 minplayers VARCHAR(15), #INT,
 maxplayers VARCHAR(15), #INT,
 minplaytime VARCHAR(15), #INT,
 maxplaytime VARCHAR(15), #INT,
 minage VARCHAR(15), #INT,
 description VARCHAR(10000),
 bgg_stats MEDIUMINT,
 date_downloaded INT,
 PRIMARY KEY(bgg_information_key)
) ;

DROP TABLE IF EXISTS  game_stats;

CREATE TABLE IF NOT EXISTS game_stats (
 bgg_stats MEDIUMINT NOT NULL AUTO_INCREMENT,
 usersrated VARCHAR(15), #INT,
 average VARCHAR(15), #FLOAT,
 baverage VARCHAR(15), #FLOAT,
 stddev VARCHAR(15), #FLOAT,
 avgweight VARCHAR(15), #INT,
 numweights VARCHAR(15), #INT,
 numgeeklists VARCHAR(15), #INT,
 numtrading VARCHAR(15), #INT,
 numwanting VARCHAR(15), #INT,
 numwish VARCHAR(15), #INT,
 numowned VARCHAR(15), #INT,
 numprevowned VARCHAR(15), #INT,
 numcomments VARCHAR(15), #INT,
 numwishlistcomments VARCHAR(15), #INT,
 numhasparts VARCHAR(15), #INT,
 numwantparts VARCHAR(15), #INT,
 views VARCHAR(15), #INT,
 playmonth VARCHAR(15), #VARCHAR(7),
 numplays VARCHAR(15), #INT,
 numplays_month VARCHAR(15), #INT,
 numfans VARCHAR(15), #INT,
# date_downloaded DATE
 PRIMARY KEY(bgg_stats)
) ;

select * from bgg_information;

select count(*) from bgg_information;

select * from game_stats;

Select MAX(bgg_stats) from game_stats;


select l.bgg_stats,l.name,r.numplays from bgg_information as l
left join game_stats as r
on l.bgg_stats = r.bgg_stats
where name = '13 Clues'
group by l.bgg_stats;
