from chatterbot.storage import SQLStorageAdapter

class newSQLStorageAdapter(SQLStorageAdapter):

    def __init__(self, **kwargs):
        super(newSQLStorageAdapter, self).__init__(**kwargs)

    def add_one_to_conversation(self, conversation_id, statement):
        """
        Add the statement and response to the conversation.
        """
        Statement = self.get_model('statement')
        Conversation = self.get_model('conversation')

        session = self.Session()
        conversation = session.query(Conversation).get(conversation_id)

        statement_query = session.query(Statement).filter_by(
            text=statement.text
        ).first()

        # Make sure the statements exist
        if not statement_query:
            self.update(statement)
            statement_query = session.query(Statement).filter_by(
                text=statement.text
            ).first()

        conversation.statements.append(statement_query)

        session.add(conversation)
        self._session_finish(session)