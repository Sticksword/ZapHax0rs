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

@app.route('/analyse_entities', methods=['GET'])
def analyse_entities():
    comment=request.args.get('comment')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('language', 'v1', credentials=credentials)

    service_request = service.documents().analyzeEntities(
        body={
            'document': {
                'type': 'PLAIN_TEXT',
                'content': comment,
            }
        }
    )
    response = service_request.execute()

    r = make_response(json.dumps(response, indent=4))
    r.headers['Content-Type'] = 'application/json'
    return r

@app.route('/analyse_sentences', methods=['GET'])
def analyse_sentences():
    comment=request.args.get('comment')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('language', 'v1', credentials=credentials)

    service_request = service.documents().analyzeSentiment(
        body={
            'document': {
                'type': 'PLAIN_TEXT',
                'content': comment,
            }
        }
    )
    response = service_request.execute()

    r = make_response(json.dumps(response, indent=4))
    r.headers['Content-Type'] = 'application/json'
    return r

@app.route('/demo', methods=['POST'])
def upload_demo():
    print request
    print request.form
    return 'success'

@app.route('/upload', methods=['POST'])
def upload_file():
    print 'hello from upload_file'
    print request
    print request.form
    # print request.get_sheet()
    print request.get_array(field_name='file')
    return 'success'

@app.route('/export', methods=['GET'])
def export_records():
    return excel.make_response_from_array([[1,2], [3, 4]], 'csv', file_name='export_data')


@app.route('/example_post', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print('Request:')
    print(json.dumps(req, indent=4))

    res = { 'sample': 'text' }

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


def init():
    print 'initializing'



@atexit.register
def goodbye():
    print 'You are now leaving the Python sector.'


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print 'Starting app on port %d' % port
    init()
    app.run(debug=True, port=port, host='0.0.0.0')
