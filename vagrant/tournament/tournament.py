#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

"""Players Array"""
players = ["Homer Simpson", "Marge Simpson", "Bart Simpson", "Lisa Simpson", "Maggie Simpson",
"Mr. Burns", "Ned Flanders", "Milhouse Van", "Moe Szyslak", "Waylon Smithers", "Barney Gumble",
"Edna Krabappel", "Nelson Muntz", "Principal Skinner", "Patty Bouvier", "Ralph Wiggum"]

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    c.execute("DELETE FROM matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    return c.execute("DELETE FROM players;")



def countPlayers():
    """Returns the number of players currently registered."""
    c.execute("SELECT count(*) FROM players;")
    # DB.commit()
    rows = c.fetchall()
    return rows[0][0]



def registerPlayer(name):
    """Adds a player to the tournament database."""

    escaped = html_escape(name)
    c.execute("INSERT INTO players VALUES (DEFAULT, '{0}');".format(escaped))

    DB.commit()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    c.execute("SELECT * FROM player_standings;")
    DB.commit()
    rows = c.fetchall()
    return rows



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    c.execute("INSERT INTO matches VALUES (DEFAULT, '{0}','{1}');".format(loser, winner))
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name


    """

    c.execute("SELECT * FROM player_standings;")
    rows = c.fetchall()
    n = len(rows)/2

    for row in n:
        try:
            print row[0], row[1] + " vs. "
            print rows[rows.index(row) + 1][0], rows[rows.index(row) + 1][1]
        except:
            pass
            # print rows[n][0], rows[n][1]
            # print rows[n][0], rows[n][1]

    # n = 0
    # a = []
    # for row in rows:
    #     while n > 8:
    #         n += 1
    #         print n
    #         print row




    """

SELECT  FROM
player_standings FULL JOIN
(SELECT *
FROM player_standings
LIMIT 2)
AS top_two
ON player_standings.id = top_two.id;


SELECT player_standings1.id, player_standings1.name
from player_standings AS player_standings1
INNER JOIN player_standings AS player_standings2
ON (player_standings1.id = player_standings2.id)
WHERE player_standings1.id > player_standings2.id;

SELECT *
FROM player_standings
WHERE (ROWID,0) IN (SELECT ROWID, MOD(ROWNUM,4)
                     FROM player_standings);


SELECT pair2.id, pair2.name from
(select *
from player_standings
limit 2 OFFSET 2) AS pair2,
SELECT pair3.id, pair3.name FROM
(SELECT *
FROM player_standings
LIMIT 2 OFFSET 4) AS pair3,



    """

def pickRandom(players):
    idx = random.randrange(0, len(players))
    return players.pop(idx)

import random
import psycopg2
import re

DB = connect()
c = DB.cursor()
swissPairings()
# registerPlayer("Chandra Nalaar")
# registerPlayer("Jace Beleren")
#
#
# """ Create the Players """
# for player in players:
#     print "Adding " + player
#     registerPlayer(player)
#     print player + " added."
# DB.commit()
# c.execute("SELECT * from players")
# print c.fetchall()
#
# """ Create the pairs """
# pairs = []
# while players:
#     rand1 = pickRandom(players)
#     rand2 = pickRandom(players)
#     pair = rand1, rand2
#     pairs.append(pair)
# print pairs
#
# """ Create the initial 8 matches and the winners"""
# for pair in pairs:
#     print pair
#     winner = random.randint(0, 1)
#     print winner
#     if winner:
#         loser = pair[0]
#     else:
#         loser = pair[1]
#
#     winner = pair[winner]
#     print "Winner is " + winner
#     print "Going to grab ID of winner"
#     c.execute("SELECT id from players WHERE name = '{0}'".format(winner))
#     result = c.fetchone()
#     winner_id = result[0]
#     print winner_id
#     print "Going to grab ID of loser"
#     c.execute("SELECT id from players WHERE name = '{0}'".format(loser))
#     result = c.fetchone()
#     loser_id = result[0]
#     print loser_id
#         # c.execute("INSERT INTO matches VALUES (DEFAULT, '{0}','{1}','{2}','{3}')".format(pair[0], pair[1], winner, winner_id))
#     c.execute("INSERT INTO matches VALUES (DEFAULT, '{0}','{1}')".format(loser_id, winner_id))
#     print "Adding win to Players table"
#
# DB.commit()
# c.execute("SELECT name, match_wins from player_standings;")
# c.fetchall()
# DB.close()
