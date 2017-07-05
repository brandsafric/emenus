#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

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
    DB.commit()
 
 
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
    # First count the number of matches played
    c.execute("SELECT * FROM matches;")
    rows = c.fetchall()
    matches = len(rows)

    c.execute("SELECT * FROM player_standings;")
    rows = c.fetchall()
    n = len(rows) - matches
    for x in range(0, n, 2):
        try:
            c.execute("INSERT INTO swiss_pairings VALUES (DEFAULT, '{0}','{1}','{2}','{3}');".format(rows[x][0], rows[x][1], rows[x + 1][0], rows[x + 1][1]))
        except:
            pass
    DB.commit()

    c.execute("SELECT player_one_id, player_one_name, player_two_id, player_two_name FROM swiss_pairings ORDER BY match LIMIT ('{0}');".format(n))
    rows = c.fetchall()
    return rows

import random
import psycopg2

DB = connect()
c = DB.cursor()
