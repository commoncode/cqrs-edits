import os
import sys
import pymongo
import time

MONGO_URL = os.environ.get('MONGO_URL', False)

if MONGO_URL:
    client = pymongo.MongoClient(host=MONGO_URL)
else:
    client = pymongo.MongoClient('localhost', 27017)

db = client.get_default_database()


def log(msg):
    """A shortcut to write to the standard error file descriptor"""
    sys.stderr.write('{}\n'.format(msg))


def process_edit_doc(edit_doc):

    # fetch the actual Document from Mongo to work with it.
    # edit_doc = db.edit_documents.find_one({'_id': msg['id']})\

    # fetch the diffs which will be useful to determine which
    # changes to apply
    edit_diff = db.edit_diffs.find_one({'editDocId': edit_doc['_id']})

    # these are the key's that we'll update
    update_keys = edit_doc['origObj'].keys()
    if 'id' in update_keys:
        update_keys.remove('id') # except for id

    # Build up the obj of attributes that have changed for update
    # checking for the existence of diffs'
    obj = {}
    for key in update_keys:
        if key != 'id':
            # @@@ perform any hydration / parsing
            # @@@ test for any diffs
            if key in edit_diff['diffs'].keys():
                obj[key] = edit_doc[key]

    log("## OBJECT: {}".format(obj))

    states = ['acknowledged', 'saved', 'reported',]

    for state in states:
        time.sleep(1)
        log("## UPDATE {}".format(state.upper()))
        db.edit_documents.update(
            {'_id': edit_doc['_id']},
            { '$set': {
                'state': state
            }})

    db.edit_documents.update(
        {'_id': edit_doc['_id']},
        { '$set': {
            'state': 'ready',
            'action': 'read'
        }})
    log("## READY READ")
