import requests
import time, threading
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

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

def getSlackHistory():
    ts = time.time() - 5 * 60
    headers = {
        # 'content-type': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = {
        'token': 'xoxp-13390904948-187170561730-377563214645-6a8769947601d95062e7ded2fce50aab',
        'channel': 'C6WKF1PBQ',
        'oldest': ts
    }

    url = "https://slack.com/api/channels.history"
    resp = requests.post(url, data=params, headers=headers)
    response_data = json.loads( resp.content )
    output_dict = [x for x in response_data[ 'messages' ] if 'attachments' in x.keys() ]
    for data in output_dict:
        t = {}
        answer = data[ 'text' ]
        attachment = data[ 'attachments'][0]
        question = attachment[ 'text' ]
        question = question.split('question')
        question = question[1]
        bot.train([question, answer,]) 
        print(question,answer)

    print(ts)

def monitor_slack():
    print(time.ctime())
    getSlackHistory()
    threading.Timer( 5 * 60, monitor_slack).start()

monitor_slack()