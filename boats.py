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
        if 'name' not in content:
            return constants.boatAttr, 400
        elif 'type' not in content:
            return constants.boatAttr, 400
        elif 'length' not in content:
            return constants.boatAttr, 400

        # check if name is valid
        elif not validation.validateChar(content['name']):
            return constants.invChar, 400
        elif not validation.validateLen(content['name']):
            return constants.invLen, 400

        # check if name is unique
        elif not validation.validateUniq(content['name']):
            return constants.boatName, 403

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
            return new_boat, 201

    elif request.method in {'PUT', 'DELETE'}:
        res = make_response(constants.badMethod)
        # methods listed in route are automatically included in Allow header
        res.status_code = 405
        return res

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
        if 'name' not in content:
            return constants.boatAttr, 400
        elif 'type' not in content:
            return constants.boatAttr, 400
        elif 'length' not in content:
            return constants.boatAttr, 400

        # check if name is valid
        elif not validation.validateChar(content['name']):
            return constants.invChar, 400
        elif not validation.validateLen(content['name']):
            return constants.invLen, 400

        # check if name is unique
        elif not validation.validateUniq(content['name']):
            return constants.boatName, 403

        target_boat.update({"name": content["name"], "type": content["type"], "length": content["length"]})
        client.put(target_boat)
        target_boat['id'] = target_boat.key.id
        target_boat["self"] = constants.current_url + "boats/" + str(target_boat.key.id)
        return make_response(target_boat, 303)

    # invalid method used
    else:
        return 'Invalid request method, please try again'
