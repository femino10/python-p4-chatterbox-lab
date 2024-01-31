from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
import json

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

def serialize_message(message):
    return {
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at.isoformat(),
        'updated_at': message.updated_at.isoformat() if message.updated_at else None
    }

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    serialized_messages = [serialize_message(message) for message in messages]
    return jsonify(serialized_messages)

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message)

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    data = request.get_json()
    message.body = data['body']
    db.session.commit()
    return jsonify(message)

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    Session = sessionmaker(bind=db.engine)
    session = Session()

    message = session.get(Message, id)
    if message:
        session.delete(message)
        session.commit()
        return jsonify({'message': 'Message deleted successfully'})
    else:
        return jsonify({'message': 'Message not found'}), 404

if __name__ == '__main__':
    app.run(port=5555)
