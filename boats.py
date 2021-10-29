from google.cloud import datastore
from flask import Flask, request, Blueprint, make_response
import json
import constants
import validation


bp = Blueprint('boats', __name__, url_prefix='/boats')
client = datastore.Client()


@bp.route('', methods=['POST'])
def boats():
    if 'application/json' not in request.accept_mimetypes:
        return "JSON cannot be returned", 406

    # adds boat to client
    if request.method == 'POST':
        # check request content-type
        if request.content_type != 'application/json':
            return "JSON not received", 415

        # get body from request
        content = request.get_json()

        # check for all attributes
        validate_content = validation.checkAttributes(content)
        if validate_content is not True:
            return validate_content

        # check if name, type, and length is valid
        validate = validation.validateAll(content)
        if validate is not True:
            return validate

        # add boat to client
        else:
            new_boat = datastore.Entity(client.key(constants.boats))
            new_boat.update(
                {"name": content["name"],
                 "type": content["type"],
                 "length": content["length"],
                 })
            client.put(new_boat)
            # add id and self attributes for response
            new_boat["id"] = new_boat.key.id
            new_boat["self"] = constants.current_url + "boats/" + str(new_boat.key.id)

            res = make_response(new_boat, 201)
            res.headers['Location'] = new_boat["self"]
            return res

    elif request.method in {'PUT', 'DELETE'}:
        return make_response(constants.badMethod, 405)

    # invalid method used
    else:
        return 'Invalid request method, please try again'


@bp.route('/<boat_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def boat(boat_id):
    boat_key = client.key(constants.boats, int(boat_id))
    target_boat = client.get(key=boat_key)

    # check for boat_id
    if target_boat is None:
        return constants.boatID, 404

    # delete boat from client
    if request.method == 'DELETE':
        client.delete(boat_key)
        return '', 204

    elif request.method == 'GET':
        if 'application/json' in request.accept_mimetypes:
            return make_response(target_boat, 200)
        elif 'text/html' in request.accept_mimetypes:
            output = """<ul>
                        <li>Name: {name}</li>
                        <li>Type: {type}</li>
                        <li>Length: {length}</li>
                        </ul>""".format(**target_boat)
            return make_response(output, 200)

    elif 'PUT' in request.method:
        # get body from request
        content = request.get_json()

        # check for all attributes
        validate_content = validation.checkAttributes(content)
        if validate_content is not True:
            return validate_content

        # check if name, type, and length is valid
        validate = validation.validateAll(content)
        if validate is not True:
            return validate

        target_boat.update({"name": content["name"],
                            "type": content["type"],
                            "length": content["length"]})
        client.put(target_boat)
        target_boat['id'] = target_boat.key.id
        target_boat["self"] = constants.current_url + "boats/" + str(target_boat.key.id)

        res = make_response(target_boat, 303)
        res.headers['Location'] = target_boat["self"]
        return res

    elif 'PATCH' in request.method:
        # get body from request
        content = request.get_json()

        # check for applicable/valid attributes
        if 'name' not in content:
            content['name'] = target_boat['name']
        else:
            # check if new name is valid
            validate_name = validation.validateName(content['name'])
            if validate_name is not True:
                return validate_name

        if 'type' not in content:
            content['type'] = target_boat['type']
        else:
            # check if new type is valid
            validate_type = validation.validateType(content['type'])
            if validate_type is not True:
                return validate_type

        if 'length' not in content:
            content['length'] = target_boat['length']
        else:
            # check if new length is valid
            validate_length = validation.validateLength(content['length'])
            if validate_length is not True:
                return validate_length

        target_boat.update({"name": content["name"], "type": content["type"], "length": content["length"]})
        client.put(target_boat)
        target_boat['id'] = target_boat.key.id
        target_boat["self"] = constants.current_url + "boats/" + str(target_boat.key.id)
        return make_response(target_boat, 200)

    # invalid method used
    else:
        return 'Invalid request method, please try again'
