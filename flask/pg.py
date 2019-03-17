import json
import psycopg2
from flask import request, jsonify, Response

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

def error_maker(status_code, message):
    return Response(
        json.dumps({'error': message}),
        status=status_code,
        mimetype='application/json'
    )

def __status_resp__(status, status_code, s_value, logic, templ, temph, unit=1):
    return Response(
        json.dumps({
            'status': status,
            'sensor_value': s_value,
            'logic': logic,
            'templ': templ,
            'temph': temph,
            'unit': unit
        }),
        status=status_code,
        mimetype='application/json'
    )

def __convert_to_celsius__(f):
    if f is None:
        return None
    else:
        print("f type is: ", type(f))
        return (float(f)-32)/1.8

def __compare_temps__(payload):
    """
    Compares temps to their logic levels and calls twilio
    """
    print('compare temps called')
    print('compare temps are: ',
          str(payload),
          payload['logic'],
          payload['templ'],
          payload['temph'],
          payload['s_value'],
          payload['s_unit']
          )

    # if the units aren't the same betweeen the db
    # and sensor data...
    if payload['unit'] != payload['s_unit']:
        # if the db is celsius, the sensor data must be fahrenheit
        if payload['unit'] == 0:
            # convert the sensor data to celsius
            payload['s_value'] = __convert_to_celsius__(payload['s_value'])
        else:
            # convert the db templ and temph to celsius
            payload['templ'] = __convert_to_celsius__(payload['templ'])
            payload['temph'] = __convert_to_celsius__(payload['temph'])

    # now that we have consistent units, we can compare logic...

    # temp under ll
    if payload['logic'] == 0:
        if payload['s_value'] < payload['templ']:
            print('logic0, temp under lower lim')
            return __status_resp__(
                'ng',
                200,
                payload['s_value'],
                payload['logic'],
                payload['templ'],
                payload['temph']
            )
        else:
            return __status_resp__(
                'ok',
                200,
                payload['s_value'],
                payload['logic'],
                payload['templ'],
                payload['temph']
            )

    # temp over ul
    elif payload['logic'] == 1:
        if payload['s_value'] > payload['temph']:
            print('logic1, temp over upper lim')
    # temp OOB
    elif payload['logic'] == 2:
        if payload['s_value'] < payload['templ'] or \
                payload['s_value'] > payload['temph']:
            print('logic2, temp OOB')

    return('butthead')

def input_data(payload):
    """
    Receives input sensor data stream and compares for alerts
    """

    content = payload.json

    # declare our soon-to-be-found rules for this id
    compare_temps_payload = {
        'logic': None,
        'unit': None,
        'templ': None,
        'temph': None,
        's_value': None,
        's_unit': None
    }

    # parse id field
    try:
        id = str(content['id'])
    except:
        return error_maker(400, 'invalid or missing id parameter')

    # parse value field
    try:
        value = float(content['value'])
    except KeyError:
        return error_maker(400, 'no value field found')
    except ValueError:
        return error_maker(400, 'value field not parsable')

    # parse unit field
    try:
        unit = int(content['unit'])
        if unit not in [0, 1]:
            return error_maker(400, 'invalid unit parameter')
    except KeyError:
        return error_maker(400, 'no unit field found')
    except ValueError:
        return error_maker(400, 'unit field not parsable')

    # call the db to get templ, temph, and logic for the input id
    # this is a copy of get_rule; needs refactored into
    # werkzeug.local.LocalProxy object for DRY
    try:
        # create a cursor
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
                    SELECT r.logic, r.unit, r.templ, r.temph
                    FROM rules r WHERE r.id = %s;
                    """,
                    (id))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res is None:
            return error_maker(400, 'rule for id does not exist, please create a rule at the /setrule endpoint')
        else:
            for k, v in zip(compare_temps_payload.keys(), res):
                compare_temps_payload[k] = v
            # add input sensor data to compare_temps_payload dict
            compare_temps_payload['s_value'] = value
            compare_temps_payload['s_unit'] = unit
            return __compare_temps__(compare_temps_payload)
    except (Exception, psycopg2.DatabaseError) as error:
        return error_maker(400, error.pgerror)

def set_rule(payload):
    """
    Sets rule for sensor with celsius default (0)
    """
    content = payload.json

    # parse id field
    try:
        id = str(content['id'])
    except:
        return error_maker(400, 'invalid or missing id parameter')

    # parse temp unit
    try:
        unit = int(content['unit'])
        # validate unit is celsius or farenheit, respetctively
        if unit not in [0, 1]:
            return error_maker(400, 'invalid unit parameter')
    # assume a default of celsius if unit is missing
    except KeyError:
        unit = 0

    # parse logic field
    try:
        logic = int(content['logic'])

        # if greater than logic, must have templ
        if logic == 0:
            try:
                templ = float(content['templ'])
                # set to an empty string to become a NULL upon db write
                temph = ''
            except KeyError:
                return error_maker(400, 'low temp needed for greater than logic')
            except ValueError:
                return error_maker(400, 'templ value not parsable')

        # if less than logic, must have temph
        elif logic == 1:
            try:
                temph = float(content['temph'])
                # set to an empty string to become a NULL upon db write
                templ = ''
            except KeyError:
                return error_maker(400, 'high temp needed for less than logic')
            except ValueError:
                return error_maker(400, 'temph value not parsable')

        # if OOB logic, must have both low and high temp limits
        elif logic == 2:
            try:
                templ = float(content['templ'])
                temph = float(content['temph'])
            except KeyError:
                return error_maker(400, 'high and low temp needed for OOB logic')
            except ValueError:
                return error_maker(400, 'templ or temph values not parsable')
            if templ >= temph:
                return error_maker(400, 'lower temp limit cannot be grater than or equal to upper temp limit')

        # logic param is parsable but not valid (0, 1, or 2)
        else:
            return error_maker(400, 'invalid logic parameter')
    except KeyError:
        return error_maker(400, 'missing logic parameter')
    except ValueError:
        return error_maker(400, 'logic parameter not parsable')

    # finally write the rule to the db
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
                    INSERT INTO rules (id, unit, logic, templ, temph)
                    VALUES (%s, %s, %s, NULLIF(CAST(%s AS TEXT), '')::numeric, NULLIF(CAST(%s AS TEXT), '')::numeric);
                    """,
                    (id, unit, logic, templ, temph))
        conn.commit()
        cur.close()
        conn.close()

        return Response(
            json.dumps({'id': id, 'unit': unit, 'logic': logic, 'templ': templ, 'temph': temph}),
            status=200,
            mimetype='application/json'
        )

    except (Exception, psycopg2.IntegrityError) as error:
        return Response(
            json.dumps({'error': str(error)}),
            status=409,
            mimetype='application/json'
        )

def get_rule(payload):

    content = request.json

    try:
        id = str(content['id'])
    except KeyError:
        return error_maker(400, 'missing id parameter')
    except ValueError:
        return error_maker(400, 'id parameter not parsable')

    print(id)

    # get the rule for the input id from the db
    try:
        # create a cursor
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
                    SELECT r.logic, u.unit from rules r
                    JOIN units u on u.id = r.unit WHERE r.id = %s;
                    """,
                    (id))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res is None:
            return error_maker(400, f'no rule exists for id {id}')
        else:
            return Response(
                json.dumps({ 'logic': res[0], 'unit': res[1] }),
                status=200,
                mimetype='application/json'
            )

    except (Exception, psycopg2.DatabaseError) as error:
        return error_maker(400, error.pgerror)

if __name__ == '__main__':
    connect()
