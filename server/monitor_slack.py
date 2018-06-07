import requests
import time, threading
import json


def getSlackHistory( bot ):
    ts = time.time() - 5 * 60
    headers = {
        # 'content-type': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = {
        'token': 'slack_token',
        'channel': 'channel_id',
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

def monitor_slack( bot ):
    print(time.ctime())
    getSlackHistory( bot )
    threading.Timer( 20, monitor_slack, [bot]).start()
