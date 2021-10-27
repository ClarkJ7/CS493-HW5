from google.cloud import datastore
import constants

client = datastore.Client()


def validateChar(input_name):
    no_spaces = input_name.replace(' ', '')
    if no_spaces.isalnum():
        return True
    else:
        return False


def validateLen(input_name):
    if len(input_name) > 20:
        return False
    else:
        return True


def validateUniq(input_name):
    # get existing boat names
    query = client.query(kind=constants.boats)
    results = list(query.fetch())
    boat_names = set()
    for boat in results:
        boat_names.add(boat['name'])

    if input_name in boat_names:
        return False
    else:
        return True
