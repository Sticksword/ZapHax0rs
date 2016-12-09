#!/usr/bin/env python

import json
import os
import csv
import atexit

from flask import Flask, request, make_response, send_from_directory, render_template, jsonify
# for reference: http://flask.pocoo.org/docs/0.11/quickstart/
import flask_excel as excel

# Flask app should start in global layout
app = Flask(__name__, static_url_path='')
in_memory_db = {}
message_db = {}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return jsonify({"result": request.get_array(field_name='file')})
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''

@app.route("/download", methods=['GET'])
def download_file():
    return excel.make_response_from_array([[1,2], [3, 4]], "csv")

@app.route("/export", methods=['GET'])
def export_records():
    return excel.make_response_from_array([[1,2], [3, 4]], "csv", file_name="export_data")


@app.route('/message', methods=['POST'])
def message():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = addMessageToDb(req)

    r = make_response(json.dumps(res, indent=4))
    r.headers['Content-Type'] = 'application/json'
    return r

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


def processRequest(req):
    print req
    if req.get("result").get("action") == "QuoteGreeting":
        return {
            "speech": 'this is a quote response!',
            "displayText": 'test quote response',
            "source": "quote-greeting-webhook"
        }
    if req.get("result").get("action") == "FindRoom":
        return parse_api_ai(req)
    return {}


def init():
    print 'initializing'



@atexit.register
def goodbye():
    print "You are now leaving the Python sector."


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print "Starting app on port %d" % port
    init()
    app.run(debug=True, port=port, host='0.0.0.0')
