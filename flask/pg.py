import json
import psycopg2

def get_conn():
    conn = None
    try:
        with open("./constants.json") as f:
            data = f.read()
            host = json.loads(data)['pg']['host']
            database = json.loads(data)['pg']['database']
            user = json.loads(data)['pg']['user']
            password = json.loads(data)['pg']['password']
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        return error.pgerror

def set_rule(id, logic, unit=1):
    """
    Sets rule for sensor with celsius default (1)
    """
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
                    INSERT INTO rules (id, scale, logic)
                    VALUES (%s, %s, %s);
                    """,
                    (id, logic, unit))
        conn.commit()
        cur.close()
        conn.close()

        return json.dumps({'id': str(id), 'scale': str(logic), 'unit': str(unit)})

    except (Exception, psycopg2.DatabaseError) as error:
        return json.dumps({'error': error.pgerror})

def get_rule(id):
    """
    Gets rule given id
    """
    try:
        # create a cursor
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
                    SELECT r.logic, s.unit from rules r
                    JOIN scale s on s.id = r.scale WHERE r.id = %s;
                    """,
                    (id))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res is None:
            return None
        else:
            return json.dumps({ 'logic': res[0], 'unit': res[1] })

    except (Exception, psycopg2.DatabaseError) as error:
        return json.dumps({'error': error.pgerror})

if __name__ == '__main__':
    connect()
