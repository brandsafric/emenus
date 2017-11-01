import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=news")

def reportTopArticles(amount):
    """Reports the top articles by visitors from the logs table.

    Args:
          amount: the number of rankings to return
    """

    query = \
        "SELECT articles.title, hits.total_hits " \
        "FROM (" \
        "SELECT COUNT(log.path) as total_hits, SUBSTRING(log.path, 10) as slug " \
        "FROM log " \
        "WHERE NOT path = '/' " \
        "GROUP BY slug " \
        "ORDER BY total_hits DESC" \
        ") AS hits " \
        "RIGHT JOIN articles ON " \
        "hits.slug = articles.slug " \
        "GROUP BY articles.title, hits.total_hits " \
        "ORDER BY hits.total_hits DESC LIMIT {0}".format(amount)
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows

def reportTopAuthors():
    query = "SELECT  authors.name, SUM(total_standings.total_hits) author_hits " \
            "FROM (" \
            "SELECT articles.author, articles.title, hits.total_hits " \
            "FROM (" \
            "SELECT COUNT(log.path) as total_hits, SUBSTRING(log.path, 10) as slug " \
            "FROM log " \
            "WHERE NOT path = '/' " \
            "GROUP BY slug " \
            "ORDER BY total_hits DESC " \
            ") as hits " \
            "RIGHT JOIN articles ON " \
            "hits.slug = articles.slug " \
            "GROUP BY articles.author, articles.title, hits.total_hits " \
            "ORDER BY hits.total_hits DESC ) as total_standings " \
            "LEFT JOIN authors " \
            "on authors.id = total_standings.author " \
            "GROUP BY authors.name " \
            " ORDER BY author_hits DESC"
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows
#
# SELECT SUBSTRING(status, 1, 4) as code, time
# FROM log
# WHERE NOT SUBSTRING(status, 1, 4) = '200'



#
# SELECT  authors.name, SUM(total_standings.total_hits) author_hits
# FROM (
# SELECT articles.author, articles.title, hits.total_hits
# FROM (
# SELECT COUNT(log.path) as total_hits, SUBSTRING(log.path, 10) as slug
# FROM log
# WHERE NOT path = '/'
# GROUP BY slug
# ORDER BY total_hits DESC
# ) as hits
# RIGHT JOIN articles ON
# hits.slug = articles.slug
# GROUP BY articles.author, articles.title, hits.total_hits
# ORDER BY hits.total_hits DESC ) as total_standings
# LEFT JOIN authors
# on authors.id = total_standings.author
# GROUP BY authors.name
# ORDER BY author_hits DESC
#
#
# SELECT players.id AS id, COUNT(match_losers.loser) AS total
# FROM players
# LEFT JOIN match_losers ON
# players.id = match_losers.loser
# GROUP BY players.id
# ) AS losses
# on wins.id = losses.id
# GROUP BY wins.id, wins.name, wins.total, losses.total
# ORDER BY wins.total DESC, wins.id;



#Table Layouts
#
# articles              authors             log
#
# author  int
# title   txt
# slug    txt
# lead    txt
# body    txt
# time    txt
# id      int           id      int         id      int
#                       bio     txt
#                       name    txt
#                                           path    txt
#                                           ip      inet
#                                           method  txt
#                                           status  txt
#                                           time    timestamp with timezone

# And here we go...
DB = connect()
c = DB.cursor()
reportTopArticles(3)
reportTopAuthors()