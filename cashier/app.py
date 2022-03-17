from config import app, jsonify, requires_auth
from producer import publish
from flask_cors import cross_origin
from flask import request
import json


@app.route("/api/generate_qr", methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def promocode_info():
    try:
        publish('generate_qr', json.dumps(
            {'promocode': request.args.get('promocode'), 'cashier': request.headers.get('Authorization')}))
    except Exception as e:
        print(e)
        return jsonify(message='Something went wrong, try again later')
    return jsonify(message='Check out your account in mystery')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
