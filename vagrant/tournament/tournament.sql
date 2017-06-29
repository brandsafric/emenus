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
CREATE TABLE matches (match_id serial, player_one text, player_two text, winner text, winner_id integer);
CREATE VIEW match_winners AS SELECT match_id, winner FROM matches GROUP BY match_id, winner ORDER BY match_id ASC;
CREATE VIEW player_scores AS SELECT winner AS player, count(*) AS wins FROM match_winners GROUP BY winner ORDER BY wins DESC;

---CREATE VIEW player_scores AS SELECT total_wins, winner, count(*) AS wins FROM scores GROUP BY winner ORDER BY wins DESC;
