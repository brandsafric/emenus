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