# *-* coding: utf-8 *-* 

from flask import Flask 

app = Flask(__name__)

@app.route('/test')
def test():
	print "in test"
	return "this is test"