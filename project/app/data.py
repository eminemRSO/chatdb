from bson import ObjectId
from copy import deepcopy
messages = dict()
i = 0


def find_conversation(db, name_a, name_b):
    out = []
    global messages
    for j in messages:
        if messages[j]["sender"] == name_a and messages[j]["receiver"] == name_b:
            out.append(messages[j])
        if messages[j]["sender"] == name_b and messages[j]["receiver"] == name_a:
            out.append(messages[j])

    return out


def user_messages(db, name):
    out = []
    global messages
    for j in messages:
        if messages[j]["sender"] == name or messages[j]["receiver"] == name:
            out.append(messages[j])
    return out


def create_message(db, message):
    global i
    global messages
    message["_id"] = str(ObjectId())
    messages[i] = message
    i += 1
    return message


def delete_message(db, id):
    message = None
    global messages
    k = -1
    for j in messages:
        if messages[j]["_id"] == id:
            message = deepcopy(messages[j]["_id"])
            k = j
            break
    if k > -1:
        del messages[k]
    return message


def get_messages(db, sender, receiver, text):
    out = []
    global messages
    for j in messages:
        if messages[j]["sender"] == sender and messages[j]["receiver"] == receiver and text == messages[j]["text"]:
            out.append(messages[j])

    return out


def delete_messages(db, sender, receiver, text):
    out = []
    global messages
    for j in messages:
        if messages[j]["sender"] == sender and messages[j]["receiver"] == receiver and text == messages[j]["text"]:
            out.append(j)
    for j in out:
        del messages[j]

    return out
