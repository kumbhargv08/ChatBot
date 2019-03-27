import os
import logging
import yaml

from pp_chatbot import PPChatBot
from chatterbot.trainers import ListTrainer

logging.basicConfig(level=logging.INFO)

bot = PPChatBot(
    'Norman',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    logic_adapters=[
        {
            'import_path': 'my_logic_adapter.MyLogicAdapter',
            "statement_comparison_function": "chatterbot.comparisons.JaccardSimilarity",
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
bot.set_trainer(ListTrainer)

for files in os.listdir('C:/Users/raman.mishra/Desktop/ChatBot/server/data'):
    print(files)
    stream = open('C:/Users/raman.mishra/Desktop/ChatBot/server/data/'+ files,'r')
    #converting yaml to python object
    pyObject = yaml.load(stream)
    print(type(pyObject))
    arrayOfConverstions = pyObject['conversations']
    for conversation in arrayOfConverstions:
        bot.train(conversation)

print("Type something to begin...")

# The following loop will execute each time the user enters input
while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        bot_input = bot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break

