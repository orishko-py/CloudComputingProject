from cassandra.cluster import Cluster
from cassandra import ReadTimeout
import uuid

cluster = Cluster(contact_points=['172.18.01'], port=9042)
cl_session = cluster.connect()

"""def startDB():
    queries = ["CREATE KEYSPACE stocksHelper WITH REPLICATION ={'class' : 'SimpleStrategy', 'replication_factor' : 1};",
           "CREATE TABLE stocksHelper.currentUsers (ID UUID, username text PRIMARY KEY, enc_password text);",
           "CREATE TABLE stocksHelper.historyLog (username text, stockIndex text PRIMARY KEY, startDate text, endDate text, prices list<float>, notes text);"]
    for q in queries:
        session.execute_async(session.prepare(q))
"""
def userSignUp(username, enc_password):
    q = """INSERT INTO stocksHelper.currentUsers
        (ID, username, enc_password)
        VALUES (?, ?, ?)"""
    cl_session.execute(cl_session.prepare(q), [uuid.uuid1(), username, enc_password])

def queryExistingUser(username):
    """use to check log in, otherwise signup"""

    q = """SELECT username, enc_password 
           FROM stocksHelper.currentUsers 
           WHERE username = '{}' 
           ALLOW FILTERING""".format(username)

    result = cl_session.execute_async(q).result()
    if len(result._current_rows)==1:
        return result[0]
    else:
        return False

def queryUserHistory(username):
    q = """SELECT stockIndex, startDate, endDate, notes  
           FROM stocksHelper.historyLog 
           WHERE username = '{}' 
           ALLOW FILTERING""".format(username)
    result = cl_session.execute_async(q).result()
    if len(result._current_rows) > 0:
        return result
    else:
        return False

def addToUserHistory(username,stockIndex, startDate, endDate, prices, notes):
    q = """INSERT INTO stocksHelper.historyLog
            (username, stockIndex, startDate, endDate, prices, notes)
            VALUES (?, ?, ?, ?, ?, ?)"""
    cl_session.execute(cl_session.prepare(q),
                    [username, stockIndex, startDate, endDate, prices, notes])

def removeFromUserHistory(username):
    pass