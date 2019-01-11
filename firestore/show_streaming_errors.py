# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
This helper file is used to print files not imported into BigQuery
'''

from google.cloud import firestore

NAME_SIZE = 40
WHEN_SIZE = 24
MESSAGE_SIZE = 80

def _print_header():
    _print_line()
    print(u'| %s | %s | %s |' % (
        u'File Name'.ljust(NAME_SIZE)[:NAME_SIZE],
        u'When'.ljust(WHEN_SIZE)[:WHEN_SIZE],
        u'Error Message'.ljust(MESSAGE_SIZE)[:MESSAGE_SIZE],))
    _print_line()

def _print_footer():
    _print_line()

def _print_line():
    print(u'+-%s-+-%s-+-%s-+' % (
        u''.ljust(NAME_SIZE, '-')[:NAME_SIZE],
        u''.ljust(WHEN_SIZE, '-')[:WHEN_SIZE],
        u''.ljust(MESSAGE_SIZE, '-')[:MESSAGE_SIZE],))

# [START firestore-query]
db = firestore.Client()
docs = db.collection(u'streaming_files')\
    .where(u'success', u'==', False)\
    .get()
# [END firestore-query]

_print_header()
for doc in docs:
    data = doc.to_dict()
    name = doc.id.ljust(NAME_SIZE)[:NAME_SIZE]
    when = data['when'].ljust(WHEN_SIZE)[:WHEN_SIZE]
    error_message = data['error_message']
    error = (error_message[:MESSAGE_SIZE-2] + '..') \
        if len(error_message) > MESSAGE_SIZE \
        else error_message.ljust(MESSAGE_SIZE)[:MESSAGE_SIZE]
    print(u'| %s | %s | %s |' % (name, when, error))
_print_footer()
