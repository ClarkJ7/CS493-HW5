from google.cloud import datastore
from flask import Flask, request, Blueprint
import json
import constants
import boats

app = Flask(__name__)
app.register_blueprint(boats.bp)

client = datastore.Client()

# variable changed for testing/deploying
current_url = constants.current_url


@app.route('/')
def index():
    return 'Please navigate to /boats to use this API'


# Route to clear datastore, used for testing
@app.route('/reset', methods=['DELETE'])
def reset():
    if request.method == 'DELETE':
        # Clear boats from datastore every reset
        del_query = client.query(kind=constants.boats)
        del_results = list(del_query.fetch())
        for entity in del_results:
            client.delete(entity.key)

        return '', 204

    else:
        return 'Invalid request type', 405


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
