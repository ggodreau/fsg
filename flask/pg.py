import json
import psycopg2
from flask import request, jsonify

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

def print_payload(payload):
    content = payload.json
    print(content['id'])
    print(content['scale'])
    print(content['logic'], type(content['logic']))
    print(content['templ'], type(content['templ']))
    print(content['temph'])
    return json.dumps({'foo': 1})

def set_rule(payload):
    """
    Sets rule for sensor with celsius default (1)
    """
    content = payload.json

    # id = None
    # logic = None
    # templ = None
    # temph = None
    # scale = None

    print("entered setrule section")
    # parse id field
    try:
        print("entered id parsing section")
        id = str(content['id'])
    except:
        return json.dumps({'error': 'invalid or missing id parameter'})

    # parse temp scale
    try:
        print("entered scale parsing section")
        scale = int(content['scale'])
        # validate scale is celsius or farenheit, respetctively
        if scale not in [0, 1]:
            return json.dumps({'error': 'invalid scale parameter'})
    # assume a default of celsius if scale is missing
    except KeyError:
        scale = 0

    # parse logic field
    try:
        print("entered logic parsing section")
        logic = int(content['logic'])
        # if greater than logic, must have templ
        if logic == 0:
            print("entered logic 0 section")
            try:
                templ = content['templ']
                # set to an empty string to become a NULL upon db write
                temph = ''
            except Keyerror:
                return json.dumps({'error': 'low temp needed for greater than logic'})
        # if less than logic, must have temph
        elif logic == 1:
            print("entered logic 1 section")
            try:
                print("entered temph")
                temph = content['temph']
                print("entered templ")
                # set to an empty string to become a NULL upon db write
                templ = ''
                print("finished templ")
            except Keyerror:
                return json.dumps({'error': 'high temp needed for less than logic'})
        # if OOB logic, must have both low and high temp limits
        elif logic == 2:
            print("entered logic 2 section")
            try:
                templ = content['templ']
                temph = content['temph']
            except Keyerror:
                return json.dumps({'error': 'both low and high temp needed for OOB logic'})
            if templ >= temph:
                return json.dumps({'error': 'lower temp limit cannot be greater than or equal to upper temp limit'})
        else:
            return json.dumps({'error': 'invalid logic parameter'})
    except Keyerror:
        return json.dumps({'error': 'missing logic parameter'})

    print('to be written: ', id, scale, logic, templ, temph)

    # finally write the rule to the db
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
                    INSERT INTO rules (id, scale, logic, templ, temph)
                    VALUES (%s, %s, %s, NULLIF(CAST(%s AS TEXT), '')::numeric, NULLIF(CAST(%s AS TEXT), '')::numeric);
                    """,
                    (id, logic, scale, templ, temph))
        conn.commit()
        cur.close()
        conn.close()

        return json.dumps({'id': id, 'scale': logic, 'logic': logic, 'templ': templ, 'temph': temph})

    except (Exception, psycopg2.IntegrityError) as error:
        return json.dumps({'error': str(error)})

def set_rule_old(id, logic, templ, temph, unit=1):
    """
    Sets rule for sensor with celsius default (1)
    """
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
                    INSERT INTO rules (id, scale, logic, templ, temph)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (id, logic, unit, templ, temph))
        conn.commit()
        cur.close()
        conn.close()

        return json.dumps({'id': str(id), 'scale': str(logic), 'unit': str(unit), 'templ': str(templ), 'temph': str(temph)})

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
