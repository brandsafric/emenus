import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=news")

def reportTopArticles(amount):
    """Reports the top articles by visitors from the logs table.

    Args:
          amount: the number of rankings to return
    """
    query = "SELECT * FROM toparticles " \
            "ORDER BY hits DESC " \
            "LIMIT {0}".format(amount)
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows


def reportTopAuthors():
    query = "SELECT * FROM authorsrank"
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows

def reportDailyErrors(percent):

    if percent < 10:
        FormattedPercent = "0" + str(percent)
    else:
        FormattedPercent = str(percent)

    query = "SELECT * from dailyerrors " \
            "WHERE (errorcount / requestcount >= .{0})".format(FormattedPercent)
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows

    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows


# And here we go...
DB = connect()
c = DB.cursor()
reportTopArticles(3)
reportTopAuthors()
reportDailyErrors(1)