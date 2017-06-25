#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

"""Players Array"""
players = ["Homer Simpson", "Marge Simpson", "Bart Simpson", "Lisa Simpson", "Maggie Simpson",
"Mr. Burns", "Ned Flanders", "Milhouse Van", "Moe Szyslak", "Waylon Smithers", "Barney Gumble",
"Edna Krabappel", "Nelson Muntz", "Principal Skinner", "Patty Bouvier", "Ralph Wiggum"]

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    c.execute("DELETE * FROM matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    c.execute("DELETE * FROM players;")


def countPlayers():
    """Returns the number of players currently registered."""
    c.execute("SELECT count(*) FROM players;")


def registerPlayer(name):
    """Adds a player to the tournament database."""
    c.execute("INSERT INTO players (name) VALUES ('%s');" % name)

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


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
 
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


def pickRandom(players):
    idx = random.randrange(0, len(players))
    return players.pop(idx)




import random
import psycopg2
DB = connect()
c = DB.cursor()
"""countPlayers()"""
"""deletePlayers()"""

""" Create the Players """
for player in players:
    print "Adding " + player
    registerPlayer(player)
    print player + " added."
DB.commit()
c.execute("SELECT * from players")
print c.fetchall()

""" Create the pairs """
pairs = []
while players:
    rand1 = pickRandom(players)
    rand2 = pickRandom(players)
    pair = rand1, rand2
    pairs.append(pair)
print pairs

""" Create the initial 8 matches and the winners"""
for pair in pairs:
    print pair
    winner = random.randint(0, 1)
    print winner
    winner = pair[winner]
    print "Winner is " + winner
    c.execute("INSERT INTO matches VALUES (DEFAULT,'{0}','{1}','{2}')".format(pair[0], pair[1], winner))

DB.commit()

c.execute("SELECT * from matches")
print c.fetchall()

DB.close()