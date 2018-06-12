from flask import Flask, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from slackclient import SlackClient
from flask_cors import CORS
from monitor_slack import monitor_slack

import time

question_dict = {}
unanswered_que =[None]
bot = ChatBot('Bot',
              logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],
    trainer='chatterbot.trainers.ListTrainer')
slack_token = 'xoxp-13390904948-172567049778-378161812517-702e3349359e45908520d76fce3e8ad2' 
sc = SlackClient(slack_token)

app = Flask(__name__)
CORS(app)

def postQuestionOnSlack( question ):
    reply = ''
    sc.api_call(
        "chat.postMessage",
        channel="#pp",
        text="Hi Vidya/Monali!!! Please answer following question " + question
        )

@app.route("/chat/query/<question>", methods=['GET'])
def get_answer( question ):
    reply=''
    print( question )
    print(unanswered_que, question_dict)
    for query in unanswered_que:
        print( 'query', query )
        if query in question_dict.keys():
            print( 'query', query )
            reply= reply + "Someone has answered your previous qeustion: "+ query +":\n"+ question_dict[ query ] + ".\n and for this question: "
            question_dict.pop( query, None)
    bot_reply = bot.get_response(question)
    if question == bot_reply or bot_reply=='I am sorry, but I do not understand.':
        reply =reply + 'sorry, I did not understand that. We have posted your query to pp slack channel'
        unanswered_que.append(question) 
        postQuestionOnSlack(question)          
    else:
        reply =reply + str(bot_reply)
        print('Chatbot:',reply)   
    return jsonify({'answer': str( reply )}), 201


if __name__ == "__main__":
    monitor_slack( bot, question_dict )
    app.run( debug=True, threaded=True )
    