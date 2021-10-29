from google.cloud import datastore
import constants
from flask import make_response

client = datastore.Client()

# CHECKS FOR BOAT NAMES


def validateNameChar(input_name):
    no_spaces = input_name.replace(' ', '')
    if no_spaces.isalnum():
        return True
    else:
        return False


def validateNameLen(input_name):
    if len(input_name) > 20:
        return False
    else:
        return True


def validateNameUniq(input_name):
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


def validateName(input_name):
    if not validateNameChar(input_name):
        return make_response(constants.invNameChar, 400)
    elif not validateNameLen(input_name):
        return make_response(constants.invNameLen, 400)
    elif not validateNameUniq(input_name):
        return make_response(constants.boatName, 403)
    else:
        return True


def checkAttributes(content):
    if 'name' not in content:
        return make_response(constants.boatAttr, 400)
    elif 'type' not in content:
        return make_response(constants.boatAttr, 400)
    elif 'length' not in content:
        return make_response(constants.boatAttr, 400)
    else:
        return True

# CHECKS FOR BOAT TYPES


def validateTypeChar(input_type):
    no_spaces = input_type.replace(' ', '')
    if no_spaces.isalpha():
        return True
    else:
        return False


def validateTypeLen(input_type):
    if len(input_type) > 20:
        return False
    else:
        return True


def validateType(input_type):
    if not validateTypeChar(input_type):
        return make_response(constants.invTypeChar, 400)
    elif not validateTypeLen(input_type):
        return make_response(constants.invTypeLen, 400)
    else:
        return True


# CHECKS FOR BOAT LENGTHS


def validateLengthChar(input_length):
    if str(input_length).isnumeric():
        return True
    else:
        return False


def validateLengthLen(input_length):
    if len(str(input_length)) > 4:
        return False
    else:
        return True


def validateLength(input_length):
    if not validateLengthChar(input_length):
        return make_response(constants.invLengthChar, 400)
    elif not validateLengthLen(input_length):
        return make_response(constants.invLengthLen, 400)
    else:
        return True


# VALIDATE ALL

def validateAll(content):
    content_attributes = len(content)
    validate_name = validateName(content['name'])
    validate_type = validateType(content['type'])
    validate_length = validateLength(content['length'])
    if content_attributes > 3:
        return make_response(constants.tooManyAtt, 400)
    elif validate_name is not True:
        return validate_name
    elif validate_type is not True:
        return validate_type
    elif validate_length is not True:
        return validate_length
    else:
        return True
