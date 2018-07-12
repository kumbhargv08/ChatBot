
from chatterbot import ChatBot

class PPChatBot(ChatBot):
    """
    A conversational dialog chat bot.
    """

    def __init__(self, name, **kwargs):
        super(PPChatBot, self).__init__(name,**kwargs)

    def get_response(self, input_item, conversation_id=None):
        """
        Return the bot's response based on the input.

        :param input_item: An input value.
        :param conversation_id: The id of a conversation.
        :returns: A response to the input.
        :rtype: Statement
        """
        if not conversation_id:
            if not self.default_conversation_id:
                self.default_conversation_id = self.storage.create_conversation()
            conversation_id = self.default_conversation_id

        input_statement = self.input.process_input_statement(input_item)

        # Preprocess the input statement
        for preprocessor in self.preprocessors:
            input_statement = preprocessor(self, input_statement)

        statement, response = self.generate_response(input_statement, conversation_id)

        # Learn that the user's input was a valid response to the chat bot's previous output
        previous_statement = self.storage.get_latest_response(conversation_id)

        print('Input: ',input_statement,' \nResponse; ',response,' \nprevious_statement: ',previous_statement)

        if (not self.read_only) and (not(response.text == 'I am sorry, but I do not understand.')):
            self.learn_response(statement, previous_statement)
            self.storage.add_to_conversation(conversation_id, statement, response)

        # Process the response output with the output adapter
        return self.output.process_response(response, conversation_id)   
