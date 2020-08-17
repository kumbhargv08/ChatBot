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
        'token': 'token',
        'channel': 'channelId',
        'oldest': str(ts)
    }

    url = "https://slack.com/api/conversations.history?token=" + params['token'] + "&channel=" + params['channel'] + "&oldest=" + params['oldest']
    resp = requests.get(url, headers)
    
    response_data = json.loads( resp.content )
    print(response_data)
    output_dict = [x for x in response_data[ 'messages' ] if 'attachments' in x.keys() ]
    for data in output_dict:
        t = {}
        answer = data[ 'text' ]
        attachment = data[ 'attachments'][0]
        question = attachment[ 'text' ]
        question = question.split('question')
        question = question[1]
        question = question.strip()
        answer = answer.strip()
        bot.train([question, answer,]) 
        question_dict[question]=answer
        print(question,answer)

    print(ts, question_dict)

def monitor_slack( bot, question_dict ):
    print(time.ctime())
    getSlackHistory( bot, question_dict )
    threading.Timer( 40, monitor_slack, [bot, question_dict]).start()