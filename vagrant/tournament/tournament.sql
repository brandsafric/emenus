-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament
CREATE TABLE players (id serial, name text);
CREATE TABLE matches (match serial, loser integer, winner integer);
--3 Column Table player | name | match_wins
CREATE VIEW match_winners AS
SELECT match, winner FROM matches GROUP BY match, winner ORDER BY match ASC;

CREATE VIEW match_losers AS
SELECT match, loser FROM matches GROUP BY match, loser ORDER BY match ASC;

--4 Columns player | name | match_wins | matches_played
CREATE VIEW player_standings AS
SELECT distinct wins.id, wins.name, wins.total AS wins, wins.total + losses.total as total
FROM (
SELECT players.id AS id, players.name as name, COUNT(match_winners.winner) AS total
FROM players
LEFT JOIN match_winners ON
players.id = match_winners.winner
GROUP BY players.id, players.name
) AS wins
inner join
(
SELECT players.id AS id, COUNT(match_losers.loser) AS total
FROM players
LEFT JOIN match_losers ON
players.id = match_losers.loser
GROUP BY players.id
) AS losses
on wins.id = losses.id
GROUP BY wins.id, wins.name, wins.total, losses.total
ORDER BY wins.total DESC, wins.id;


