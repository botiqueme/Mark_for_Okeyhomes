import os
from chatbot import OpenAIBot
from flask import Flask, render_template, request, session, Response, redirect, send_file, jsonify
import utils
import functions
import json
import logging
from logging.handlers import RotatingFileHandler
from apscheduler.schedulers.background import BackgroundScheduler
from collections import defaultdict
import re

# Configurazione del logger
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


# Configurazione del RotatingFileHandler
handler = RotatingFileHandler('./logs/chatbot.log', maxBytes=10*1024*1024, backupCount=10)
formatter = logging.Formatter('%(asctime)s:%(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

######################## Check if the required environment variables are set
required_variables = ['OPENAI_API_KEY', 'MARK_ASSISTANT_ID', 'FLASK_KEY']
missing_values = [value for value in required_variables if os.environ.get(value) is None]
if len(missing_values) > 0:
    print(f'The following environment values are missing in your .env: {", ".join(missing_values)}')
    exit(1)

###################### Start the FLASK app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')

openai_client = OpenAIBot(os.environ.get('OPENAI_API_KEY'), os.environ.get('MARK_ASSISTANT_ID'))

# #read saved clients
# users_db_path = './resources/users.json'
# if os.path.exists(users_db_path) and os.path.getsize(users_db_path) > 0:
#     with open(users_db_path, 'r') as f:
#         openai_client.users = json.load(f)

# @app.before_first_request
# def before_first_request():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(openai_client.delete_users, 'interval', seconds=10)
#     scheduler.start()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/get', methods=['GET', 'POST'])
def get_bot_response():
    utils.clean_tmp()

    user_text = None

    if request.method == 'POST':
        if 'audio_message' in request.files:
            user_text = utils.transcribe(openai_client, request.files['audio_message'])
    else:
        user_text = request.args.get('msg')

    if 'authenticated' not in session or 'thread_id' not in session:
        thread_id = openai_client.start_conversation()

        session['authenticated'] = True
        session['thread_id'] = thread_id
    else:
        thread_id = session['thread_id']

    openai_client.create_message(session['thread_id'], user_text)
    run = openai_client.create_run(session['thread_id'])
    run, failed = openai_client.wait_for_run(session['thread_id'], run)

    if failed:
        return json.dumps("Sono spiacente, al momento sto riposando &#128164;! Riprova più tardi.")

    # assert run.status == 'completed'

    answer = openai_client.collect_response(session['thread_id'])

    function, answer = utils.check_trigger_functions(answer)

    answer = utils.text_to_html(answer)
    answer = utils.remove_keywords(answer)
    # print(answer, function)

    utils.log_conversation(logger, thread_id, user_text, answer)

    if function == 'take_appointment':
        # showform = {"showForm": True}
        return json.dumps(True)


    if request.method == 'POST':
        speech_url = openai_client.text_to_speech(answer)
        return send_file(speech_url, mimetype='audio/mpeg')
    #         return jsonify({
    #     "audio": speech_url,
    #     "link": "www.google.com"
    # })
    else:
        return json.dumps(answer)

@app.route('/admin/conversations')
def show_conversations():
    data = utils.parse_log_file()
    return render_template('admin_log.html', stats=data, conversations=data["conversations"], thread_dates=data['thread_dates'])



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
