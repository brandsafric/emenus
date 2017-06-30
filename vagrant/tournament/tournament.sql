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
CREATE VIEW match_winners AS SELECT match, winner FROM matches GROUP BY match, winner ORDER BY match ASC;
CREATE VIEW player_scores AS SELECT sum1.player, sum1.name, sum1.match_wins
FROM (
SELECT players.id AS player, players.name as name, COUNT(match_winners.winner) AS match_wins FROM players LEFT JOIN match_winners ON players.id = match_winners.winner
GROUP BY players.id, players.name
) sum1
RIGHT JOIN players
ON players.name = sum1.name ORDER BY sum1.match_wins DESC, sum1.player;

--CREATE VIEW player_scores AS SELECT winner AS player, count(*) AS wins FROM match_winners GROUP BY winner ORDER BY wins DESC;
--CREATE VIEW player_standings AS SELECT matches.winner_id AS id, matches.winner AS name, COUNT(matches.winner_id)/2 as wins, COUNT(matches.player)/2 AS matches FROM matches INNER JOIN player_scores
--    ON matches.winner = player_scores.player GROUP BY matches.winner, matches.winner_id ORDER BY matches.winner;


---CREATE VIEW player_scores AS SELECT total_wins, winner, count(*) AS wins FROM scores GROUP BY winner ORDER BY wins DESC;


--SELECT matches.winner AS id, COUNT(matches.winner_id) as wins, COUNT(matches.loser) AS matches FROM matches INNER JOIN player_scores
--    ON matches.winner = player_scores.player GROUP BY matches.winner, matches.winner_id ORDER BY matches.winner;
--
--SELECT * FROM players INNER JOIN matches on players.id =

--SELECT winner AS player, count(*) AS wins FROM match_winners INNER JOIN players ON match_winners.winner = players.id GROUP BY winner ORDER BY wins DESC;
--
--
--SELECT sum1.player, sum1.name, sum1.match_wins
--FROM (
--SELECT players.id AS player, players.name as name, COUNT(match_winners.winner) AS match_wins FROM players LEFT JOIN match_winners ON players.id = match_winners.winner
--GROUP BY players.id, players.name
--) sum1
--RIGHT JOIN players
--ON players.name = sum1.name ORDER BY sum1.match_wins DESC, sum1.player;



