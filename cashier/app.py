from config import app, jsonify, requires_auth
from producer import publish
from flask_cors import cross_origin
from flask import request
import json


@app.route("/api/generate_qr", methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def promocode_info():
    response = publish('generate_qr', json.dumps(
        {'promocode': request.args.get('promocode'), 'cashier': request.headers.get('Authorization')}))
    return jsonify(message=response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
