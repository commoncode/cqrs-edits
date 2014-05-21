import bson
import datetime
import time

from optparse import make_option
from django.core.management.base import BaseCommand

from pymongo import MongoClient
from pymongo.cursor import _QUERY_OPTIONS
from pymongo.errors import AutoReconnect

from ...tasks import process_edit_doc


class Command(BaseCommand):
    help = 'Monitor the Mongo Oplog for changes to the Edits Collection Documents'

    # Tailable cursor options.
    _TAIL_OPTS = {'tailable': True, 'await_data': True}

    # Time to wait for data or connection.
    _SLEEP = 1

    def handle(self, *args, **options):

        db = MongoClient().local

        while True:

            query = {
                'ts': {'$gt': bson.timestamp.Timestamp(datetime.datetime.now(),0) }
            }
            cursor = db.oplog.rs.find(query, **self._TAIL_OPTS)
            cursor.add_option(_QUERY_OPTIONS['oplog_replay'])

            try:
                while cursor.alive:
                    print 'alive'
                    try:
                        doc = cursor.next()

                        if 'edit_document' in doc['ns']:

                            try:
                                state = doc['o']['$set']['state']
                                print 'state: {}'.format(state)

                                action = doc['o']['$set']['action']
                                print 'action: {}'.format(action)
                            except KeyError, e:
                                print e
                            else:
                                if state == 'committed':
                                    print '** COMMIT **'
                                    print doc

                                    print '** FETCH **'
                                    db = MongoClient()[doc['ns'].split('.')[0]]
                                    edit_doc = db[doc['ns'].split('.')[1]].find_one({'_id': doc['o2']['_id']})
                                    print edit_doc

                                    print '** QUEUE TO PROCESS **'
                                    process_edit_doc(edit_doc)

                    except (AutoReconnect, StopIteration), e:
                        print e
                        print 'sleep'
                        time.sleep(self._SLEEP)

            finally:
                print 'close'
                cursor.close()
