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
        "SELECT COUNT(path) as total_hits, SUBSTRING(path, 10) as article " \
        "FROM log " \
        "WHERE NOT path = '/' " \
        "GROUP BY article " \
        "ORDER BY total_hits DESC LIMIT {0}".format(amount)
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows


# SELECT hits.total_hits, hits.slug, articles.title
# FROM (
# SELECT COUNT(log.path) as total_hits, SUBSTRING(log.path, 10) as slug
# FROM log
# WHERE NOT path = '/'
# GROUP BY slug
# ORDER BY total_hits DESC
# ) AS hits
# LEFT JOIN articles ON
# hits.slug = articles.slug
# GROUP BY hits.total_hits, hits.slug, articles.title
#
#
#
#
# SELECT COUNT(path) as total_hits, SUBSTRING(path, 10) as slug
# FROM log
# WHERE NOT path = '/'
# GROUP BY slug
# ORDER BY total_hits DESC
# limit 3;

def reportTopAuthors():
    query = "SELECT COUNT(path) as total_hits, SUBSTRING(path, 10) as article " \
        "FROM log " \
        "WHERE NOT path = '/' " \
        "GROUP BY article " \
        "ORDER BY total_hits DESC LIMIT {0}".format(amount)
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows

# SELECT author, slug FROM articles
#
#
# SELECT COUNT(path) as total_hits, SUBSTRING(path, 10) as article
# FROM log
# WHERE NOT path = '/'
# GROUP BY article
# ORDER BY total_hits DESC



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
#                                           ip      txt
#                                           method  txt
#                                           status  txt
#                                           time    txt

# And here we go...
DB = connect()
c = DB.cursor()
reportTopArticles(3)