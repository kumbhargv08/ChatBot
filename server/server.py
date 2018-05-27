from flask import Flask, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

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

app = Flask(__name__)

@app.route("/chat/query/<question>", methods=['GET'])
def get_answer( question ):
    print( question )
    reply = bot.get_response(question)
    return jsonify({'answer': str( reply )}), 201


if __name__ == "__main__":
    app.run( debug=True )