import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=news")

def reportTopArticles(amount):
    """Reports the top articles by visitors from the logs table.

    Args:
          amount: the number of rankings to return
    """

    # query = \
    #     "SELECT articles.title, hits.HitCount " \
    #     "FROM (" \
    #     "SELECT COUNT(log.path) as HitCount, SUBSTRING(log.path, 10) as Slug " \
    #     "FROM log " \
    #     "WHERE NOT path = '/' " \
    #     "GROUP BY Slug " \
    #     "ORDER BY HitCount DESC" \
    #     ") AS hits " \
    #     "RIGHT JOIN articles ON " \
    #     "hits.Slug = articles.slug " \
    #     "GROUP BY articles.title, hits.HitCount " \
    #     "ORDER BY hits.HitCount DESC LIMIT {0}".format(amount)
    query = "SELECT * FROM toparticles " \
            "ORDER BY hits DESC " \
            "LIMIT {0}".format(amount)
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows


def reportTopAuthors():
    query = "SELECT * FROM authorsrank"
    # query = "SELECT  authors.name, SUM(Standings.HitCount) AuthorHits " \
    #         "FROM (" \
    #         "SELECT articles.author, articles.title, Hits.HitCount " \
    #         "FROM (" \
    #         "SELECT COUNT(log.path) as HitCount, SUBSTRING(log.path, 10) as Slug " \
    #         "FROM log " \
    #         "WHERE NOT path = '/' " \
    #         "GROUP BY Slug " \
    #         "ORDER BY HitCount DESC " \
    #         ") as Hits " \
    #         "RIGHT JOIN articles ON " \
    #         "Hits.Slug = articles.slug " \
    #         "GROUP BY articles.author, articles.title, Hits.HitCount " \
    #         "ORDER BY Hits.HitCount DESC) as Standings " \
    #         "LEFT JOIN authors " \
    #         "on authors.id = Standings.author " \
    #         "GROUP BY authors.name " \
    #         "ORDER BY AuthorHits DESC"
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
    # query = "SELECT * from dailyerrors " \
    #         "WHERE (errorcount / requestcount >= .01)"
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows




    # query = "SELECT ErrorPercent.date, concat(SUBSTRING(cast(ErrorPercent.ErrorDecimal as varchar(5)), 1, 3), ' %') as ErrorDecimal " \
    #         "FROM (" \
    #         "SELECT DailyErrors.time as date, ROUND((DailyErrors.DailyErrorCount / DailyRequestCount.requests_count), 2) * 100  as ErrorDecimal " \
    #         "FROM  (" \
    #         "SELECT SUM(ErrorByDay.count) DailyErrorCount, ErrorByDay.ErrorDate as time " \
    #         "FROM ( " \
    #         "SELECT COUNT(status), DATE(time) as ErrorDate " \
    #         "FROM (" \
    #         "SELECT status, time " \
    #         "FROM log " \
    #         "WHERE status <> '200 OK' " \
    #         "GROUP BY status, time) as ErrorTimes " \
    #         "GROUP BY ErrorTimes.time, ErrorDate) as ErrorByDay " \
    #         "GROUP BY ErrorByDay.ErrorDate, ErrorByDay.count) as DailyErrors " \
    #         "LEFT JOIN (" \
    #         "SELECT COUNT(DATE(time)) requests_count, date(time) as ShortDate " \
    #         "FROM log " \
    #         "GROUP BY ShortDate) as DailyRequestCount " \
    #         "ON DailyErrors.time = DailyRequestCount.ShortDate " \
    #         "WHERE (DailyErrors.DailyErrorCount / DailyRequestCount.requests_count) >= .01) as ErrorPercent"
    # query = "SELECT * from dailyerrors " \
    #         "WHERE (errorcount / requestcount >= .01)"
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows


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
reportDailyErrors(1)