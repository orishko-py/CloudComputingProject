from cassandra.cluster import Cluster
from cassandra import ReadTimeout
import uuid

cluster = Cluster(contact_points=['172.18.01'], port=9042)
session = cluster.connect()

"""def startDB():
    queries = ["CREATE KEYSPACE stocksHelper WITH REPLICATION ={'class' : 'SimpleStrategy', 'replication_factor' : 1};",
           "CREATE TABLE stocksHelper.currentUsers (ID UUID, username text PRIMARY KEY, enc_password text);",
           "CREATE TABLE stocksHelper.history (ID UUID PRIMARY KEY, username text, stockIndex text, startDate text, endDate text, prices list<float>, gen_headlines list<text>);"]
    for q in queries:
        session.execute_async(session.prepare(q))
"""
def userSignUp(username, enc_password):
    q = """INSERT INTO stocksHelper.currentUsers
        (ID, username, enc_password)
        VALUES (?, ?, ?)"""
    session.execute(session.prepare(q), [uuid.uuid1(), username, enc_password])

def queryExistingUser(username):
    """use to check log in, otherwise signup"""

    q = """SELECT username, enc_password 
           FROM stocksHelper.currentUsers 
           WHERE username = '{}' 
           ALLOW FILTERING""".format(username)

    result = session.execute_async(q).result()
    if len(result._current_rows)>0:
        return result[0]
    else:
        return False

"""def queryUserHistory(username):
    q = "SELECT stockIndex, startDate, endDate, prices, gen_headlines 
           FROM stocksHelper.userHistory 
           WHERE username = '{}' 
           ALLOW FILTERING".format(username)
    pass

def addToUserHistory(username):
    pass

def removeFromUserHistory(username):
    pass"""