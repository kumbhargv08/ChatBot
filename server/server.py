from flask import Flask, jsonify, request
from slackclient import SlackClient
from flask_cors import CORS
from monitor_slack import monitor_slack

from pp_chatbot import PPChatBot
from chatterbot.trainers import ListTrainer

import copy
import logging
import time, threading

#setting log level to debug
logging.basicConfig(level=logging.DEBUG)

#initilize logging object for INFO, DEBUG, ERROR logs
tLogger = logging.getLogger(__name__)

#keep track of all the question answered on slack channel (KEY: question, VALUE: answer)
question_dict = {}

#key is 'user_session_id' and value is dict containing { array of unanswered questions, time of recent activity }
sessionId_unans_question_map ={}

#chatbot object
bot = PPChatBot(
    'Shaktiman',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'my_logic_adapter.MyLogicAdapter',
            "statement_comparison_function": "chatterbot.comparisons.LevenshteinDistance",
            "response_selection_method": "chatterbot.response_selection.get_random_response",
            'threshold': 0.65,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],
    filters=["chatterbot.filters.RepetitiveResponseFilter"],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    database='./database.sqlite3',
    trainer='chatterbot.trainers.ListTrainer'
)

#slack token to connect to Slack Client
slack_token = 'slack_token' 
sc = SlackClient( slack_token )

app = Flask(__name__)
# for Cross Origin Resource Sharing
CORS(app)

HALF_HOUR = 30 * 60 #in seconds
def set_interval( func, sec ):
    def func_wrapper():
        set_interval( func, sec )
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def postQuestionOnSlack( question ):
    reply = ''
    sc.api_call(
        "chat.postMessage",
        channel="#pp_trainer",
        text="Hi Vidya/Monali!!! Please answer following question " + question
        )

def updateUnansweredQuestionsForUser( sessionId ):
    questionArray = sessionId_unans_question_map[ sessionId ]['questions']
    updatedQuestionArray = copy.deepcopy( questionArray )
    reply=''

    for ques in questionArray:
        if ques in question_dict:
            updatedQuestionArray.remove( ques )
            reply= reply + "Someone has answered your previous question: "+ ques +":\n"+ question_dict[ ques ] + ".\n and for this question: "
            question_dict.pop( ques, None )

    sessionId_unans_question_map[ sessionId ]['questions'] = updatedQuestionArray
    return reply

def clearExpiredSession():
    tLogger.debug("Time to clear session is {}".format(time.time()))
    cloneObject = copy.deepcopy( sessionId_unans_question_map )
    for sessionId in cloneObject:
        if(sessionId_unans_question_map[sessionId]['recently_active'] - time.time() > HALF_HOUR ):
            sessionId_unans_question_map.pop( sessionId, None )

def checkExpiredSession():
    #if no user activity for more than 30 minutes than clear session
    set_interval( clearExpiredSession, HALF_HOUR )


#----------------Routes START----------------------
#1
@app.route("/userQuery", methods=['POST'])
def processUserQuery():
    sessionId = request.json['sessionId']

    #checking if request have session id
    if( not sessionId ):
        tLogger.error('Didn\'t recevived session ID in request: {}',format(request)) 
        response = app.response_class(
            response = 'Bad Request: Session details not found',
            status = 400,
            mimetype = 'text/plain'
        )
        return response

    question = request.json['query']

    tLogger.info( 'Received Query "{}" from user with session id {}'.format(
                        question, sessionId ))

    #if new user session then create a new key for sessionId_question map
    if not ( sessionId in sessionId_unans_question_map ):
        sessionId_unans_question_map[ sessionId ] = {}
        sessionId_unans_question_map[ sessionId ]['questions'] = []

    #store the time of last question asked by user
    sessionId_unans_question_map[ sessionId ]['recently_active'] = time.time()

    tLogger.debug( 'Unanswered question for user {} are: {}'.format(
                        sessionId, sessionId_unans_question_map))

    reply = updateUnansweredQuestionsForUser( sessionId )

    bot_reply = bot.get_response(question)
    tLogger.debug('Reply from chatBot is {}'.format(bot_reply))

    if question == bot_reply or bot_reply == 'I am sorry, but I do not understand.':
        reply = reply + 'sorry, I did not understand that. We have posted your query to pp slack channel'
        sessionId_unans_question_map[ sessionId ]['questions'].append( question ) 
        postQuestionOnSlack( question )          
    else:
        reply = reply + str( bot_reply )

    return jsonify({'answer': str( reply )}), 201

#2 TODO: trigger this route when window/tab closes on UI
@app.route("/clearSession",methods=['POST'])
def clearSessionDetailsForUser():
    sessionId = request.json['sessionId']
    #checking if request have session id
    if( not sessionId ):
        tLogger.error('Didn\'t recevived session ID in request: {}',format( request )) 
        response = app.response_class(
            response='Bad Request: Session details not found',
            status=400,
            mimetype='text/plain'
        )
        return response
    sessionId_unans_question_map.pop( sessionId, None)
    tLogger.info('Session Successfully cleared for user: {}',format( sessionId )) 
    response = app.response_class(
        response='Session Successfully Cleared!',
        status=200,
        mimetype='text/plain'
    )
    return response
#----------------Routes END----------------------    


if __name__ == "__main__":
    tLogger.debug("Time when Scheduling starts: {}".format(time.time()))
    monitor_slack( bot, question_dict )
    checkExpiredSession()
    app.run( debug=True, use_reloader=False )
    
