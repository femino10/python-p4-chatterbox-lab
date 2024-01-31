from datetime import datetime

from app import app
from models import db, Message

class TestApp:
    '''Flask application in app.py'''

    with app.app_context():
        m = Message.query.filter(
            Message.body == "Hello 👋"
        ).filter(Message.username == "Liza")

        for message in m:
            db.session.delete(message)

        db.session.commit()

    def test_has_correct_columns(self):
        with app.app_context():

            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")

            db.session.add(hello_from_liza)
            db.session.commit()

            assert(hello_from_liza.body == "Hello 👋")
            assert(hello_from_liza.username == "Liza")
            assert(type(hello_from_liza.created_at) == datetime)

            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        '''returns a list of JSON objects for all messages in the database.'''
        with app.app_context():
            response = app.test_client().get('/messages')
            assert response.status_code == 200  # Ensure the response is successful
            if response.status_code == 200:
                records = response.json  # Access json only if the response is successful
                assert isinstance(records, list)
                assert len(records) > 0

    # ... (other test methods)

    def test_deletes_message_from_database(self):
        '''deletes the message from the database.'''
        with app.app_context():

            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")

            db.session.add(hello_from_liza)
            db.session.commit()

            app.test_client().delete(
                f'/messages/{hello_from_liza.id}'
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(not h)
