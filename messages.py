
from datetime import datetime

_messages = []

def add(message, stack=True):

    if stack and _messages and _messages[-1]['text'] == message:
        # increment count of last message
        _messages[-1]['count'] += 1
    else:
        # add message to list
        _messages.append({
            'text': message,
            'count': 1,
        })

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("messages.log", "a") as log:
        log.write(f"{ts} {message}\n")

def get( n=5, offset=0 ):
    return _messages[offset:offset+n]

def last(n=5):
    return _messages[-n:]

def count():
    return len(_messages)
