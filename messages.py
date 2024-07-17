
from datetime import datetime

_messages = []

def add(message):

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # add message to list
    _messages.append(message)

    with open("messages.txt", "a") as log:
        log.write(f"{ts} {message}\n")

def get( n=5 ):
    return _messages[-n:]
