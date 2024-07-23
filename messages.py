
from datetime import datetime

_messages = []

def add(message):

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # add message to list
    _messages.append(message)

    with open("messages.log", "a") as log:
        log.write(f"{ts} {message}\n")

def get( n=5, offset=0 ):
    return _messages[offset:offset+n]

def last(n=5):
    return _messages[-n:]

def count():
    return len(_messages)
