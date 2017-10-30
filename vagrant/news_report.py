import psycopg2

DB = connect()
c = DB.cursor()

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=news")

