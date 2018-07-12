import requests
import time, threading
import json

def set_interval( func, sec, bot, question_dict ):
    def func_wrapper():
        set_interval( func, sec, bot, question_dict )
        func( bot, question_dict )
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

SlackChannelPollingStarted = False
def getSlackHistory( bot, question_dict):
    print('BUIBUI',time.ctime())
    ts = time.time() - 40
    headers = {
        # 'content-type': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = {
        'token': 'xoxp-13390904948-207581812692-395136787829-9ae111ce4d042136321c0826e2a5a170',
        'channel': 'CBL8T6Y9E',
        'oldest': ts
    }

    url = "https://slack.com/api/channels.history"
    resp = requests.post(url, data=params, headers=headers)
    response_data = json.loads( resp.content )
    print('response data from slack channel history', response_data)
    output_dict = [x for x in response_data[ 'messages' ] if 'attachments' in x.keys() ]
    for data in output_dict:
        t = {}
        answer = data[ 'text' ]
        attachment = data[ 'attachments'][0]
        question = attachment[ 'text' ]
        question = question.split('question')
        question = question[1]
        question = question.encode('utf-8','ignore').strip()
        answer = answer.encode('utf-8','ignore').strip()
        bot.train([question, answer,]) 
        question_dict[question]=answer
        print(question,answer)

    print(ts, question_dict)

def monitor_slack( bot, question_dict ): 
    set_interval( getSlackHistory, 40, bot, question_dict )
