import requests
import time, threading
import json


def getSlackHistory( bot, question_dict):
    ts = time.time() - 40
    headers = {
        # 'content-type': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = {
        'token': 'xoxp-13390904948-172567049778-378161812517-702e3349359e45908520d76fce3e8ad2',
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
        question = question.encode('ascii','ignore').strip()
        answer = answer.encode('ascii','ignore').strip()
        bot.train([question, answer,]) 
        question_dict[question]=answer
        print(question,answer)

    print(ts, question_dict)

def monitor_slack( bot, question_dict ):
    print(time.ctime())
    getSlackHistory( bot, question_dict )
    threading.Timer( 40, monitor_slack, [bot, question_dict]).start()