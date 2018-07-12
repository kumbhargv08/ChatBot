from chatterbot.logic import LogicAdapter
from chatterbot.comparisons import SynsetDistance
from chatterbot.conversation import Statement

class MyLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(MyLogicAdapter, self).__init__(**kwargs)

        self.confidence_threshold = kwargs.get('threshold', 0.65)

        default_responses = kwargs.get(
            'default_response', "I'm sorry, I do not understand."
        )

        # Convert a single string into a list
        if isinstance(default_responses, str):
            default_responses = [
                default_responses
            ]

        self.default_responses = [
            Statement(text=default) for default in default_responses
        ]

    def get(self, input_statement):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        statement_list = self.chatbot.storage.get_response_statements()

        if not statement_list:
            if self.chatbot.storage.count():
                # Use a randomly picked statement
                self.logger.info(
                    'No statements have known responses. ' +
                    'Choosing a random response to return.'
                )
                random_response = self.chatbot.storage.get_random()
                random_response.confidence = 0
                return random_response
            else:
                raise self.EmptyDatasetException()

        closest_match = input_statement
        closest_match.confidence = 0

        # Find the closest matching known statement
        for statement in statement_list:
            confidence = self.comparison_object.compare( input_statement, statement)

            if confidence > closest_match.confidence:
                statement.confidence = confidence
                closest_match = statement

        return closest_match

    def can_process(self, statement):
        """
        Check that the chatbot's storage adapter is available to the logic
        adapter and there is at least one statement in the database.
        """
        return self.chatbot.storage.count()


    def get_initialization_functions(self):
        """
        Return a dictionary of functions to be run once when the chat bot is instantiated.
        """
        self.comparison_object = self.compare_statements()
        return self.compare_statements.get_initialization_functions(self.comparison_object)

    def initialize(self):
        for function in self.get_initialization_functions().values():
            function()

    def process(self, input_statement):

        # Select the closest match to the input statement
        closest_match = self.get(input_statement)
        self.logger.info('Using "{}" as a close match to "{}"'.format(
            input_statement.text, closest_match.text
        ))

        # Get all statements that are in response to the closest match
        response_list = self.chatbot.storage.filter(
            in_response_to__contains=closest_match.text
        )


        # If confidence of closest match statement is higher than thershold
        # then let it choose response from response list
        print('Closest Match Confidence: ', closest_match.confidence, closest_match.text)
        if closest_match.confidence >= self.confidence_threshold and response_list:
            self.logger.info(
                'Selecting response from {} optimal responses.'.format(
                    len(response_list)
                )
            )
            response = self.select_response(input_statement, response_list)
            response.confidence = closest_match.confidence
            self.logger.info('Response selected from Respose list. Using "{}"'.format(response.text))

        else:
            # Choose a response from the list of default options
            response = self.select_response(input_statement, self.default_responses)
            response.confidence = self.confidence_threshold
            self.logger.info('Response selected from default Response list. Using "{}"'.format(response.text))


        return response