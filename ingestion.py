import flask

from flask import request, jsonify

app = flask.Flask( __name__ )
app.config["DEBUG"] = True

#Return 
@app.route('/historicals/crypto', methods=['GET'])
def crypto_historicals():
	if 'ticker' in request.args:
		ticker = int(request.args['ticker'])
	else:
		return ""
