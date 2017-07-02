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

--4 Columns player | name | match_wins | matches_played
CREATE VIEW player_standings AS
SELECT sum1.player, sum1.name, sum1.match_wins, sum4.matches_played
FROM (
SELECT players.id AS player, players.name as name, COUNT(match_winners.winner) AS match_wins
FROM players
LEFT JOIN match_winners ON
players.id = match_winners.winner
GROUP BY players.id, players.name
) sum1,
(
SELECT players.id AS player, players.name as name, COUNT(matches.loser) AS match_losers
FROM players
LEFT JOIN matches ON
players.id = matches.winner
GROUP BY players.id, players.name
) sum2,
(
SELECT players.id, COUNT(sum3.player) matches_played
FROM (
SELECT loser as player
FROM matches
UNION ALL
SELECT winner
FROM matches
) sum3
RIGHT join players on
players.id = sum3.player
GROUP BY players.id, sum3.player
ORDER BY matches_played DESC
) sum4
GROUP BY sum1.player, sum1.name, sum1.match_wins, sum4.matches_played
ORDER BY sum1.match_wins DESC, sum1.player;





