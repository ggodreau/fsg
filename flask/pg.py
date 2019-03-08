import json
import psycopg2

def foo():
    with open("./constants.json") as f:
        data = f.read()
        host = json.loads(data)['pg']['host']
        database = json.loads(data)['pg']['database']
        user = json.loads(data)['pg']['user']
        password = json.loads(data)['pg']['password']
    return host

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        with open("./constants.json") as f:
            data = f.read()
            host = json.loads(data)['pg']['host']
            database = json.loads(data)['pg']['database']
            user = json.loads(data)['pg']['user']
            password = json.loads(data)['pg']['password']
        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        # create a cursor
        cur = conn.cursor()

 # execute a statement
        # print('Postgres db version:')
        cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        # print(db_version)
        return(db_version[0])

     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        # print(error)
        return(error)
    # finally:
        # if conn is not None:
            # conn.close()
            # print('Database connection closed.')

if __name__ == '__main__':
    connect()
