import flask

from flask import request, jsonify

app = flask.Flask( __name__ )
app.config["DEBUG"] = True

#Return crypto historicals
@app.route('/historicals/crypto', methods=['GET'])
def equity_historicals():
	if "ticker" and "start" and "end" and "asset_type" in request.args:
		ticker = str().upper()
	else:
		return "missing arguments"

	
