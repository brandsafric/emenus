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
    print "Length of matches is " + str(matches)


    c.execute("SELECT * FROM player_standings;")
    rows = c.fetchall()
    # print rows
    n = len(rows) - matches
    print "length of rows - matches = " + str(n)
    for x in range(0, n, 2):
        print "x is currently at " + str(x)
        try:
            # print "Trying to add"
            c.execute("INSERT INTO swiss_pairings VALUES (DEFAULT, '{0}','{1}','{2}','{3}');".format(rows[x][0], rows[x][1], rows[x + 1][0], rows[x + 1][1]))
            DB.commit()
        except:
            pass
    DB.commit()

    c.execute("SELECT player_one_id, player_one_name, player_two_id, player_two_name FROM swiss_pairings ORDER BY match LIMIT ('{0}');".format(n))
    rows = c.fetchall()
    return rows
    # for x in range(0, n, 2):
    #     try:
    #         print rows[x][0], rows[x][1] + " vs. "
    #         print rows[x + 1][0], rows[x + 1][1]
    #     except:
    #         pass


def pickRandom(players):
    idx = random.randrange(0, len(players))
    return players.pop(idx)

import random
import psycopg2
import re

DB = connect()
c = DB.cursor()

# Test commands
# registerPlayer("Twilight Sparkle")
# registerPlayer("Fluttershy")
# registerPlayer("Applejack")
# registerPlayer("Pinkie Pie")
# registerPlayer("Rarity")
# registerPlayer("Rainbow Dash")
# registerPlayer("Princess Celestia")
# registerPlayer("Princess Luna")
# standings = playerStandings()
# [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
# print "standings : " + str(standings)
# pairings = swissPairings()
# print pairings
# print len(pairings)
# reportMatch(id1, id2)
# reportMatch(id3, id4)
# reportMatch(id5, id6)
# reportMatch(id7, id8)
# pairings = swissPairings()
# print len(pairings)
# [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
# possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
#                       frozenset([id1, id7]), frozenset([id3, id5]),
#                       frozenset([id3, id7]), frozenset([id5, id7]),
#                       frozenset([id2, id4]), frozenset([id2, id6]),
#                       frozenset([id2, id8]), frozenset([id4, id6]),
#                       frozenset([id4, id8]), frozenset([id6, id8]),
#                       frozenset([id1, id2]), frozenset([id3, id4]),
#                       frozenset([id5, id6]), frozenset([id7, id8])
#                       ])
# print "pairings = " + str(pairings)
# print "pissible_pairs = " + str(possible_pairs)
# actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
# print "acutal_pairs = " + str(actual_pairs)
#
# for pair in actual_pairs:
#     print "pair is :" + str(pair)
#     if pair not in possible_pairs:
#         print "possible_pairs = " + str(possible_pairs)
#         raise ValueError(
#             "After one match, players with one win should be paired.")
#
#
""" Create the Players """
# for player in players:
#     # print "Adding " + player
#     registerPlayer(player)
#     # print player + " added."
# DB.commit()
# c.execute("SELECT * from players")
# print c.fetchall()

# swissPairings()
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
