from flask import Flask, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from slackclient import SlackClient
from flask_cors import CORS
import time

bot = ChatBot('Bot',read_only=True,
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
slack_token = 'SLACK_TOKEN' 
sc = SlackClient(slack_token)

app = Flask(__name__)
CORS(app)
@app.route("/chat/query/<question>", methods=['GET'])
def get_answer( question ):
    print( question )
    reply = bot.get_response(question)
    if question == reply or reply=='I am sorry, but I do not understand.':
        sc.api_call(
            "chat.postMessage",
            channel="#pp",
            text="Hi Vidya/Monali!!! Please answer following question " + question
            )
        if sc.rtm_connect():
            while True:
                result = sc.rtm_read()
                if(len(result)):
                    set1 = result[0]
                    # print(type(set1))
                    if("attachments" in set1.keys()):
                        attachments = set1["attachments"][0]
                        if(attachments["is_share"]):
                            ques = attachments["text"].replace("Hi Vidya/Monali!!! Please answer following question ", "")
                            print(ques)
                            response = set1["text"]         #response=<bytecode> message
                            response = response.split("> ")[1] if response.__contains__('>') else response
                            bot.train([ques, response,])
                    if(len(set1) and set1["type"]=="message" and set1["channel"]=="C6WKF1PBQ"):
                        #print("type is : " , type(set1))
                        response = set1["text"]         #response=<bytecode> message
                        response = response.split("> ")[1] if response.__contains__('>') else response
                        #print("response is:",response)
                        
                        reply = response
                        break
                #print("result is: " , result)
                time.sleep(1)
        else:
            print("unable to connect to slack chatbot")             
    else:
        print('Chatbot:',reply)
    return jsonify({'answer': str( reply )}), 201


if __name__ == "__main__":
    app.run( debug=True )
